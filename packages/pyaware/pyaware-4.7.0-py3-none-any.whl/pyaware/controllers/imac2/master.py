import asyncio
import json
import os
import struct
import time
import typing
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import aiohttp

import pyaware.aggregations
import pyaware.commands
import pyaware.config
import pyaware.events
import pyaware.protocol
import pyaware.triggers
from pyaware import events, async_threaded
from pyaware.commands import Commands, ValidateIn, TopicTask, InvalidCommandData
from pyaware.data_types.modbus import AddressMapUint16
from pyaware.mqtt.models import TopologyChildren
from pyaware.protocol.imac2 import ModuleStatus
from pyaware.protocol.imac2.modules import ImacModule, module_types
from pyaware.protocol.imac2.protocol import log
from pyaware.controllers.imac2.topology import Topology
from pyaware.store import memory_storage
from pyaware.triggers.collect import Deadline
from pyaware.triggers.process import run_triggers
from pyaware.protocol.imac2.protocol import Imac2Protocol
from pyaware import watchdog


async def auto_detect(protocol: Imac2Protocol):
    await protocol.client_eth.connected.wait()
    dev = ImacControllerDevice(
        protocol,
        module_type="imac-controller-master",
        config_name="imac_controller_parameter_spec.yaml",
        device_id="unknown_auto_detect",
    )
    # Retry to overcome issue with iMAC in certain failed states requiring multiple connection attempts and
    # reads before responding
    for _ in range(50):
        try:
            resp = await dev.read_parameters(
                {"slp-version", "serial-number", "rotary-sw", "master-fieldbus-number"}
            )
            break
        except (asyncio.TimeoutError, asyncio.CancelledError):
            if pyaware.evt_stop.is_set():
                return
            await asyncio.sleep(1)
            continue

    else:
        log.warning("Failed to read from iMAC modbus stopping pyaware")
        pyaware.stop()

    if resp["slp-version"].startswith("RTGS GG2 Master V"):
        log.info("Auto detected Gasguard Live Master Controller")
        device_id = f"imac-{resp['master-fieldbus-number']}"
        serial_number = resp["serial-number"]
        control = Imac2MasterController(device_id, serial_number, protocol)
        # Start RTGM topology
        Topology(
            device_id=f"imac-{resp['master-fieldbus-number']}",
            serial_number=resp["serial-number"],
            update_interval=60,
        )
        return control
    elif resp["slp-version"].startswith("RTGS GG2 Slave V"):
        logical_number = int(resp["rotary-sw"]) + 1
        device_id = f"rts-{resp['master-fieldbus-number']}-{logical_number}"
        serial_number = resp["serial-number"]
        control = ImacControllerRts(device_id, serial_number, logical_number, protocol)
        # Start RTGM topology
        if resp["master-fieldbus-number"] != 0:
            Topology(
                device_id=f"imac-{resp['master-fieldbus-number']}",
                serial_number=resp["serial-number"],
                update_interval=60,
            )
        return control
    else:
        raise ValueError(f"Unknown imac controller slp version {resp['slp-version']}")


class ImacControllerDevice:
    name = "Imac Controller"

    def __init__(
        self,
        protocol: Imac2Protocol,
        module_type: str,
        config_name: str,
        device_id: str,
    ):
        """ """
        self.protocol = protocol
        self.module_type = module_type
        self.device_id = device_id
        self.config_name = config_name
        self.config_path = (
            Path(pyaware.__file__).parent
            / "devices"
            / "ampcontrol"
            / "imac"
            / self.config_name
        )
        self.config = pyaware.config.load_yaml_config(self.config_path)
        self.parameters = pyaware.data_types.parse_data_types_by_source(
            self.config["parameters"], {}
        )
        self.data_point_blocks = self._modbus_ranges(
            (0, 0x47F), (0x500, 0x580), (0x600, 0x6A2)
        )
        self.parameter_handlers = {
            "rest": self.parameter_handler_rest,
            "poll": self.parameter_handler_poll,
        }

    def _modbus_ranges(self, *ranges, max_block=125):
        return [
            (x, min([max_block, stop - x]))
            for start, stop in ranges
            for x in range(start, stop, max_block)
        ]

    async def read_parameters(self, data: set):
        """
        :param data: A set of parameter values to read
        :param exact: If true will only return the parameters that were in the original data set
        :return:
        """
        parameters = {}
        for source in self.parameters:
            handler = self.parameter_handlers[source]
            parameters.update(await handler(data))
        return parameters

    async def parameter_handler_rest(self, data: set):
        rest_data = await self.protocol.read_rest_data()
        parameters = {}
        for key in data.intersection(self.parameters["rest"]):
            param_spec = self.parameters["rest"][key]
            parameters.update(param_spec.decode(rest_data))
        return parameters

    async def parameter_handler_poll(self, data: set):
        addr_map = AddressMapUint16()
        for address, count in self.data_point_blocks:
            addr_map.merge(await self.protocol.read_eth(address, count))
        parameters = {}
        for key in data.intersection(self.parameters["poll"]):
            param_spec = self.parameters["poll"][key]
            parameters.update({k: v for k, v in param_spec.decode(addr_map).items()})
        return parameters

    def identify(self):
        return self.dict()

    def dict(self):
        return {"type": self.module_type}


