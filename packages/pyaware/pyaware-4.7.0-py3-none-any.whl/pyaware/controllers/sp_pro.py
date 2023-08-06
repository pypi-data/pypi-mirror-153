import asyncio
import struct
import typing
from datetime import datetime

import pyaware
import pyaware.data_types
import pyaware.data_types.modbus
import pyaware.triggers
import pyaware.aggregations
import pyaware.transformations
from pyaware import watchdog
from pyaware.store import memory_storage
from pyaware import events
from pyaware import log
from pyaware.mqtt.models import TopologyChildren

from aiosppro.serial import SPPROSerialClient

numeric = typing.Union[int, float]


class SPPRODevice:
    dev_type = "sppro-device"

    def __init__(
        self,
        client: SPPROSerialClient,
        device_id: str,
        config,
        poll_intervals: typing.Optional[typing.Dict[str, numeric]] = None,
    ):
        self.client = client
        self.device_id = device_id
        if poll_intervals is None:
            self.poll_intervals = {}
        else:
            self.poll_intervals = poll_intervals
        self.store_state = {}
        self.send_state = {}
        self.event_state = {}
        self.current_state = {}
        self.config = pyaware.config.load_yaml_config(config)
        self.parameters = pyaware.data_types.parse_data_types(
            self.config["parameters"], {}
        )
        self.triggers = pyaware.triggers.build_from_device_config(
            config,
            device_id=device_id,
            send_state=self.send_state,
            store_state=self.store_state,
            event_state=self.event_state,
            current_state=self.current_state,
        )
        self.transformations = pyaware.transformations.build_from_device_config(config)
        self.aggregates = pyaware.aggregations.build_from_device_config(config)

    def init(self):
        # Initialise subscriptions
        events.subscribe(self.process_data, topic=f"process_data/{id(self)}")
        events.subscribe(self.process_write, topic=f"process_write/{id(self)}")

        for name, source_config in self.config["sources"].items():
            if source_config.get("type", "poll") == "poll":
                asyncio.create_task(self.trigger_poll(name))
        self.setup_watchdogs()

    def setup_watchdogs(self):
        try:
            self.client.protocol.connection_made = watchdog.watch(
                f"sppro_serial_status_{id(self)}"
            )(self.client.protocol.connection_made)
        except AttributeError:
            pass
        try:
            self.client.protocol.connection_lost = watchdog.watch_starve(
                f"sppro_serial_status_{id(self)}"
            )(self.client.protocol.connection_lost)
        except AttributeError:
            pass
        try:
            self.client.read = watchdog.watch(f"sppro_serial_status_{id(self)}")(
                self.client.read
            )
        except AttributeError:
            pass
        try:
            self.client.write = watchdog.watch(f"sppro_serial_status_{id(self)}")(
                self.client.write
            )
        except AttributeError:
            pass
        dog_eth = watchdog.WatchDog(
            heartbeat_time=5,
            success_cbf=lambda: events.publish(
                f"process_data/{id(self)}",
                data={"serial-comms-status": True},
                timestamp=datetime.utcnow(),
                device_id=self.device_id,
            ),
            failure_cbf=lambda: events.publish(
                f"process_data/{id(self)}",
                data={"serial-comms-status": False},
                timestamp=datetime.utcnow(),
                device_id=self.device_id,
            ),
        )
        watchdog.manager.add(f"sppro_serial_status_{id(self)}", dog_eth)
        dog_eth.start(start_fed=False)

    async def trigger_poll(self, source: str, poll_interval=None):
        # TODO replace poll interval with config patching
        # Checks device config
        try:
            poll_interval = self.config["sources"][source]["poll_interval"]
        except KeyError:
            pass
        # Overwrites device config if poll intervals exists in gateway config
        try:
            poll_interval = self.poll_intervals[source]
        except KeyError:
            pass
        # If all fails sets to 5
        if poll_interval is None:
            poll_interval = 5
        loop = asyncio.get_running_loop()
        start = loop.time()
        log.info(f"Waiting for connection for {self.device_id}")
        await self.client.connected.wait()
        log.info(f"Starting poll pipeline for {self.device_id}")
        blocks = self.config["sources"][source]["blocks"]
        while True:
            if pyaware.evt_stop.is_set():
                log.info(f"Closing SP PRO device {self.device_id} polling")
                return
            try:
                start = loop.time()
                await self.poll_pipeline(blocks, source)
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning(
                        f"SP PRO device {self.device_id} cancelled without stop signal"
                    )
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)
            sleep_time = start - loop.time() + poll_interval
            if sleep_time > 0:
                await asyncio.sleep(start - loop.time() + poll_interval)

    async def poll_pipeline(self, blocks, source):
        addr_map = pyaware.data_types.modbus.AddressMapUint16()
        for start, end in blocks:
            count = len(range(start, end))
            addr_map.merge(await self.read(start, count))
        timestamp = datetime.utcnow()
        if timestamp is None:
            timestamp = datetime.utcnow()
        device_data = {}
        for k, v in self.config["parameters"].items():
            if v.get("source") == source:
                try:
                    device_data.update(self.parameters[k].decode(addr_map))
                except KeyError:
                    pass
        processed_data = await events.publish(
            f"process_data/{id(self)}",
            data=device_data,
            timestamp=timestamp,
            device_id=self.device_id,
        ).all()
        self.current_state.update(device_data)

    async def process_data(self, data, timestamp, device_id):
        transformed_data = pyaware.transformations.transform(data, self.transformations)
        store_data, send_data, event_data = await asyncio.gather(
            pyaware.triggers.process.run_triggers(
                self.triggers.get("process", {}).get("store", {}),
                transformed_data,
                timestamp,
            ),
            pyaware.triggers.process.run_triggers(
                self.triggers.get("process", {}).get("send", {}),
                transformed_data,
                timestamp,
            ),
            pyaware.triggers.process.run_triggers(
                self.triggers.get("process", {}).get("event", {}),
                transformed_data,
                timestamp,
            ),
        )
        if store_data:
            memory_storage.update(store_data, topic=f"{self.device_id}")
            self.store_state.update(store_data)
        if send_data:
            memory_storage.update(send_data, topic=f"{self.device_id}")
            cached_data = memory_storage.pop(f"{self.device_id}")
            aggregated_data = pyaware.aggregations.aggregate(
                cached_data, self.aggregates
            )
            events.publish(
                f"trigger_send",
                data=aggregated_data,
                meta=self.dict(),
                timestamp=timestamp,
                topic_type="telemetry",
                device_id=self.device_id,
            )
            self.send_state.update(cached_data)
        if event_data:
            for param, value in event_data.items():
                events.publish(
                    f"parameter_trigger/{self.device_id}/{param}",
                    data=next(iter(value.values())),
                    timestamp=timestamp,
                )
            self.event_state.update(event_data)
        return send_data

    async def process_write(self, register_type: str, data: typing.Dict[str, int]):
        """
        Processes write to an SP-PRO device.

        :param register_type: Type of register to be written to. i.e. "holding" OR "coils". Not applicable for SP PRO
        devices
        :param data: Data as a dictionary in the format {"param1": data, "param2": data, ...} to be written.
        """
        addr_map = pyaware.data_types.modbus.AddressMapUint16()
        for param_name, val in data.items():
            if type(self.parameters[param_name]) == pyaware.data_types.modbus.ParamBits:
                data_to_encode = val
            else:
                data_to_encode = {param_name: val}
            self.parameters[param_name].encode(data_to_encode, addr_map)
        # Gets contiguous address blocks
        # In the form: blocks = [[start1, end1], [start2, end2], ...]
        blocks = []
        index = 0
        sorted_addr_map = sorted(addr_map._buf.items())
        for addr, val in sorted_addr_map:
            if len(blocks) != (index + 1):
                blocks.append([addr, addr])
            if (addr + 1) not in addr_map._buf.keys():
                blocks[index][1] = addr
                index += 1
        # Writes block to the SP-PRO device
        for start, end in blocks:
            values = addr_map[start : end + 1]
            await self.client.write(start, values)

    async def read(self, start_addr: int, num_addr_to_read: int, timeout=None):
        addr_map = pyaware.data_types.modbus.AddressMapUint16()
        try:
            data = await self.client.read(
                start_addr=start_addr,
                num_addr_to_read=num_addr_to_read,
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            await asyncio.sleep(1)
            return addr_map
        except BaseException as e:
            log.exception(e)
            raise
        try:
            # Expecting 16-bit word for each address, so unpacking as such and capturing the rest.
            # returns empty data if data cannot be unpacked.
            unpacked_data = struct.unpack("<" + "H" * (len(data) // 2), data)
            addr_map[start_addr : start_addr + num_addr_to_read] = unpacked_data
        except (struct.error, IndexError) as e:
            log.exception(e)
            log.warning(
                f"SP PRO device {self.device_id} data was unpacked improperly or set improperly into the address map."
                f"Expecting 16-bit word for each address. Data received: {data}"
            )
        return addr_map

    def identify(self):
        response = TopologyChildren(
            values={},
            type=self.dev_type,
            serial=self.device_id,
            children=[],
        )
        return response

    def dict(self):
        response = {"type": self.dev_type}
        return response
