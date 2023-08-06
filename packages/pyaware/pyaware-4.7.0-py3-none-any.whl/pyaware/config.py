"""
This module is intended to parse configuration files and instantiate the necessary systems within pyaware.
"""
import asyncio
import logging
import platform
import typing
import uuid
from copy import deepcopy
from functools import lru_cache, partial
from pathlib import Path

import ruamel.yaml
import ifaddr

import pyaware
import pyaware.mqtt.config
import pyaware.mqtt.client

aware_path = Path("")
config_main_path = Path("")

log = logging.getLogger(__file__)


@lru_cache()
def load_file_raw(file_path: typing.Union[Path, str]) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()


@lru_cache()
def _yaml_load(data: str) -> dict:
    return ruamel.yaml.safe_load(data)


def yaml_load(data: bytes) -> dict:
    return deepcopy(_yaml_load(data.decode()))


def load_yaml_config(file_path: typing.Union[str, Path]) -> dict:
    """
    Load yaml config from a path
    :param file_path:
    :return: Loaded config
    """
    return yaml_load(load_file_raw(file_path))


def save_yaml_config(file_path: typing.Union[str, Path], config: dict):
    """
    Load config in its raw form and produce a dictionary, raw
    :param file_path:
    :return: Loaded config, raw data
    """
    with open(file_path, "w") as f:
        ruamel.yaml.dump(config, f, default_flow_style=False)
    load_file_raw.cache_clear()


def save_config_raw(file_path, config):
    """
    Load config in its raw form and produce a dictionary, raw
    :param file_path:
    :return: Loaded config, raw data
    """
    with open(file_path, "wb") as f:
        f.write(config)
    load_file_raw.cache_clear()


async def parse_modbus_rtu(port, **kwargs):
    """
    :param kwargs: All parameters required for instantiating the modbus client
    :return: Asyncronous modbus client
    """
    from aiomodbus.serial import ModbusSerialClient

    client = ModbusSerialClient(port, **kwargs)
    asyncio.get_event_loop().create_task(client.connect())
    return client


async def parse_modbus_tcp(host, **kwargs):
    """
    :param kwargs: All parameters required for instantiating the modbus client
    :return: Partial function that can be called to initiate the object and connection.
    """
    from aiomodbus.tcp import ModbusTCPClient

    client = ModbusTCPClient(host, **kwargs)
    asyncio.get_event_loop().create_task(client.connect())
    return client


async def parse_modbus_tcp_server(host, **kwargs):
    from pyaware.protocol.modbus import ModbusAsyncTcpServer

    server = ModbusAsyncTcpServer(host, **kwargs)
    asyncio.get_event_loop().create_task(server.start())
    return server


async def parse_translator(**kwargs):
    from pyaware.controllers.translator import Translator

    Translator(**kwargs)


async def parse_sp_pro(port: str, baudrate: int, parity: str, stopbits: int, **kwargs):
    try:
        from aiosppro.serial import SPPROSerialClient
    except ImportError:
        log.error(
            "Proprietary driver SPPro is specified in the config but is not correctly installed. "
            "Please acquire and install an appropriate version of aiosppro"
        )
        pyaware.stop()
        return

    client = SPPROSerialClient(
        port=port, baudrate=baudrate, parity=parity, stopbits=stopbits, **kwargs
    )
    asyncio.get_event_loop().create_task(client.connect())
    return client


async def parse_imac2_master_auto_detect(**kwargs):
    from pyaware.protocol.imac2.protocol import Imac2Protocol
    from pyaware.controllers.imac2.master import auto_detect

    proto = Imac2Protocol(
        client_ser=kwargs.get("client_ser"),
        client_eth=kwargs.get("client_eth"),
        unit=kwargs.get("unit", 1),
    )
    return await auto_detect(proto)


async def parse_modbus_device(**kwargs):
    from pyaware.controllers.modbus import ModbusDevice

    loop = asyncio.get_event_loop()
    partial_device = partial(ModbusDevice, **kwargs)
    return await loop.run_in_executor(None, partial_device)


async def parse_comap_device(**kwargs):
    from pyaware.controllers.comap import ComApInteliliteMRS16

    return ComApInteliliteMRS16(**kwargs)


async def parse_sp_pro_device(**kwargs):
    from pyaware.controllers.sp_pro import SPPRODevice

    return SPPRODevice(**kwargs)


async def parse_snmp_device(**kwargs):
    from pyaware.controllers.snmp import SNMPDevice

    return SNMPDevice(**kwargs)


async def parse_solar_cube(**kwargs):
    from pyaware.controllers.solar_cube import SolarCube

    return SolarCube(**kwargs)


async def parse_hbmqtt_gcp(**kwargs):
    raise DeprecationWarning(
        "Mqtt information should not be included in gateway configuration. Please remove"
    )


async def parse_hbmqtt_raw(device_id, **kwargs):
    raise DeprecationWarning(
        "Mqtt information should not be included in gateway configuration. Please remove"
    )


