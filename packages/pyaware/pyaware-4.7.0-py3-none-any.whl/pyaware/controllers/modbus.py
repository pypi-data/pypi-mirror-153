from __future__ import annotations

import asyncio
import logging
import typing
from datetime import datetime
from pathlib import Path

import pyaware.aggregations
import pyaware.commands
import pyaware.config
import pyaware.data_types
import pyaware.data_types.modbus
import pyaware.meta
import pyaware.parameters
import pyaware.transformations
import pyaware.triggers
from pyaware import events
from pyaware import watchdog
from pyaware.controllers import Controller
from pyaware.controllers.commands import SetParameters, GetParameters
from pyaware.mqtt.models import TopologyChildren
from pyaware.store import memory_storage

numeric = typing.Union[int, float]
log = logging.getLogger(__name__)
if typing.TYPE_CHECKING:
    from pyaware.parameters import Parameter


@events.enable
class ModbusDevice(Controller):
    name = "Modbus Device"
    module_type = "modbus-device"

    def __init__(
        self,
        client,
        device_id: str,
        config: Path,
        unit=0,
        address_shift=0,
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
        self.unit = unit
        self.config = pyaware.config.load_yaml_config(config)
        self.address_shift = address_shift
        self.parameter_metadata = pyaware.meta.parse_metadata(self.config["parameters"])
        self.parameters = pyaware.parameters.parse_parameters(
            self.config["parameters"], {}
        )
        self.sequences = {}
        self.commands = pyaware.commands.Commands(
            {
                "set-parameters": [SetParameters()],
                "get-parameters": [GetParameters()],
            },
            meta_kwargs={"controller": self},
            device_id=device_id,
        )

        if address_shift:
            for param in self.parameters.values():
                try:
                    param.form.address += address_shift
                except (TypeError, AttributeError):
                    continue
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

        self.read_handles = {
            "holding": self.client.read_holding_registers,
            "input": self.client.read_input_registers,
            "discrete": self.client.read_discrete_inputs,
            "coils": self.client.read_coils,
        }
        self.write_handles = {
            "holding": self.client.write_multiple_registers,
            "coils": self.client.write_multiple_coils,
        }
        self.update_parameter_handlers()

    def init(self):
        # Initialise subscriptions
        events.subscribe(self.process_data, topic=f"process_data/{id(self)}")
        events.subscribe(self.process_write, topic=f"process_write/{id(self)}")
        for name, source_config in self.config["sources"].items():
            if source_config.get("type", "poll") == "poll":
                asyncio.create_task(
                    self.trigger_poll(name, address_shift=self.address_shift)
                )
        self.setup_watchdogs()

    def setup_watchdogs(self):
        dog_comms = watchdog.WatchDog(
            heartbeat_time=5,
            success_cbf=lambda: events.publish(
                f"process_data/{id(self)}",
                data={"modbus-comms-status": True},
                timestamp=datetime.utcnow(),
                device_id=self.device_id,
            ),
            failure_cbf=lambda: events.publish(
                f"process_data/{id(self)}",
                data={"modbus-comms-status": False},
                timestamp=datetime.utcnow(),
                device_id=self.device_id,
            ),
        )
        watchdog.manager.add(f"modbus_comms_status_{id(self)}", dog_comms)
        try:
            self.client.protocol_made_connection = watchdog.watch(
                f"modbus_comms_status_{id(self)}"
            )(self.client.protocol_made_connection)
        except AttributeError:
            pass
        try:
            self.read_registers = watchdog.watch(f"modbus_comms_status_{id(self)}")(
                self.read_registers
            )
        except AttributeError:
            pass
        try:
            self.client.protocol_lost_connection = watchdog.watch_starve(
                f"modbus_comms_status_{id(self)}"
            )(self.client.protocol_lost_connection)
        except AttributeError:
            pass
        dog_comms.start(start_fed=False)

    def get_modbus_blocks(self, source, address_shift):
        if address_shift:
            modbus_blocks = []
            for start, end in self.config["sources"][source]["blocks"]:
                modbus_blocks.append([start + address_shift, end + address_shift])
        else:
            return self.config["sources"][source]["blocks"]
        return modbus_blocks

    async def trigger_poll(self, source, address_shift=0, poll_interval=None):
        modbus_blocks = self.get_modbus_blocks(source, address_shift)
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
        register_type = self.config["sources"][source].get("handle", "holding")
        read_handle = self.read_handles[register_type]

        while True:
            if pyaware.evt_stop.is_set():
                log.info(f"Closing modbus device {self.device_id} polling")
                return
            try:
                start = loop.time()
                # If connection is interrupted stops reading and waits for connection to be reestablished.
                if not self.client.connected.is_set():
                    await self.client.connected.wait()
                await self.poll_pipeline(modbus_blocks, source, read_handle)
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning(
                        f"Modbus device {self.device_id} cancelled without stop signal"
                    )
                    continue
            except asyncio.TimeoutError as e:
                log.error(repr(e))
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)
            sleep_time = start - loop.time() + poll_interval
            if sleep_time > 0:
                await asyncio.sleep(start - loop.time() + poll_interval)

    async def poll_pipeline(self, blocks, source, read_handle):
        addr_map = pyaware.data_types.modbus.AddressMapUint16()
        for start, end in blocks:
            count = len(range(start, end))
            addr_map.merge(await self.read_registers(read_handle, start, count))
        timestamp = datetime.utcnow()
        if timestamp is None:
            timestamp = datetime.utcnow()
        device_data = {}
        for k, v in self.parameters.items():
            if v.source == source:
                try:
                    device_data.update(v.decode(addr_map))
                except KeyError:
                    pass
        await events.publish(
            f"process_data/{id(self)}",
            data=device_data,
            timestamp=timestamp,
            device_id=self.device_id,
        ).all()
        self.current_state.update(device_data)

    async def read_registers(
        self, read_handle: typing.Callable, address: int, count: int
    ):
        f"""
        Read modbus registers
        :param read_handle:
        :param address:
        :param count:
        :return:
        """
        addr_map = pyaware.data_types.modbus.AddressMapUint16()
        addr_map[address : address + count] = await read_handle(
            address, count, unit=self.unit
        )
        return addr_map

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
        Processes write to a modbus device.

        :param register_type: Type of register to be written to. i.e. "holding" OR "coils".
        :param data: Data as a dictionary in the format {"param1": data, "param2": data, ...} to be written.
        """
        await self.set_parameters(data)

    async def set_parameter(self, parameter: str, value: typing.Any):
        """
        Directly sets the parameter using the data type encode method. Assumes that all validation checks are completed.
        :param parameter: Parameter id to get from self.parameters
        :param value: The value to encode
        :return:
        """
        source = self.config["parameters"]["source"]
        register_type = self.config["sources"][source].get("handle", "holding")
        write_handle = self.write_handles[register_type]
        await write_handle(
            self.parameters[parameter].address,
            self.parameters[parameter].encode(value),
            unit=self.unit,
        )

    async def get_parameter(
        self, parameter: str, strict: bool = True
    ) -> typing.Dict[str, typing.Any]:
        """
        Directly gets the parameter using the data type decode method. Assumes that all validation checks are completed.
        :param parameter: Parameter id to get from self.parameters
        :param strict:
        True: Only return the parameter requested
        False: Include parameters read from the same read. Has performance penalty.
        :return: Return the value of the parameter read
        """
        source = self.config["parameters"]["source"]
        register_type = self.config["sources"][source].get("handle", "holding")
        read_handle = self.read_handles[register_type]
        data = await read_handle(self.parameters[parameter].address)
        if strict:
            return self.parameters[parameter].decode(data)
        else:
            resp = {}
            for param in self.parameters.values():
                resp.update(param.decode(data))
            return resp

    async def set_parameters(self, parameters: typing.Dict[str, typing.Any]):
        """
        Directly sets the parameters using the data type encode method. Assumes that all validation checks are completed
        and ignores the write sequencing of the parameter. Care should be used when setting parameters that share a
        write block as any parameters not included will not have default values. In the case of modbus, this will erase
        any other parameters present in the register if not included.
        :param data: Key value pairs of the parameters to set
        :return:
        """
        # Initialise write handles for registers
        addr_maps = {
            handle: pyaware.data_types.modbus.AddressMapUint16()
            for handle in self.write_handles
        }
        for param_name, val in parameters.items():
            # Format data to encode differently if its ParamBits
            if type(self.parameters[param_name]) == pyaware.data_types.modbus.ParamBits:
                data_to_encode = val
            else:
                data_to_encode = {param_name: val}
            try:
                # Device specific register type of each parameter
                # In this case "coils" or "holding"
                source = self.config["parameters"][param_name]["source"]
                register_type = self.config["sources"][source].get("handle", "holding")
                # Write to the right register address map
                addr_map = addr_maps[register_type]
                self.parameters[param_name].encode(data_to_encode, addr_map)
            except KeyError:
                log.warning(
                    f"Invalid device config definition for {self.device_id}. Cannot write, skipping..."
                )
        # Gets contiguous address blocks
        # In the form: blocks = [[start1, end1], [start2, end2], ...]
        for register_type, addr_map in addr_maps.items():
            # Fetches write handle for each addr map.
            write_handle = self.write_handles[register_type]
            blocks = []
            index = 0
            sorted_addr_map = sorted(addr_map._buf.items())
            for addr, val in sorted_addr_map:
                if len(blocks) != (index + 1):
                    blocks.append([addr, addr])
                if (addr + 1) not in addr_map._buf.keys():
                    blocks[index][1] = addr
                    index += 1
            # Writes block to the modbus device
            for start, end in blocks:
                values = addr_map[start : end + 1]
                await self.write_registers(write_handle, start, values)

    async def get_parameters(self, parameters: set) -> typing.Dict[str, typing.Any]:
        """
        Directly gets the parameter using the data type decode method. Assumes that all validation checks are completed.
        :param keys: Set of keys to read
        :return: Return the value of the parameter read
        """

    async def write_parameters(self, data: dict):
        """
        Write parameters to the appropriate modbus registers.
        This is done by a sequence which can be defined in the configuration file.
        A standard parameter would default to a configuration of:
        ```
        write:
          - type: write
        ```
        A Param mask would default to a configuration of:
        ```
        write:
          - type: read
          - type: write
        ```
        which would read the register first to ensure that only the appropriate bits were modified in the register.

        An example of a parameter that would sequence as a negative pulse. This would have to be coded in the
        parameter's configuration.
        ```write:
        - type: write_value
          value: false
        - type: wait
          value: 0.2
        - type: write_value
          value: true
        ```

        NOTE: Writing many parameters might take longer than expected due to parameter writes being written individually
        and conforming to the write sequence for a parameter.
        NOTE: This is not compatible with ParamBits. They should instead have an individual ParamBit definition for
        writing parameters. This is because ParamBits does not exist in the parameters field but as an aggregate.
        Instead of looping through all the parameters it needs a valid key in the parameters dict.
        :param data: Dictionary of form parameter: value
        :return:
        """
        assert not set(data).difference(self.parameters)
        for key in data:
            await self.parameters[key].write(data)

    async def read_parameters(self, parameters: set) -> typing.Dict[str, typing.Any]:
        """
        Read parameters through the controller process flow. This will run through read process triggers and return the
        key value pairs of the data read
        :param parameters:
        :return: dictionary of parameters read
        """
        ret_val = {}
        params = self.parameters.keys() & parameters
        for key in params:
            if key in ret_val:
                continue
            ret_val.update(await self.parameters[key].read())
        return ret_val

    async def write_registers(
        self, write_handle: typing.Callable, address: int, values: typing.List[int]
    ):
        f"""
        Write to modbus registers
        :param write_handle:
        :param address:
        :param values:
        :return:
        """
        await write_handle(address, *values, unit=self.unit)

    def identify(self):
        response = TopologyChildren(
            values={},
            type=self.module_type,
            serial=self.device_id,
            children=[],
        )
        return response

    def dict(self):
        response = {"type": self.module_type}
        return response

    def update_parameter_handlers(self):
        """
        Loops through all the parameters and sets the read and write handles based on the parameter relationships with
        each other and the data source
        :return:
        """
        for param in self.parameters.values():
            if param.parent:
                continue
            self._set_param_handles(param)

    def _set_param_handles(self, param: Parameter):
        # Only set the parent parameter handlers
        addresses = self._get_param_address(param)

        try:
            register_type = self.config["sources"][param.source].get(
                "handle", "holding"
            )
        except KeyError:
            log.warning(f"Missing source definition for {param}")
            return
        # Assumes param group has contiguous values
        start = min(addresses)
        end = max(addresses)
        count = end - start + 1
        # TODO work for non-contiguous values
        assert len(addresses) == end - start + 1
        write_handle = self.write_handles.get(register_type)
        read_handle = self.read_handles.get(register_type)

        if write_handle:

            async def write(data: pyaware.data_types.modbus.AddressMapUint16):
                """
                Writes the data for the parameter to the appropriate register
                :param data:
                :return:
                """
                await self.write_registers(write_handle, start, data[start : end + 1])

            param.writer.handle = write
            param.writer.encoder_factory = pyaware.data_types.modbus.AddressMapUint16

        if read_handle:

            async def read() -> pyaware.data_types.modbus.AddressMapUint16:
                return await self.read_registers(read_handle, start, count)

            param.reader.handle = read

    def _get_param_address(self, param: Parameter) -> set:
        addresses = set([])
        try:
            addresses.update(param.form.get_addresses())
        except AttributeError:
            pass
        for child in param.children:
            addresses.update(self._get_param_address(child))
        return addresses
