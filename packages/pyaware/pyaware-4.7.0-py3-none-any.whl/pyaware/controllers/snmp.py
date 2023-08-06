import asyncio
import puresnmp
import puresnmp.types
import pyaware
import pyaware.aggregations
import pyaware.commands
import pyaware.data_types.snmp
import pyaware.parameters
import pyaware.transformations
import pyaware.triggers
from datetime import datetime
from pathlib import Path
from pyaware import events
from pyaware import log
from pyaware.controllers import Controller
from pyaware.controllers.commands import SetParameters, GetParameters
from pyaware.parameters import Parameter
from pyaware.store import memory_storage
from typing import List, Dict, Union, Optional, Any, Set, TYPE_CHECKING

numeric = Union[int, float]

if TYPE_CHECKING:
    import puresnmp.typevars


@events.enable
class SNMPDevice(Controller):
    name = "SNMP Device"
    module_type = "snmp-device"

    def __init__(
        self,
        ip_address: str,
        community_string: str,
        device_id: str,
        config: Path,
        poll_intervals: Optional[Dict[str, numeric]] = None,
        port: int = 161,
    ):
        self.device_id = device_id
        self.ip_address = ip_address
        self.community_string = community_string
        self.port = port
        if poll_intervals is None:
            self.poll_intervals = {}
        else:
            self.poll_intervals = poll_intervals
        self.store_state = {}
        self.send_state = {}
        self.event_state = {}
        self.current_state = {}
        self.config = pyaware.config.load_yaml_config(config)
        self.parameters = pyaware.parameters.parse_parameters(
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
        self.commands = pyaware.commands.Commands(
            {
                "set-parameters": [SetParameters()],
                "get-parameters": [GetParameters()],
            },
            meta_kwargs={"controller": self},
            device_id=device_id,
        )
        self.update_parameter_handlers()

    def init(self):
        # Initialise read/write subscriptions.
        events.subscribe(self.process_data, topic=f"process_data/{id(self)}")
        events.subscribe(self.process_write, topic=f"process_write/{id(self)}")
        for name, source_config in self.config["sources"].items():
            if source_config.get("type", "poll") == "poll":
                asyncio.create_task(self.trigger_poll(name))

    async def trigger_poll(self, source: str, poll_interval: int = 5):
        """
        Trigger to begin polling data from the device at a set interval.

        :param source: The identifier of the source of polling. Typically included in device config.
        :param poll_interval: The interval to poll data from the device as an integer in seconds.
        """
        # Sets poll interval to value in device config.
        try:
            poll_interval = self.config["sources"][source]["poll_interval"]
        except KeyError:
            pass
        # Overwrites device config if poll intervals exists in gateway config
        try:
            poll_interval = self.poll_intervals[source]
        except KeyError:
            pass

        loop = asyncio.get_running_loop()
        start = loop.time()
        log.info(f"Starting poll pipeline for {self.device_id}")

        while True:
            if pyaware.evt_stop.is_set():
                log.info(f"Closing {self.name} {self.device_id} polling")
                return
            try:
                start = loop.time()
                await self.poll_pipeline(source)
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning(
                        f"{self.name} {self.device_id} cancelled without stop signal"
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

    async def poll_pipeline(self, source: str):
        """
        Pipeline to poll data from the device.

        :param source: The identifier of the source of polling. Typically included in device config.
        """
        timestamp = datetime.utcnow()
        device_data = {}
        for k, v in self.parameters.items():
            if v.source == source:
                try:
                    device_data.update(await v.read())
                except KeyError:
                    pass
        await events.publish(
            f"process_data/{id(self)}",
            data=device_data,
            timestamp=timestamp,
            device_id=self.device_id,
        ).all()
        self.current_state.update(device_data)

    async def process_data(
        self,
        data: Dict[str, puresnmp.typevars.PyType],
        timestamp: datetime,
        device_id: str,
    ):
        """
        Process data read from the device.

        :param data: Data read from the device in the form: {"parameter_name": DATA, ...}.
        :param timestamp: The timestamp of the data read as a datetime.
        :param device_id: The device identifier as a string.
        """
        # Setup data transformations
        transformed_data = pyaware.transformations.transform(data, self.transformations)
        # Gathers triggers from the data for storing, sending and performing events
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
            # Perform data store operations.
            memory_storage.update(store_data, topic=f"{self.device_id}")
            self.store_state.update(store_data)
        if send_data:
            # Perform data send operations.
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
            # Perform data event operations.
            for param, value in event_data.items():
                events.publish(
                    f"parameter_trigger/{self.device_id}/{param}",
                    data=next(iter(value.values())),
                    timestamp=timestamp,
                )
            self.event_state.update(event_data)
        return send_data

    async def process_write(self, data: Dict[str, puresnmp.typevars.PyType]):
        """
        Processes write to the SNMP device.

        :param data: Data as a dictionary in the format {"Parameter1": data, "Parameter2": data, ...}.
        """
        await self.set_parameters(data)

    async def set_parameter(
        self, parameter: str, value: puresnmp.typevars.PyType
    ) -> Dict[str, puresnmp.typevars.PyType]:
        """
        Directly sets the parameter using the data type encode method. Assumes that all validation checks are completed.

        :param parameter: Parameter id to get from self.parameters as a string.
        :param value: The value to write to the parameter as a PyType.
        :return: The data written to the parameter. This is in the form: {"OID1": DATA_WRITTEN}
        """
        encoded_data = {}
        self.parameters[parameter].encode({parameter: value}, encoded_data)
        return await self.write_multiple(encoded_data)

    async def get_parameter(
        self, parameter: str, strict: bool = True
    ) -> Dict[str, puresnmp.typevars.PyType]:
        """
        Directly gets the parameter using the data type decode method. Assumes that all validation checks are completed.

        :param parameter: Parameter id to get from self.parameters as a string.
        :param strict: True: Only return the parameter requested; False: Include parameters read from the same read. Has performance penalty.
        :return: Data read from the parameter as a dictionary in the form: {"parameter_name": DATA_TO_WRITE}
        """
        data = await self.read_multiple([self.parameters[parameter].form.oid])
        if strict:
            return self.parameters[parameter].decode(data)
        else:
            resp = {}
            for param in self.parameters.values():
                resp.update(param.decode(data))
            return resp

    async def set_parameters(
        self, parameters: Dict[str, puresnmp.typevars.PyType]
    ) -> Dict[str, puresnmp.typevars.PyType]:
        """
        Directly sets the parameters using the data type encode method. Assumes that all validation checks are completed
        and ignores the write sequencing of the parameter. Care should be used when setting parameters that share a
        write block as any parameters not included will not have default values. In the case of modbus, this will erase
        any other parameters present in the register if not included.

        :param parameters: The device data to write in the form: {"parameter_name": DATA_TO_WRITE, ...}
        :return: The data successfully written to the device. This is in the form: {"OID1": DATA_WRITTEN, "OID2": DATA_WRITTEN, ...}
        """
        encoded_data = {}
        for parameter, value in parameters.items():
            self.parameters[parameter].encode({parameter: value}, encoded_data)
        return await self.write_multiple(encoded_data)

    async def get_parameters(
        self, parameters: Set[str]
    ) -> Dict[str, puresnmp.typevars.PyType]:
        """
        Directly gets the parameter using the data type decode method. Assumes that all validation checks are completed.

        :param parameters: Set of parameters to read as strings. In the form: ["Parameter1", "Parameter2", ...]
        :return: Data read from the list of parameters as a dictionary in the form: {"parameter_name": DATA_TO_WRITE, ...}
        """
        ret_val = {}
        data = await self.read_multiple(list(parameters))
        for parameter in parameters:
            ret_val.update(self.parameters[parameter].decode(data))
        return ret_val

    async def write_parameters(self, data: Dict[str, puresnmp.typevars.PyType]):
        """
        Write parameters to the appropriate SNMP Object Ids(OIDs).
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

        :param data: The device data to write in the form: {"parameter_name": DATA_TO_WRITE, ...}
        """
        assert not set(data).difference(self.parameters)
        for key in data:
            await self.parameters[key].write(data)

    async def read_parameters(
        self, parameters: Set[str]
    ) -> Dict[str, puresnmp.typevars.PyType]:
        """
        Read parameters through the controller process flow. This will run through read process triggers and return the
        key value pairs of the data read

        :param parameters: Set of parameters to read as strings. In the form: ["Parameter1", "Parameter2", ...]
        :return: Data read from the list of parameters as a dictionary in the form: {"parameter_name": DATA, ...}
        """
        ret_val = {}
        params = self.parameters.keys() & parameters
        for key in params:
            if key in ret_val:
                continue
            ret_val.update(await self.parameters[key].read())
        return ret_val

    async def read_multiple(
        self, oids: List[str]
    ) -> Dict[str, puresnmp.typevars.PyType]:
        """
        Reads multiple snmp parameters using SNMP GET.

        :param oids: A list of SNMP Object IDs (OIDs) to read. This is in the form: ["OID1", "OID2", ...]
        :return: Data read from the device as dictionary in the form: {"OID1": OID1_DATA, "OID2": OID2_DATA, ...}
        """
        data = puresnmp.multiget(
            ip=self.ip_address, community=self.community_string, oids=oids
        )
        # The puresnmp library produces an ordered list in the same order as the input oids. This allows us to put the
        # data in a dictionary by iterating over the oid list.
        output = {}
        for index, oid in enumerate(oids):
            output[oid] = data[index]
        return output

    async def write_multiple(
        self, device_data: Dict[str, Any]
    ) -> Dict[str, puresnmp.typevars.PyType]:
        """
        Writes to multiple snmp parameters using SNMP SET.

        :param device_data: The device data to write in the form: {"parameter_name": DATA_TO_WRITE, ...}
        :return: Returns the data successfully written to the device. This is in the form: {"OID1": DATA_WRITTEN, "OID2": DATA_WRITTEN, ...}
        """
        # Maps the data from dictionaries to tuples.
        # The tuples are to be in the form [(parameter, value), ...].
        mappings = [(p, v) for p, v in device_data.items()]
        return puresnmp.multiset(
            ip=self.ip_address, community=self.community_string, mappings=mappings
        )

    def update_parameter_handlers(self):
        """
        Loops through all the parameters and sets the read and write handles based on the parameter relationships with
        each other and the data source. Ignores the child parameters and will only set the parent parameters.
        """
        for param in self.parameters.values():
            if param.parent:
                continue
            self._set_param_handles(param)

    def _set_param_handles(self, parameter: Parameter):
        """
        Sets the parameter read and write handles for the controller.

        :param parameter: The parameter to set the read/write handles for.
        """
        # Get the object id of the parameter
        oids = self._get_param_oid(parameter)

        async def read():
            """
            Reads data from the parameter using the appropriate read handle.
            """
            return await self.read_multiple(list(oids))

        async def write(data: Dict[str, puresnmp.typevars.PyType]):
            """
            Writes data for the parameter using the appropriate write handle.

            :param data: Data to write in the form: {"parameter_name": DATA_TO_WRITE, ...}
            """
            await self.write_multiple(data)

        # Sets the read and write handles and encoder factory.
        parameter.reader.handle = read
        parameter.writer.handle = write
        parameter.writer.encoder_factory = dict

    def _get_param_oid(self, parameter: Parameter) -> Set[str]:
        """
        Get the parameter Object IDs (OIDs) from each parameter in the parent/child tree.

        :param parameter: Parent parameter to start updating OIDs from as type PyAWARE Parameter.
        :return: Set of OIDs that belong to the parent and child parameters requested.
        """
        oids = set([])
        try:
            oids.update(parameter.form.get_oids())
        except AttributeError:
            pass
        for child in parameter.children:
            oids.update(self._get_param_oid(child))
        return oids

    def dict(self) -> Dict[str, str]:
        response = {"type": self.module_type}
        return response