def build_connection_yaml():
    """
    Attempts to build a valid connection.yaml from legacy configuration files
    :return:
    """
    try:
        # Legacy cloud.yaml
        log.info("Attempting to build connection.yaml from legacy cloud.yaml.")
        with open(aware_path / "config" / "cloud.yaml") as r:
            with open(aware_path / "config" / "connection.yaml", "w") as w:
                w.write("defaults: gcp\n" + r.read())
    except FileNotFoundError:
        # Legacy Local gateway.yaml
        log.warning(f"Legacy cloud.yaml not found in file path {aware_path / 'config'}")
        log.info("Attempting to build connection.yaml from legacy gateway.yaml.")
        try:
            legacy_config = pyaware.config.load_yaml_config(
                aware_path / "config" / "gateway.yaml"
            )
        except FileNotFoundError:
            raise FileNotFoundError(
                f"No valid config file is found in file path {aware_path / 'config'}. "
                f"Please provide a connection config or legacy config file with valid configuration."
            )
        mqtt_info = [
            v["params"]
            for v in legacy_config.get("communication", [])
            if v.get("type") in ["hbmqtt_raw", "mqtt_raw"]
        ]
        if len(mqtt_info) != 1:
            raise ValueError(
                "No valid mqtt communication information in legacy gateway.yaml. Aborting"
            )
        mqtt_info = mqtt_info[0]
        mqtt_info["defaults"] = "local"
        pyaware.config.save_yaml_config(
            aware_path / "config" / "connection.yaml", mqtt_info
        )


def load_connection_config():
    try:
        return pyaware.config.load_yaml_config(
            pyaware.config.aware_path / "config" / "connection.yaml"
        )
    except FileNotFoundError:
        log.warning(
            f"connection.yaml not found in file path {pyaware.config.aware_path / 'config'}."
        )
        pyaware.config.build_connection_yaml()
        return pyaware.config.load_yaml_config(
            pyaware.config.aware_path / "config" / "connection.yaml"
        )


async def parse_mqtt(
    params: typing.Dict[
        str, typing.Dict[str, typing.Union[str, dict, int, float, bool]]
    ],
    is_deferred_params: typing.Optional[bool] = False,
) -> pyaware.mqtt.client.Mqtt:
    import pyaware.mqtt.client

    # Checks if the unit can parse the mqtt comms without information from gateway.yaml
    defaults = params.pop("defaults", "gcp")
    if defaults == "local":
        # If there is no configuration option or configuration option failed.
        if not params.get("gateway_id"):
            log.info(f"No valid gateway_id was provided from connection.yaml config.")
            adapters = list(
                ifaddr.get_adapters()
            )  # NOTE: Adapters returned is an ordered dictionary
            while adapters:
                # Fetch the last adapter out of our list to try our best and be deterministic every start-up without
                # a gateway_id specified
                eth_interface = adapters.pop()
                ip_addresses = [ip_address.ip for ip_address in eth_interface.ips]
                if "127.0.0.1" not in ip_addresses:
                    # If the adapter is not a loopback adapter
                    log.info(f"Defaulting to last adapter: {eth_interface.name}.")
                    params["gateway_id"] = await get_mac_address(
                        eth_interface=eth_interface.name
                    )
                    break
            if not adapters:
                # In the case where we don't have a gateway id specified and there are no valid adapters present on the
                # device we have most likely reached a race condition with adapter setup or a faulty device
                log.warning("No valid adapter found on device. Cannot set gateway_id.")
                log.warning("Stopping pyaware.")
                pyaware.stop()

        config = pyaware.mqtt.config.LocalConfig(**params)
    elif defaults == "gcp":
        config = pyaware.mqtt.config.GCPCloudConfig(**params)
    else:
        config = pyaware.mqtt.config.GCPCloudConfig(**params)
    client = pyaware.mqtt.client.Mqtt(config)
    client.setup_gateway_topics()
    if not is_deferred_params:
        client.gateway_parse_complete.set()
    client.start()
    client.start_managers()
    # Wait 10 seconds for mqtt to connect
    try:
        await asyncio.wait_for(client.evt_connected.wait(), timeout=10)
    except asyncio.TimeoutError:
        log.info("Failed to connect within 10 seconds, continuing startup")

    try:
        log.info(
            f"Waiting {config.remote_configuration_timeout} seconds for configuration over mqtt"
        )
        await asyncio.wait_for(
            client.gateway_config_received.wait(),
            timeout=config.remote_configuration_timeout,
        )
    except asyncio.TimeoutError:
        log.info("Failed to receive remote configuration")
    if not client.gateway_config:
        log.info("Proceeding to load local configuration")
        client.load_config_from_disk()
    return client


async def parse_gateway(**kwargs):
    raise DeprecationWarning(
        "Gateway IPC information should not be included in gateway configuration. Please remove"
    )