@events.enable
class ImacControllerRts:
    name = "Imac Controller"
    module_type = "imac-controller-rts"
    config_name = "rts_controller_parameter_spec.yaml"

    def __init__(
        self,
        device_id: str,
        serial_number: str,
        logical_number: int,
        protocol: Imac2Protocol,
    ):
        self.device_id = device_id
        self.serial_number = serial_number
        self.logical_number = logical_number
        self.fieldbus_address = int(self.device_id.split("-")[1])
        if self.fieldbus_address == 0:
            log.info(f"Invalid fieldbus address 0 for rts restarting")
            # Stop pyAWARE in ~1second to allow for gateway heartbeat and state message to come through
            asyncio.create_task(pyaware.stop_in(1))
            return
        self.store_state = {}
        self.send_state = {}
        self.event_state = {}
        self.current_state = {
            "logical-number": self.logical_number,
            "master-fieldbus-number": self.fieldbus_address,
            "dev-id": self.device_id,
        }
        self.config_path = (
            Path(pyaware.__file__).parent
            / "devices"
            / "ampcontrol"
            / "imac"
            / self.config_name
        )
        self.config = pyaware.config.load_yaml_config(self.config_path)
        self.parameters = pyaware.data_types.parse_data_types_by_source(
            self.config["parameters"], self.current_state
        )
        self.modules = {}
        self.protocol = protocol
        self.triggers = pyaware.triggers.build_from_device_config(
            self.config_path,
            device_id=self.device_id,
            send_state=self.send_state,
            store_state=self.store_state,
            event_state=self.event_state,
            current_state=self.current_state,
        )
        self.aggregates = pyaware.aggregations.build_from_device_config(
            self.config_path
        )
        self.data_point_blocks = self._modbus_ranges(
            (0, 0x47F), (0x500, 0x580), (0x600, 0x6A2)
        )
        self.commands = Commands(
            {}, device_id=device_id, command_destination=self.device_id
        )
        self.poll_interval = 0.5
        self.commands.update(
            {
                "boundary-enable": [
                    pyaware.commands.ValidateHandle(lambda x: len(x) == 40),
                    pyaware.commands.TopicTask(f"boundary_enable", {"data": "value"}),
                ],
                "trip-reset": [pyaware.commands.TopicTask(f"trip_reset")],
            }
        )
        self.update_topology()

    def init(self):
        if self.fieldbus_address == 0:
            return
        asyncio.create_task(self.trigger_poll())
        asyncio.create_task(self.trigger_heartbeat())
        events.subscribe(
            self.rotary_switch_update,
            topic=f"parameter_trigger/{self.serial_number}/rotary-sw",
        )
        events.subscribe(
            self.fieldbus_number_update,
            topic=f"parameter_trigger/{self.serial_number}/master-fieldbus-number",
        )
        events.subscribe(
            self.serial_number_update,
            topic=f"parameter_trigger/{self.serial_number}/serial-number",
        )
        self.setup_watchdogs()

    def setup_watchdogs(self):
        dog_eth = watchdog.WatchDog(
            10,
            lambda: self.process_module_data_triggers({"ethernet-comms-status": True}),
            lambda: self.process_module_data_triggers({"ethernet-comms-status": False}),
        )

        dog_ser = watchdog.WatchDog(
            90,
            lambda: self.process_module_data_triggers({"serial-comms-status": True}),
            lambda: self.process_module_data_triggers({"serial-comms-status": False}),
        )

        dog_heartbeat_poll = watchdog.WatchDog(
            10,
            lambda: events.publish(
                f"trigger_send",
                data={},
                meta=self.dict(),
                timestamp=datetime.utcnow(),
                topic_type="device_heartbeat_serial_source",
                device_id=self.device_id,
                serial_number=self.serial_number,
                source="poll",
            ),
        )
        watchdog.manager.add("imac_eth_status", dog_eth)
        watchdog.manager.add("imac_ser_status", dog_ser)
        watchdog.manager.add("imac_heartbeat_poll", dog_heartbeat_poll)
        try:
            self.client_eth.protocol_made_connection = watchdog.watch(
                "imac_eth_status", starve_on_exception=3
            )(self.client_eth.protocol_made_connection)
        except AttributeError:
            pass
        try:
            self.client_eth.protocol_lost_connection = watchdog.watch_starve(
                "imac_eth_status"
            )(self.client_eth.protocol_lost_connection)
        except AttributeError:
            pass
        try:
            self.client_eth.protocol_made_connection = watchdog.watch(
                "imac_ser_status", starve_on_exception=3
            )(self.client_eth.protocol_made_connection)
        except AttributeError:
            pass
        try:
            self.client_eth.protocol_lost_connection = watchdog.watch_starve(
                "imac_ser_status"
            )(self.client_eth.protocol_lost_connection)
        except AttributeError:
            pass
        dog_eth.start(start_fed=False)
        dog_ser.start(start_fed=False)
        dog_heartbeat_poll.start(start_fed=False)

    def _modbus_ranges(self, *ranges, max_block=125):
        return [
            (x, min([max_block, stop - x]))
            for start, stop in ranges
            for x in range(start, stop, max_block)
        ]

    async def rotary_switch_update(self, data, timestamp):
        if data + 1 != self.logical_number:
            log.warning(
                f"{self.device_id} has had the logical number changed from {self.logical_number} to {data + 1}. Restarting pyaware"
            )
            pyaware.stop()

    async def serial_number_update(self, data, timestamp):
        if data != self.serial_number:
            log.warning(
                f"{self.device_id} has had the serial number changed from {self.serial_number} to {data}. Restarting pyaware"
            )
            pyaware.stop()

    async def fieldbus_number_update(self, data, timestamp):
        if data != self.fieldbus_address:
            log.warning(
                f"{self.device_id} has had the fieldbus number changed from {self.fieldbus_address} to {data}. Restarting pyaware"
            )
            pyaware.stop()

    @events.subscribe(topic="trip_reset")
    async def trip_reset(self):
        """
        Perform a remote trip reset.
        :return:
        """
        await self.protocol.write_bit(0x525, 15, 0)
        await asyncio.sleep(0.5)
        await self.protocol.write_bit(0x525, 15, 1)

    async def trigger_poll(self):
        loop = asyncio.get_running_loop()
        start = loop.time()
        log.info(f"Starting {self.device_id} bus polling")
        while True:
            if pyaware.evt_stop.is_set():
                log.info(f"Closing {self.device_id} polling")
                return
            try:
                await asyncio.sleep(start - loop.time() + self.poll_interval)
                start = loop.time()
                await self.poll_pipeline()
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning(f"iMAC {self.device_id} cancelled without stop signal")
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)

    async def process_rest_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://{self.protocol.client_eth.host}/cgi-bin/deviceinfo.cgi"
                ) as response:
                    text_obj = await response.read()
                    json_obj = json.loads(text_obj.decode("utf-8", "ignore"))
                    parameters = {}
                    for param_spec in self.parameters["rest"].values():
                        parameters.update(
                            {k: v for k, v in param_spec.decode(json_obj).items()}
                        )
                    return parameters
        except AttributeError:
            pass
        except BaseException as e:
            log.error(repr(e))
        return {}

    async def poll_pipeline(self):
        """
        Pipeline that begins when a pipeline is published
        :param data:
        :return:
        """
        poll_data, rest_data, static_data = await asyncio.gather(
            self.poll_once(), self.process_rest_data(), self.process_static_data()
        )
        addr_map, timestamp = poll_data
        controller_data = await self.process_controller_data(addr_map)
        data = {**controller_data, **rest_data, **static_data}
        await self.process_module_data_triggers(data, timestamp)

    @watchdog.watch("imac_heartbeat_poll", feed_on_entry=True)
    async def poll_once(self) -> typing.Tuple[AddressMapUint16, datetime]:
        """
        Perform a complete poll of the imac data
        :requires: client_eth to be available
        :return:
        """
        addr_map = AddressMapUint16()
        for address, count in self.data_point_blocks:
            addr_map.merge(await self.protocol.read_eth(address, count))
        return addr_map, datetime.utcnow()

    async def process_static_data(self):
        data = {param.idx: param.value for param in self.parameters["static"].values()}
        data.update(
            {
                param.idx: self.current_state[param.idx]
                for param in self.parameters["state"].values()
            }
        )
        return data

    async def process_module_data_triggers(self, data, timestamp=None):
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.update_current_state(data)
        store_data, send_data, event_data = await asyncio.gather(
            run_triggers(
                self.triggers.get("process", {}).get("store", {}), data, timestamp
            ),
            run_triggers(
                self.triggers.get("process", {}).get("send", {}), data, timestamp
            ),
            run_triggers(
                self.triggers.get("process", {}).get("event", {}), data, timestamp
            ),
        )
        if store_data:
            memory_storage.update(store_data, topic=f"{self.device_id}")
            self.update_store_state(store_data)
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
                topic_type="telemetry_serial",
                device_id=self.device_id,
                serial_number=self.serial_number,
            )
            self.update_send_state(cached_data)
        if event_data and self.serial_number:
            for param, value in event_data.items():
                events.publish(
                    f"parameter_trigger/{self.serial_number}/{param}",
                    data=next(iter(value.values())),
                    timestamp=timestamp,
                )
            self.event_state.update(event_data)

    def update_store_state(self, parameters: dict):
        """
        Update the state the module has represented in the cache database
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.store_state.update(parameters)

    def update_send_state(self, parameters: dict):
        """
        Update the state used the module has represented from queued mqtt messages
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.send_state.update(parameters)

    def update_event_state(self, parameters: dict):
        """
        Update the state used the module has represented from queued mqtt messages
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.event_state.update(parameters)

    def update_current_state(self, parameters: dict):
        """
        Update the state used to run diff module data against
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.current_state.update(parameters)

    @async_threaded
    def process_controller_data(self, addr_map: AddressMapUint16):
        """
        Process
        :param addr_map:
        :param timestamp:
        :return:
        """
        parameters = {}
        for param_spec in self.parameters["poll"].values():
            parameters.update({k: v for k, v in param_spec.decode(addr_map).items()})
        return parameters

    def dict(self):
        return {"type": self.module_type, "serial": self.serial_number}

    @events.subscribe(topic="request_topology")
    def update_topology(self):
        children = [dev.identify() for dev in self.modules.values()]
        payload = TopologyChildren(
            serial=self.serial_number,
            type=self.module_type,
            values={},
            children=children,
        )
        events.publish(
            f"device_topology/{self.device_id}",
            data=payload,
            timestamp=datetime.utcnow(),
        )

    @events.subscribe(topic="boundary_enable")
    async def boundary_enable(self, data):
        """
        :param data: 40 bit sequence in an array corresponding to detectors 1-40
        :param timestamp:
        :return:
        """
        if len(data) != 40:
            raise ValueError
        addr_map = AddressMapUint16()
        addr_map[0x520:0x523] = 0, 0, 0
        for index, bit in enumerate(data):
            address = 0x520 + index // 16
            addr_map[address] |= bit << (index % 16)
        await self.protocol.write(0x520, *addr_map[0x520:0x523])

    async def trigger_heartbeat(self):
        value = 1
        log.info("Starting imac master plc heartbeat writes")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing imac master heartbeat")
                return
            try:
                await self.protocol.write(0x524, value)
                value = (value % 1000) + 1
                await asyncio.sleep(10)
                continue
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning(
                        "iMAC master plc heartbeat cancelled without stop signal"
                    )
                    continue
            except BaseException as e:
                if pyaware.evt_stop.is_set():
                    continue
                log.error(repr(e))
            await asyncio.sleep(1)


