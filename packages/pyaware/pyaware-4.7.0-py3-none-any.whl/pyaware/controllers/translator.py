import typing
import datetime

import pyaware
import pyaware.data_types
import pyaware.data_types.modbus
import pyaware.transformations
from pyaware import log, events


@events.enable
class Translator:
    """
    Device/Server Translator. Takes information from config to translate data from one/multiple device(s) to
    one/multiple server(s).

    Each server will have a list of devices, registers and register types as well as a list of data transformation
    functions specific to each server -> device relationship.
    Example Config (yaml format):
        server-translation:
            server1:
                devices:
                    dev1:
                        transformations:
                            - func1:
                                definition:
                                    ...
                            -func2:
                                definition:
                                    ...
                    dev2:
                        ...
                    ...
                registers:
                    holding:
                        param1:
                        ...
                    ...
            server2:
                ...

    Each device will have a list of servers and a list of data transformation functions specific to each device ->
    server relationship.
    Example Config (yaml format):
        device-translation:
            dev1:
                servers:
                    server1:
                        transformations:
                            - func1:
                                definition:
                                    ...
                            -func2:
                                definition:
                                    ...
                    server2:
                        ...
                    ...
            ...

    NOTE: Each device and server require access to their reference objects parsed in communications.
    This needs to be defined in gateway.yaml under ref_translation.
    Example Config (yaml format):
      - name: translator
        type: translator
        params:
          config: {type: ref_translation_config, value: translator.yaml}
          devices: {type: ref_translation, value: [dev1, dev2, ...]}
          servers: {type: ref_translation, value: [server1, server2, ...]}
    """

    def __init__(self, config, devices, servers):
        self.config = pyaware.config.load_yaml_config(config)

        try:
            # Initialise server translations from config
            self.servers = {k: p for k, p in self.config["server-translation"].items()}
            for server, items in self.servers.items():
                registers = items["registers"]
                server_dev = items["devices"]
                for reg, params in registers.items():
                    registers[reg].update(
                        pyaware.data_types.parse_data_types(params, {})
                    )
                try:
                    self.servers[server]["ref"] = servers[server]
                    server_id = id(servers[server])
                    events.subscribe(
                        self.process_server_data, topic=f"device_update/{server_id}"
                    )
                except KeyError:
                    log.warning(
                        f"Server {server} does not have a reference object defined, "
                        f"skipping this device for translation."
                    )
                    pass
                for device, params in server_dev.items():
                    server_dev[device].update(
                        {
                            "transformations": pyaware.transformations.build_from_reference(
                                params
                            )
                        }
                    )

            # Initialise device translations from config
            self.devices = {k: p for k, p in self.config["device-translation"].items()}
            for device, items in self.devices.items():
                servers = items["servers"]
                try:
                    self.devices[device]["ref"] = devices[device]
                    dev_id = id(devices[device])
                    events.subscribe(
                        self.process_device_data, topic=f"process_data/{dev_id}"
                    )
                except KeyError:
                    log.warning(
                        f"Device {device} does not have a reference object defined, "
                        f"skipping this device for translation."
                    )
                    pass
                for server, params in servers.items():
                    servers[server].update(
                        {
                            "transformations": pyaware.transformations.build_from_reference(
                                params
                            )
                        }
                    )
        except KeyError:
            log.warning("Invalid translation config file.")
            raise

    def process_device_data(
        self,
        data: typing.Dict[str, int],
        timestamp: datetime.datetime,
        device_id: str,
        gateway: str = "",
    ):
        """
        Processes data received from a device and sends transformed result to the correct locations.

        :param data: Device data to be processed in the format -> {"param1": data, "param2": data, ...}
        :param timestamp: Timestamp of data processing
        :param device_id: Device ID that the data came from
        """
        # Checks if the server mapping exists for the device polled
        try:
            # If no servers to publish to return
            servers_to_publish = self.devices[device_id]["servers"].keys()
        except KeyError:
            return

        # Apply Transformations to data
        for server_id in servers_to_publish:
            transformations = self.servers[server_id]["devices"][device_id][
                "transformations"
            ]
            data = pyaware.transformations.transform(data, transformations)
            for reg, server_params in self.servers[server_id]["registers"].items():
                # Returns the encoded address map for each parameter
                addr_map = pyaware.data_types.modbus.AddressMapUint16()
                for param, value in data.items():
                    try:
                        # TODO: Make this float to int transform more robust, will lose accuracy this way
                        if type(value) == float:
                            value = int(value)
                        if (
                            type(server_params[param])
                            == pyaware.data_types.modbus.ParamBits
                        ):
                            data_to_encode = value
                        else:
                            data_to_encode = {param: value}
                        server_params[param].encode(data_to_encode, addr_map)
                    except KeyError:
                        pass
                server_id = id(self.servers[server_id]["ref"])
                events.publish(
                    f"update_server/{server_id}", addr_map=addr_map, register=reg
                )

    def process_server_data(
        self, start_addr: int, values: typing.List[int], server_id: str
    ):
        """
        Processes data received from a server and sends transformed result to the correct locations.

        :param start_addr: Start address of data
        :param values: Values as an array of integers starting at start_addr
        :param server_id: Server ID that the data came from
        """
        try:
            # If no devices to publish return
            devices_to_publish = self.servers[server_id]["devices"].keys()
        except KeyError:
            return

        addr_map = pyaware.data_types.modbus.AddressMapUint16(
            {start_addr + index: v for index, v in enumerate(values)}
        )
        for reg, params in self.servers[server_id]["registers"].items():
            device_data = {}
            for param_id, param in params.items():
                try:
                    device_data.update(param.decode(addr_map))
                except KeyError:
                    continue

            # Apply Transformations
            for dev_id in devices_to_publish:
                transformations = self.devices[dev_id]["servers"][server_id][
                    "transformations"
                ]
                device_data = pyaware.transformations.transform(
                    device_data, transformations
                )
                try:
                    device_parameters = self.devices[dev_id]["ref"].parameters
                except (KeyError, AttributeError):
                    continue
                data_to_send = {
                    k: v for k, v in device_data.items() if k in device_parameters
                }
                if data_to_send:
                    dev_id = id(self.devices[dev_id]["ref"])
                    events.publish(
                        f"process_write/{dev_id}", register_type=reg, data=data_to_send
                    )