async def get_mac_address(eth_interface="eth0", **kwargs) -> str:
    if platform.system() == "Linux":
        import fcntl
        import socket
        import struct

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(
            s.fileno(), 0x8927, struct.pack("256s", bytes(eth_interface, "utf-8")[:15])
        )
        return ":".join([f"{b:02x}" for b in info[18:24]])
    else:
        import uuid

        # Note: This ignores the interface selection and if no interfaces are present will return a random mac address
        # each power up with the least significant bit of the first octet set to 1
        return ":".join(
            [f"{(uuid.getnode() >> ele) & 0xff:02x}" for ele in range(0, 8 * 6, 8)][
                ::-1
            ]
        )


async def parse_comm_params(comms, instances) -> typing.Tuple[dict, dict]:
    comms_params = {}
    comms_params_unable_to_parse = {}

    for (
        k,
        v,
    ) in comms["params"].items():
        communication_types = [
            "value",
            "ref_comms",
            "ref_path",
            "ref_device",
            "ref_comms_param",
            "ref_translation_config",
            "ref_translation",
            "ref_mac_address",
            "uuid",
        ]
        # If the value does not exist (not set in config) then set the value to the default.
        # NOTE: Assumes that NoneType is not a valid value to be set.
        if not isinstance(v, dict) and v is None:
            log.warning(
                f'Value for communications parameter: "{k}" cannot be NoneType. Using default value if one is available.'
            )
            continue
        elif isinstance(v, dict) and "value" in v.keys() and v.get("value") is None:
            log.warning(
                f'Value for communications parameter: "{k}" cannot be NoneType. Using default value if one is available.'
            )
            continue
        elif isinstance(v, dict) and "key" in v.keys() and v.get("key") is None:
            log.warning(
                f'Key for communications parameter: "{k}" cannot be NoneType. Using default value if one is available.'
            )
            continue
        # Begin parsing the valid parameters
        elif not isinstance(v, dict):
            comms_params[k] = v
        elif v["type"] == "value":
            comms_params[k] = v["value"]
        elif v["type"] == "ref_comms" and instances:
            comms_params[k] = instances[v["value"]]
        elif v["type"] == "ref_path":
            comms_params[k] = aware_path / Path(v["value"])
        elif v["type"] == "ref_device":
            comms_params[k] = (
                Path(pyaware.__file__).parent / "devices" / Path(v["value"])
            )
        elif v["type"] == "ref_comms_param" and instances:
            comms_params[k] = getattr(instances[v["value"]], v["key"])
        elif v["type"] == "ref_translation_config":
            comms_params[k] = aware_path / "config" / Path(v["value"])
        elif v["type"] == "ref_translation" and instances:
            comms_params[k] = {d: instances[d] for d in v["value"]}
        elif v["type"] == "ref_mac_address":
            try:
                comms_params[k] = await get_mac_address(v.get("value", "eth0"))
            except OSError:
                comms_params_unable_to_parse[k] = v
        elif v["type"] == "uuid":
            comms_params[k] = uuid.uuid4()
        # Perform any error handling and validation steps
        elif not instances and v["type"] in communication_types:
            # If there are no instances the comms param has a valid type then we just can't parse these parameters
            comms_params_unable_to_parse[k] = v
        else:
            # The type in the file is not valid
            raise ValueError("No valid type detected in config file")
    return comms_params, comms_params_unable_to_parse


async def parse_communication(communication: list):
    """
    :param communication:
    :return: dictionary of form
    {
      <id>:
        {
          "protocol": <string>, # eg. modbus_rtu, modbus_tcp
          "handler": handler to call to return the communication type in a connected state
        },
        {...},
      ...,
    }
    """
    protocol_handlers = {
        "modbus_rtu": parse_modbus_rtu,
        "modbus_rtu2": parse_modbus_rtu,
        "modbus_tcp": parse_modbus_tcp,
        "modbus_tcp2": parse_modbus_tcp,
        "sp_pro": parse_sp_pro,
        "modbus_tcp_server": parse_modbus_tcp_server,
        "imac2_auto_detect": parse_imac2_master_auto_detect,
        "translator": parse_translator,
        "modbus_device": parse_modbus_device,
        "comap_device": parse_comap_device,
        "sp_pro_device": parse_sp_pro_device,
        "mqtt_raw": parse_hbmqtt_raw,
        "mqtt_gcp": parse_hbmqtt_gcp,
        "hbmqtt_raw": parse_hbmqtt_raw,
        "hbmqtt_gcp": parse_hbmqtt_gcp,
        "gateway_ipc": parse_gateway,
        "snmp_device": parse_snmp_device,
        "solar_cube": parse_solar_cube,
    }
    instances = {}
    for comms in communication:
        log.info(f"Initialising {comms['name']}")
        comms_params, invalid_params = await parse_comm_params(comms, instances)
        if invalid_params:
            log.warning(
                f'The following parameters are invalid and were ignored: "{invalid_params}"'
            )
        try:
            instances[comms["name"]] = await protocol_handlers[comms["type"]](
                **comms_params
            )
        except DeprecationWarning as e:
            log.warning(repr(e))
        log.info(f"Initialised {comms['name']}")
    return instances