@events.enable
class Imac2MasterController:
    name = "Imac Controller"
    module_type = "imac-controller-master"
    config_name = "imac_controller_parameter_spec.yaml"

    def __init__(self, device_id: str, serial_number: str, protocol: Imac2Protocol):
        """ """
        self.device_id = device_id
        self.serial_number = serial_number
        self.fieldbus_address = int(self.device_id.split("-")[-1])
        self.device = ImacControllerDevice(
            protocol, self.module_type, self.config_name, self.device_id
        )
        self.protocol = protocol
        self.store_state = {}
        self.send_state = {}
        self.event_state = {}
        self.current_state = {"master-fieldbus-number": self.fieldbus_address}
        self.triggers = pyaware.triggers.build_from_device_config(
            self.device.config_path,
            device_id=self.device_id,
            send_state=self.send_state,
            store_state=self.store_state,
            event_state=self.event_state,
            current_state=self.current_state,
        )
        self.aggregates = pyaware.aggregations.build_from_device_config(
            self.device.config_path
        )
        self.schedule_reads: typing.Dict[str, Deadline] = {}
        self.poll_interval = 1
        # TODO load from store
        self.modules: {str: ImacModule} = {}
        self.data_point_blocks = self._modbus_ranges(
            (0, 0x47F), (0x500, 0x580), (0x600, 0x6A2)
        )
        self.commands = Commands(
            {}, device_id=device_id, command_destination=self.serial_number
        )
        self.auto_discover_lock = asyncio.Lock()
        self.commands.update(
            {
                "find-system": [
                    TopicTask(topic="imac_discover_system"),
                ],
                "find-modules": [
                    ValidateIn(range(256)),
                    TopicTask(topic="find_modules", key_map={"data": "address"}),
                ],
                "find-serial": [
                    TopicTask(
                        topic="find_serial",
                        key_map={"data": "serial"},
                        include_cmd_as_key="cmd",
                    ),
                ],
                "clear-address": [
                    ValidateIn(range(256)),
                    TopicTask(topic="clear_address", key_map={"data": "address"}),
                ],
                "remove-devices": [
                    pyaware.commands.TopicTask(
                        f"remove_devices", {"devices": "devices"}
                    )
                ],
                "sync-rtc": [
                    TopicTask(topic="sync_rtc", key_map={"timestamp": "value"})
                ],
                "boundary-enable": [
                    TopicTask(topic=f"boundary_enable/{id}", key_map={"data": "value"}),
                ],
                "remote-bypass-gg2": [
                    ValidateIn(range(1, 41), key="address"),
                    ValidateIn(range(2), key="value"),
                    TopicTask(
                        topic="remote_bypass_gg2",
                        key_map={"logical_address": "address", "value": "value"},
                    ),
                ],
                "remote-bypass-rts": [
                    ValidateIn(range(1, 13), key="address"),
                    ValidateIn(range(2), key="value"),
                    TopicTask(
                        topic="remote_bypass_rts",
                        key_map={"logical_address": "address", "value": "value"},
                    ),
                ],
                "plc-trip-reset": [
                    TopicTask(topic="plc_trip_reset"),
                ],
                "trip-reset": [
                    TopicTask(topic="trip_reset"),
                ],
            }
        )
        self.schema = pyaware.config.load_yaml_config(
            os.path.join(os.path.dirname(__file__), "ensham_schema.yaml")
        )

    def init(self):
        events.subscribe(
            self.fieldbus_number_update,
            topic=f"parameter_trigger/{self.serial_number}/master-fieldbus-number",
        )
        events.subscribe(
            self.serial_number_update,
            topic=f"parameter_trigger/{self.serial_number}/serial-number",
        )
        asyncio.create_task(self.trigger_poll())
        asyncio.create_task(self.trigger_rest())
        asyncio.create_task(self.trigger_blocks())
        asyncio.create_task(self.trigger_heartbeat())
        asyncio.create_task(
            self.trigger_system_address_roll_call(60 * 60 * 24)  # Daily
        )
        self.setup_watchdogs()

    def setup_watchdogs(self):
        dog_eth = watchdog.WatchDog(
            10,
            lambda: self.process_module_data_triggers({"ethernet-comms-status": True}),
            lambda: self.process_module_data_triggers({"ethernet-comms-status": False}),
        )

        dog_ser = watchdog.WatchDog(
            90,
            lambda: self.process_module_data_triggers({"serial-comms-status": True}),
            lambda: self.process_module_data_triggers({"serial-comms-status": False}),
        )

        dog_heartbeat_poll = watchdog.WatchDog(
            10,
            lambda: events.publish(
                f"trigger_send",
                data={},
                meta=self.dict(),
                timestamp=datetime.utcnow(),
                topic_type="device_heartbeat_serial_source",
                device_id=self.device_id,
                serial_number=self.serial_number,
                source="poll",
            ),
        )
        watchdog.manager.add("imac_eth_status", dog_eth)
        watchdog.manager.add("imac_ser_status", dog_ser)
        watchdog.manager.add("imac_heartbeat_poll", dog_heartbeat_poll)

        dog_eth.start(start_fed=False)
        dog_ser.start(start_fed=False)
        dog_heartbeat_poll.start(start_fed=False)
        try:
            self.client_eth.protocol_made_connection = watchdog.watch(
                "imac_eth_status"
            )(self.client_eth.protocol_made_connection)
        except AttributeError:
            pass
        try:
            self.client_eth.protocol_lost_connection = watchdog.watch_starve(
                "imac_eth_status"
            )(self.client_eth.protocol_lost_connection)
        except AttributeError:
            pass
        try:
            self.client_eth.protocol_made_connection = watchdog.watch(
                "imac_ser_status"
            )(self.client_eth.protocol_made_connection)
        except AttributeError:
            pass
        try:
            self.client_eth.protocol_lost_connection = watchdog.watch_starve(
                "imac_ser_status"
            )(self.client_eth.protocol_lost_connection)
        except AttributeError:
            pass

    def _modbus_ranges(self, *ranges, max_block=125):
        return [
            (x, min([max_block, stop - x]))
            for start, stop in ranges
            for x in range(start, stop, max_block)
        ]

    async def trigger_poll(self):
        loop = asyncio.get_running_loop()
        start = loop.time()
        log.info("Starting imac master bus polling")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing imac master polling")
                return
            try:
                await asyncio.sleep(start - loop.time() + self.poll_interval)
                start = loop.time()
                await self.poll_pipeline()
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning("iMAC master poll cancelled without stop signal")
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)

    async def trigger_rest(self):
        log.info("Starting imac master rest polling")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Stop signal received, closing imac master rest calls")
                return
            try:
                await asyncio.sleep(5)
                json_obj = await self.protocol.read_rest_data()
                parameters = {}
                for param_spec in self.device.parameters["rest"].values():
                    parameters.update(
                        {k: v for k, v in param_spec.decode(json_obj).items()}
                    )
                pyaware.events.publish(
                    "imac_controller_data",
                    data=parameters,
                    timestamp=datetime.utcnow(),
                )
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning("iMAC master rest calls cancelled without stop signal")
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.error(repr(e))

    async def trigger_heartbeat(self):
        value = 1
        log.info("Starting imac master plc heartbeat writes")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing imac master heartbeat")
                return
            try:
                await asyncio.sleep(30)
                await self.protocol.write(0x525, value)
                value = (value % 1000) + 1
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning(
                        "iMAC master plc heartbeat cancelled without stop signal"
                    )
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)

    async def trigger_blocks(self):
        """
        Schedules block and force_roll call based on deadline.
        :return:
        """
        loop = asyncio.get_running_loop()
        wait_time = 5
        start = loop.time()
        log.info("Starting imac master block reads")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing imac master scheduled device parameter reads")
                return
            try:
                sleep_time = start - loop.time() + wait_time
                if sleep_time < 0:
                    sleep_time = 0
                await asyncio.sleep(sleep_time)
                start = loop.time()
                # Get item from list
                try:
                    itm = min(self.schedule_reads.values())
                except ValueError:
                    continue
                await self.modules.get(itm.device).read_parameters({itm.param})
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning("iMAC master block reads cancelled without stop signal")
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)

    async def trigger_system_address_roll_call(self, seconds: int):
        """
        Schedules roll call of all system owned addresses
        :return:
        """
        log.info("Starting system address roll call schedule")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing system owned address roll call schedule")
                return
            try:
                await asyncio.sleep(seconds)
                # Get system owned addresses
                log.info("Doing system address roll call")
                statuses = {
                    i: x
                    for i, x in enumerate(self.current_state["address-status"])
                    if x in [ModuleStatus.SYSTEM, ModuleStatus.SYSTEM_ONLINE]
                }
                log.info(f"Doing system address roll call {statuses}")
                events.publish("imac_discover_addresses", data=statuses)
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning("iMAC master block reads cancelled without stop signal")
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)

    async def serial_number_update(self, data, timestamp):
        if data != self.serial_number:
            log.warning(
                f"{self.device_id} has has the serial number changed from "
                f"{self.serial_number} to {data}. Restarting pyaware"
            )
            pyaware.stop()

    async def fieldbus_number_update(self, data, timestamp):
        if data != self.fieldbus_address:
            log.warning(
                f"{self.device_id} has has the fieldbus number changed from "
                f"{self.fieldbus_address} to {data}. Restarting pyaware"
            )
            pyaware.stop()

    @events.subscribe(topic="imac_controller_data")
    async def process_module_data_triggers(self, data, timestamp=None):
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.update_current_state(data)
        store_data, send_data, event_data = await asyncio.gather(
            run_triggers(
                self.triggers.get("process", {}).get("store", {}), data, timestamp
            ),
            run_triggers(
                self.triggers.get("process", {}).get("send", {}), data, timestamp
            ),
            run_triggers(
                self.triggers.get("process", {}).get("event", {}), data, timestamp
            ),
        )
        if store_data:
            memory_storage.update(store_data, topic=f"{self.device_id}")
            self.update_store_state(store_data)
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
                topic_type="telemetry_serial",
                device_id=self.device_id,
                serial_number=self.serial_number,
            )
            self.update_send_state(cached_data)
        if event_data and self.serial_number:
            for param, value in event_data.items():
                events.publish(
                    f"parameter_trigger/{self.serial_number}/{param}",
                    data=next(iter(value.values())),
                    timestamp=timestamp,
                )
            self.event_state.update(event_data)

    async def poll_pipeline(self):
        """
        Pipeline that begins when a pipeline is published
        :param data:
        :return:
        """
        addr_map, timestamp = await self.poll_once()
        events.publish("imac_poll_data", data=addr_map, timestamp=timestamp)
        module_data, module_status, controller_data = await asyncio.gather(
            self.process_module_data(addr_map, timestamp),
            self.process_module_status(addr_map, timestamp),
            self.process_controller_data(addr_map, timestamp),
        )
        self.update_module_current_state(module_data)
        await asyncio.gather(
            events.publish(
                "imac_module_data", data=module_data, timestamp=timestamp
            ).all(),
            events.publish(
                "imac_module_status", data=module_status, timestamp=timestamp
            ).all(),
            events.publish(
                "imac_controller_data", data=controller_data, timestamp=timestamp
            ).all(),
        )
        self.process_safe_gas()

    @events.subscribe(topic="find_modules")
    async def find_modules(self, data):
        await self.auto_discover_modules(
            data={data: self.current_state["address-status"][data]}
        )

    @events.subscribe(topic="find_serial")
    async def find_serial(self, data, cmd):
        """
        Find device by serial number
        :param data: Serial number of the form X-GY
        Where X is the serial between 1-65535 and Y is is the generation between 1-4

        Finds the serial numbered device by reading by serial number at block 0
        Param 1 is the address
        Discovers modules at that address
        :return:
        """
        cmd["return_values"]["serial"] = data
        cmd["return_values"]["type"] = None
        cmd["return_values"]["name"] = None
        cmd["return_values"]["status"] = False
        try:
            serial, gen = data.split("-G")
            serial = int(serial)
            gen = int(gen) - 1
            assert 1 <= serial <= 65535
            assert 0 <= gen <= 3
        except:
            raise InvalidCommandData(
                f"Invalid serial number: {data} must be of the form XXXXX-GX"
            )
        try:
            addr_map = await self.protocol.read_by_serial_number(
                serial_number=serial, generation=gen, block=0
            )
        except ValueError as e:
            if "Bit check failed" in e.args[0]:
                raise IOError(f"Could not find module @ {data}") from e
            raise
        module_address = addr_map[1038]
        async with self.auto_discover_lock:
            async for mod in self.discover_at_address(module_address):
                if mod.current_state["dev-id"] == data:
                    cmd["return_values"]["type"] = mod.module_type
                    cmd["return_values"]["name"] = mod.name
                    cmd["return_values"]["status"] = True
                    return

    @events.subscribe(topic="remove_devices")
    async def remove_devices(self, devices: list):
        """
        Remove a device from the current topology
        :return:
        """
        for dev in devices:
            try:
                mod = self.modules[dev]
            except KeyError:
                log.info(f"No known device: {dev}")
                continue
            await mod.disconnect()
            del self.modules[dev]
            log.info(f"Removed device: {dev}")
        self.update_topology()

    async def update_devices(self, modules: [dict]):
        """
        Updates the modules from a roll call
        :param roll_call: A list of address maps with data from the roll call addresses
        :return: None
        """
        devs = defaultdict(set)
        for imac_module in modules:
            dev_id = imac_module["dev_id"]
            if dev_id in self.modules:
                self.update_device(**imac_module)
            else:
                self.add_device(**imac_module)
            devs[dev_id].add(imac_module.get("module_type"))
        for dev_id in devs:
            try:
                await self.modules[dev_id].find_missing_starting_data()
            except BaseException as e:
                if pyaware.evt_stop.is_set():
                    raise
                log.error(repr(e))
            log.info(f"Added {self.modules[dev_id]}")
        if devs:
            self.update_topology()
        return devs

    def update_device(self, dev_id, **kwargs):
        """
        Update the device from roll call if any of the meta data of the device has changed
        :param dev_id:
        :param kwargs:
        :return:
        """
        if any(
            self.modules[dev_id].current_state.get(kwarg) != kwargs[kwarg]
            for kwarg in kwargs
        ):
            self.modules[dev_id].update_from_roll_call(dev_id=dev_id, **kwargs)
            self.commands.sub_commands[dev_id] = self.modules[dev_id].commands

    @events.subscribe(topic="request_topology")
    def update_topology(self):
        children = [dev.identify() for dev in self.modules.values()]
        payload = TopologyChildren(
            serial=self.serial_number,
            type=self.module_type,
            values={},
            children=children,
        )
        events.publish(
            f"device_topology/{self.device_id}",
            data=payload,
            timestamp=datetime.utcnow(),
        )

    def add_device(self, dev_id, module_type, **kwargs):
        """
        Add the device to the imac protocol. This will allow the imac data poll to interpret the data from the device
        :param dev_id:
        :param module_type:
        :param version:
        :param kwargs:
        :return:
        """
        self.modules[dev_id] = module_types.get(module_type, ImacModule)(
            controller=self, dev_id=dev_id
        )
        self.update_device(dev_id, module_type=module_type, **kwargs)

    @watchdog.watch("imac_heartbeat_poll", feed_on_entry=True)
    async def poll_once(self) -> typing.Tuple[AddressMapUint16, datetime]:
        """
        Perform a complete poll of the imac data
        :requires: client_eth to be available
        :return:
        """
        addr_map = AddressMapUint16()
        for address, count in self.data_point_blocks:
            addr_map.merge(await self.protocol.read_eth(address, count))
        return addr_map, datetime.utcnow()

    def process_poll(self, addr_map: AddressMapUint16):
        """
        Process the results from a poll_once call.
        Grouped in categories
        "system-data"
        "module-data":
        "system-runtime-variables"
        "nvm-variables"
        "nvm-user"
        "controller-information"

        Module data should be
        :param addr_map:
        :return:
        """

    @async_threaded
    def process_module_data(self, addr_map: AddressMapUint16, timestamp: datetime):
        """
        :param addr_map: address map returned from poll_once or poll_once_async
        :return: dictionary of parameter data indexed by imac serial number
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        module_data = {
            f"{dev.current_state['dev-id']}": dev.process_module_data(
                addr_map, timestamp
            )
            for dev in list(self.modules.values())
        }
        return module_data

    @async_threaded
    def process_module_status(self, addr_map: AddressMapUint16, timestamp: datetime):
        """
        Process the module status registers and trigger messages based on status changes
        :param addr_map:
        :param timestamp:
        :return:
        """
        status = {
            "address-status": [
                self.protocol.parse_status(addr_map[x + 0x100]) for x in range(1, 0x100)
            ],
            "address-status-raw": addr_map[0x100:0x200],
            "address-resistance": [addr_map[x] for x in range(0x201, 0x300)],
            "address-offline-count": [addr_map[x] & 0xFF for x in range(0x301, 0x400)],
            "address-clash-count": [addr_map[x] & 0xFF00 for x in range(0x301, 0x400)],
            "address-bypass": [
                self.protocol.parse_address_bypass(addr_map[x]) for x in range(81, 120)
            ],
        }
        # Make address 0 always System Status
        status["address-status"].insert(0, ModuleStatus.SYSTEM)
        status["address-resistance"].insert(0, 0)
        status["address-offline-count"].insert(0, 0)
        status["address-clash-count"].insert(0, 0)
        status["address-bypass"].insert(0, 0)
        return status

    @async_threaded
    def process_controller_data(self, addr_map: AddressMapUint16, timestamp: datetime):
        """
        Process
        :param addr_map:
        :param timestamp:
        :return:
        """
        parameters = {}
        for param_spec in list(self.device.parameters["poll"].values()):
            parameters.update({k: v for k, v in param_spec.decode(addr_map).items()})
        return parameters

    def process_safe_gas(self):
        """
        Processes a message for safe gas of each gas detector's gas value and data flags.
        Message format:
        {
            'detector-gas-analog-safe-gas-array': [...],
            'detector-gas-detector-type-safe-gas-array': [...],
            'raw_integration_data': [...],
        }
        'detector-gas-analog-safe-gas-array':
        - Initialised to data values present in addresses 1-40 of the iMAC
        - For detected GG2 modules, the analog value is replaced by the gas scaled value
        'detector-gas-detector-type-safe-gas-array':
        - Initialised to 0 for the addresses 1-40 of the iMAC
        - Reports the type of detector for a GG2 module or if the module is an AIM module. This value is dictated by the
        analog_conversion enum located at pyaware/protocol/imac2/modules.py on the Gasguard2 class.
        'raw_integration_data':
        - Raw IMAC data for each address
        """
        # Initialise the response.
        resp = {
            "detector-gas-analog-safe-gas-array": [0] * 60,
            "detector-gas-detector-type-safe-gas-array": [0] * 60,
            "raw-integration-data": self.current_state["raw-integration-data"],
        }
        # Special case AIM module detector type value
        AIM_DETECTOR_TYPE = 99
        for dev in self.modules.values():
            try:
                if dev.module_type == "imac-module-gg2":
                    if 41 <= dev.current_state["address-analog"] <= 80:
                        # Set the gas values
                        resp["detector-gas-analog-safe-gas-array"][
                            dev.current_state["address-analog"] - 41
                        ] = dev.current_state.get("detector-gas-value", 0)
                        # Set the sensor type
                        resp["detector-gas-detector-type-safe-gas-array"][
                            dev.current_state["address-analog"] - 41
                        ] = dev.current_state.get("detector-type", 0)
                    elif 161 <= dev.current_state["address-analog"] <= 180:
                        # Set the gas values
                        resp["detector-gas-analog-safe-gas-array"][
                            dev.current_state["address-analog"] - 161 + 40
                        ] = dev.current_state.get("detector-gas-value", 0)
                        # Set the sensor type
                        resp["detector-gas-detector-type-safe-gas-array"][
                            dev.current_state["address-analog"] - 161 + 40
                        ] = dev.current_state.get("detector-type", 0)
                elif dev.module_type == "imac-module-aim":
                    if 41 <= dev.current_state["address-analog"] <= 80:
                        # Set the type to AIM module
                        resp["detector-gas-detector-type-safe-gas-array"][
                            dev.current_state["address-analog"] - 41
                        ] = AIM_DETECTOR_TYPE
                    elif 161 <= dev.current_state["address-analog"] <= 180:
                        # Set the type to AIM module
                        resp["detector-gas-detector-type-safe-gas-array"][
                            dev.current_state["address-analog"] - 161 + 40
                        ] = AIM_DETECTOR_TYPE

            except KeyError:
                # Current state value not found for the module
                pass
            except BaseException as e:
                log.exception(e)
                pass

        events.publish(
            f"trigger_send",
            data=resp,
            meta=self.dict(),
            timestamp=datetime.utcnow(),
            topic_type="safe-gas",
            device_id=self.device_id,
        ),

    def update_module_current_state(self, module_data: dict):
        for serial, data in module_data.items():
            self.modules[serial].update_current_state(data)

    @events.subscribe(topic="boundary_enable/{id}")
    async def boundary_enable(self, data):
        """
        :param data: 40 bit sequence in an array corresponding to detectors 1-40
        :param timestamp:
        :return:
        """
        if len(data) != 40:
            raise ValueError
        addr_map = AddressMapUint16()
        addr_map[0x520:0x523] = 0, 0, 0
        for index, bit in enumerate(data):
            address = 0x520 + index // 16
            addr_map[address] |= bit << (index % 16)
        await self.protocol.write(0x520, *addr_map[0x520:0x523])

    @events.subscribe(topic="remote_bypass_gg2")
    async def remote_bypass_gg2(self, logical_address, value):
        """
        :param data: Dictionary, {"address": 1-40, "value": False or True}
        :return:
        """
        index = logical_address - 1
        address = 0x527 + index // 16
        bit = index % 16
        await self.protocol.write_bit(address, bit, value)
        await self.protocol.wait_on_bit(address, bit, check_to=value, timeout=2)

    @events.subscribe(topic="remote_bypass_rts")
    async def remote_bypass_rts(self, logical_address, value):
        """
        :param data: Dictionary, {"address": 1-12, "value": False or True}
        :return:
        """
        await self.protocol.write_bit(0x52A, logical_address - 1, value)
        await self.protocol.wait_on_bit(
            0x52A, logical_address - 1, check_to=value, timeout=2
        )

    @events.subscribe(topic="plc_trip_reset")
    async def plc_trip_reset(self):
        await self.protocol.write_bit(0x526, 15, 0)
        # Sleep for 500ms
        await asyncio.sleep(0.500)
        await self.protocol.write_bit(0x526, 15, 1)

    @events.subscribe(topic="trip_reset")
    async def trip_reset(self):
        await self.protocol.write(0x52C, 0)
        # Sleep for 500ms
        await asyncio.sleep(0.500)
        await self.protocol.write(0x52C, 0xA5)

    @events.subscribe(topic="imac_module_status")
    async def process_module_status_diff(self, data, timestamp):
        try:
            diff = {
                index: status
                for index, status in enumerate(data["address-status"])
                if status != self.current_state["address-status"][index]
            }
            if diff:
                self.current_state.update(data)
                events.publish(
                    "imac_discover_addresses", data=diff, timestamp=timestamp
                )
        except KeyError:
            # This is the first read, discover the full system
            self.current_state.update(data)
            events.publish("imac_discover_system")
        events.publish("imac_controller_data", data=data, timestamp=timestamp)

    @events.subscribe(topic="imac_discover_system")
    async def auto_discover_system(self):
        """
        Does a full system roll coll
        :return:
        """
        try:
            async with self.auto_discover_lock:
                log.info(f"Roll call System Start")
                online_addresses = {
                    address
                    for address, status in enumerate(
                        self.current_state["address-status"]
                    )
                    if status in {ModuleStatus.ONLINE}
                }
                # Check for RTSs based on schema
                for address in online_addresses:
                    schema = self.address_schema_match(address)
                    if "rts-config" in schema["name"]:
                        # Do an address discover of the RTS addresses and ensure that they are RTSs
                        async for mod in self.discover_at_address(
                            address, ModuleStatus.ONLINE
                        ):
                            log.info(f"Module found in RTS schema location: {mod}")
                # Roll call the remaining modules
                async for roll_module in self.protocol.roll_call():
                    # Find the discovered modules
                    mod = self.protocol.decode_roll_call_single(roll_module)
                    log.info(f"Roll call System: {mod}")
                    await self.update_devices([mod])
        except asyncio.CancelledError:
            log.info("Shutting down system roll call")
            return
        except BaseException as e:
            if pyaware.evt_stop.is_set():
                log.info("Shutting down autodiscover")
                return
            log.exception(e)
            events.publish("imac_discover_system")

    @events.subscribe(topic="imac_discover_addresses")
    async def auto_discover_modules(self, data, **kwargs):
        """
        Auto discovers modules based on the address status.
        Gets the modules to roll call based on address status.
        Failed roll calls are repeated with the auto discover lock still held.
        Devices that are returned are queried for their other addresses and removed from the roll call queue if the
        address is not clashed
        :param data:
        :param kwargs:
        :return:
        """
        async with self.auto_discover_lock:
            online_queue = {
                address
                for address, status in data.items()
                if status == ModuleStatus.ONLINE or address == 0
            }
            clash_queue = {
                address
                for address, status in data.items()
                if status == ModuleStatus.CLASH
            }
            system_queue = {
                address
                for address, status in data.items()
                if status in {ModuleStatus.SYSTEM, ModuleStatus.SYSTEM_ONLINE}
            }
            offline_queue = {
                address
                for address, status in data.items()
                if status in {ModuleStatus.OFFLINE}
            }
            modules = set([])
            while True:
                if online_queue:
                    address = min(online_queue)
                elif clash_queue:
                    address = min(clash_queue)
                elif system_queue:
                    address = min(system_queue)
                elif offline_queue:
                    address = min(offline_queue)
                else:
                    break
                status = data[address]
                try:
                    async for imac_mod in self.discover_at_address(address, status):
                        # Find the discovered modules
                        modules.add(imac_mod)
                        await imac_mod.find_missing_starting_data()
                except asyncio.CancelledError:
                    log.info("Shutting down autodiscover")
                    return
                except BaseException as e:
                    if pyaware.evt_stop.is_set():
                        log.info("Shutting down autodiscover")
                        return
                    log.exception(e)
                    events.publish(
                        "imac_discover_addresses", data={address: data[address]}
                    )
                    await asyncio.sleep(1)

                clash_queue.discard(address)
                system_queue.discard(address)
                online_queue.discard(address)
                offline_queue.discard(address)
                await self.delete_missing_modules_at_address(modules, address)

    async def discover_at_address(
        self, address: int, status: ModuleStatus = ModuleStatus.UNKNOWN
    ):
        roll_module = None
        log.info(f"Roll call address start: {address}")
        roll_calls = await self.protocol.roll_call_force(address)
        for roll_module in roll_calls:
            mod = self.protocol.decode_roll_call_single(roll_module)
            log.info(f"Roll call: Address: {address}, {mod}")
            await self.update_devices([mod])
            yield self.modules[mod["dev_id"]]
        if roll_module is not None:
            return
        # Check for RTSs based on schema if no module is found at this address
        schema = self.address_schema_match(address)
        if self.address_schema_match_addresses_online(
            address, "rts", self.current_state["address-status"]
        ):
            rts_number = address - schema["range"][0] + 1
            dev_id = f"rts-{self.current_state['master-fieldbus-number']}-{rts_number}"
            mod = {"dev_id": dev_id, "imac_address": address, "module_type": "rts"}
            log.info(f"Roll call: Address: {address}, {mod}")
            await self.update_devices([mod])
            yield self.modules[mod["dev_id"]]

    def address_schema_violation(
        self, address, imac_module_roll: typing.List[dict]
    ) -> list:
        """
        Checks the loaded schema to determine if a address violation has occured
        :param address:
        :param imac_module_roll:
        :return:
        """
        schema = self.address_schema_match(address)
        violations = []
        for imac_module in imac_module_roll:
            # Enforce schema
            if self._address_schema_violation(schema, imac_module):
                log.info(
                    f"Schema Violation: Address: {address}, {imac_module['dev_id']}:"
                    f"{imac_module['module_type']}"
                )
                violations.append(imac_module)
        return violations

    def _address_schema_violation(self, schema, imac_module_roll: dict) -> bool:
        if schema.get("allowed_modules") is not None:
            return imac_module_roll["module_type"] not in schema["allowed_modules"]
        return False

    def address_status_schema_violation(self, address, status: ModuleStatus) -> bool:
        """
        Checks the loaded schema to determine if a address violation has occured
        :param address:
        :param imac_module_roll:
        :return:
        """
        schema = self.address_schema_match(address)
        if schema.get("allowed_statuses") is not None:
            return status.name not in schema["allowed_statuses"]
        return False

    def address_schema_match(self, address) -> dict:
        for schema in self.schema.get("address", []):
            if address in range(*schema["range"]):
                return schema

    def address_schema_match_offset(self, address) -> int:
        schema = self.address_schema_match(address)
        return address - schema.get("range", [0])[0]

    def address_schema_match_by_name(self, name) -> dict:
        for schema in self.schema.get("address", []):
            if schema.get("name") == name:
                return schema
        raise ValueError("No Schema Match")

    def schema_relation_match(self, name: str) -> dict:
        for relation in self.schema.get("address-relations", []):
            try:
                if relation["name"] == name:
                    return relation
            except KeyError:
                pass
        return {}

    def address_schema_match_addresses_online(
        self, address: int, name: str, address_statuses: typing.List[ModuleStatus]
    ) -> bool:
        """
        Return if all the addresses are online for the schema matching the given address
        :param address: Address of the module to check against
        :param name: The schema relational name for all the schema matches. eg. rts would match rts-config-1,
        rts-config-2 and rts-config-3
        :param address_statuses: The address statuses read from the imac
        :return: True if all addresses that match the input address are online
        """
        matched_address_status = []
        relation = self.schema_relation_match(name)
        try:
            if self.address_schema_match(address)["name"] not in relation["addresses"]:
                return False
        except IndexError:
            return False
        offset = self.address_schema_match_offset(address)
        for name in relation.get("addresses", []):
            schema_range = self.address_schema_match_by_name(name).get("range", [0])[0]
            matched_address_status.append(address_statuses[schema_range + offset])

        return all([addr == ModuleStatus.ONLINE for addr in matched_address_status])

    @events.subscribe(topic="clear_address")
    async def clear_status_at_address(self, data):
        await self.protocol.write_bit(data + 0x100, 0, 0)

    def remove_device_from_schedule(self, dev_id: str):
        remove_items = {k for k in self.schedule_reads if k.split("::")[0] == dev_id}
        for k in remove_items:
            del self.schedule_reads[k]

    def update_store_state(self, parameters: dict):
        """
        Update the state the module has represented in the cache database
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.store_state.update(parameters)

    def update_send_state(self, parameters: dict):
        """
        Update the state used the module has represented from queued mqtt messages
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.send_state.update(parameters)

    def update_event_state(self, parameters: dict):
        """
        Update the state used the module has represented from queued mqtt messages
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.event_state.update(parameters)

    def update_current_state(self, parameters: dict):
        """
        Update the state used to run diff module data against
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.current_state.update(parameters)

    @events.subscribe(topic="sync_rtc")
    async def rtc_sync(self, timestamp: int):
        """
        Writes to NVM 13 and 14 the timestamp for the real time clock
        This is Ampcontrol Epoch of 01/01/2000 with high byte in NVM 13 and low byte in NVM 14
        This will be an integer sent from the master which should have the necessary conversions to Ampcontrol Epoch
        already implemented.
        The timestamp is offset by the amount of time setting up so that the time written is closer to accurate.
        Note that there will be other time offsets due to communication times and loop and the fact that Ampcontrol
        Epoch has a resolution of seconds.
        :return:
        """
        start = time.time()
        await self.protocol.write(0x52D, 0, 0)
        await asyncio.sleep(3)
        values = struct.unpack(
            ">HH", struct.pack(">I", round(timestamp + time.time() - start))
        )
        await self.protocol.write(0x52D, *values)

    def identify(self):
        return self.dict()

    def dict(self):
        return {"type": self.module_type, "serial": self.serial_number}

    async def delete_missing_modules_at_address(
        self, modules: typing.Set[ImacModule], address: int
    ):
        """
        Determines which modules are currently missing from the address that was roll called.
        Finds the difference between what modules we expect at that address vs what was roll called.
        Each ImacModule should have an implementation of detecting if it is offline based on an address-status parsed
        :param modules:
        :param address:
        :return:
        """
        expected_modules = {
            x
            for x in self.modules.values()
            if address in x.identify_rollcall_addresses().values()
        }
        missing_modules = expected_modules.difference(modules)
        modules_to_delete = [
            x.current_state["dev-id"]
            for x in missing_modules
            if not x.any_addresses_online(self.current_state["address-status"])
        ]
        if modules_to_delete:
            await self.remove_devices(modules_to_delete)
