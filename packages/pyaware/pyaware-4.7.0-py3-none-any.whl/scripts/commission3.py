import aiomodbus.serial

# !/usr/bin/env python
"""
Pymodbus Synchronous Client Examples
--------------------------------------------------------------------------
The following is an example of how to use the synchronous modbus client
implementation from pymodbus.
It should be noted that the client can also be used with
the guard construct that is available in python 2.5 and up::
    with ModbusClient('127.0.0.1') as client:
        result = client.read_coils(1,10)
        print result
"""
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
# from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# from pymodbus.client.sync import ModbusUdpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
import logging
import asyncio
from pathlib import Path
import pyaware.config
import pyaware.data_types

FORMAT = (
    "%(asctime)-15s %(threadName)-15s "
    "%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
)
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)


async def get_modbus_comms(config):
    modbus_comms = [
        comm
        for comm in config.get("communication", [])
        if comm["type"] in ["modbus_rtu", "modbus_rtu2", "modbus_tcp", "modbus_tcp2"]
    ]
    return await pyaware.config.parse_communication(modbus_comms)


async def get_modbus_blocks(config, instances):
    modbus_devices = [
        comm
        for comm in config.get("communication", [])
        if comm["type"] in ["modbus_device"]
    ]
    blocks = []
    for dev in modbus_devices:
        params = await pyaware.config.parse_comm_params(dev, instances)
        dev_config = pyaware.config.load_yaml_config(params["config"])
        read_blocks = []
        address_shift = params.get("address_shift", 0)
        for source in dev_config["sources"].values():
            source.get("handle", "holding")
            shifted = []
            for x in source["blocks"]:
                shifted.append([y + address_shift for y in x])
            read_blocks.append(
                {"handle": source.get("handle", "holding"), "blocks": shifted}
            )
        blocks.append(
            {
                "device_id": params["device_id"],
                "blocks": read_blocks,
                "client": params["client"],
                "unit": params["unit"],
            }
        )
    return blocks


async def main():
    config = pyaware.config.load_yaml_config(Path() / "config" / "gateway.yaml")
    comms = await get_modbus_comms(config)
    read_blocks = await get_modbus_blocks(config, comms)
    for x in read_blocks:
        addr_map = pyaware.data_types.modbus.AddressMapUint16()
        for block in x["blocks"]:
            if block["handle"] == "holding":
                handle = x["client"].read_holding_registers
            elif block["handle"] == "input":
                handle = x["client"].read_input_registers
            elif block["handle"] == "coils":
                handle = x["client"].read_coils
            else:
                print(f"Invalid handle {x['handle']} for {x['device_id']}")
                continue
            for start, end in block["blocks"]:
                count = len(range(start, end))
                for _ in range(3):
                    try:
                        resp = await handle(
                            address=start, count=count, unit=x["unit"], timeout=2
                        )
                        addr_map[start:end] = resp
                        break
                    except BaseException as e:
                        print(f"Device {x['device_id']} failed read block {block}")
                        print(repr(e))

        print(f"Device {x['device_id']}: {addr_map}")


if __name__ == "__main__":
    asyncio.run(main())
