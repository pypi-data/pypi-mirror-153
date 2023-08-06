from unittest.mock import MagicMock
import threading
from _datetime import datetime
from pyaware import events
from pyaware.controllers.imac2.master import Imac2MasterController
from pyaware.data_types.modbus import AddressMapUint16, Param, ParamMask

roll_call_params = {
    "generation_id": ParamMask(0x409, "generation_id", mask=0b11 << 8, rshift=8),
    "serial_number": Param(0x40B, "serial_number"),
    "module_type": ParamMask(0x40C, "module_type", mask=0xFF),
    "imac_address": Param(0x40A, "imac_address"),
    "version": ParamMask(0x40C, "version", mask=0xFF00, rshift=8),
}


@events.enable
class MockImac2Protocol(Imac2MasterController):
    def __init__(self, roll_call, device_id: str, eth_client=None, _async=False):
        super().__init__(
            MagicMock(),
            stop_evt=threading.Event(),
            client_eth=eth_client or MagicMock(),
            _async=_async,
            device_id=device_id,
        )
        self.block_mimic = {}
        self._roll = roll_call

    def _read_by_serial_number_sync(
        self, serial_number, generation, block=0
    ) -> AddressMapUint16:
        """
        :param serial_number:
        :param generation:
        :param block:
        :return:
        """
        key = f"{serial_number}-G{generation + 1}"
        if key not in self.devices:
            raise IOError("No Device found")
        if key not in self.block_mimic:
            block_mock = AddressMapUint16()
            block_mock[0x409:0x412] = [0 for _ in range(0x409, 0x412)]
            self.block_mimic[key] = {
                k: AddressMapUint16() for k in [None, 0, 1, 2, 3, 4, 5, 6, 7]
            }
            for block_map in self.block_mimic[key].values():
                block_map[0x409:0x412] = block_mock[0x409:0x412]
        return self.block_mimic[key][block]

    async def _read_by_serial_number_async(
        self, serial_number, generation, block=0
    ) -> AddressMapUint16:
        """
        :param serial_number:
        :param generation:
        :param block:
        :return:
        """
        key = f"{serial_number}-G{generation + 1}"
        if key not in self.devices:
            raise IOError("No Device found")
        if key not in self.block_mimic:
            block_mock = AddressMapUint16()
            block_mock[0x409:0x412] = [0 for _ in range(0x409, 0x412)]
            self.block_mimic[key] = {
                k: AddressMapUint16() for k in [None, 0, 1, 2, 3, 4, 5, 6, 7]
            }
            for block_map in self.block_mimic[key].values():
                block_map[0x409:0x412] = block_mock[0x409:0x412]
        return self.block_mimic[key][block]

    def _write_by_serial_number_sync(
        self, serial_number, generation, block, addr_map: AddressMapUint16
    ):
        key = f"{serial_number}-G{generation + 1}"
        if key not in self.devices:
            raise IOError("No Device found")
        if key not in self.block_mimic:
            self.block_mimic[key] = AddressMapUint16(buffer={})
        self.block_mimic[key][block][0x409:0x412] = addr_map[0x409:0x412]

    async def _write_by_serial_number_async(
        self, serial_number, generation, block, addr_map: AddressMapUint16
    ):
        key = f"{serial_number}-G{generation + 1}"
        if key not in self.devices:
            raise IOError("No Device found")
        if key not in self.block_mimic:
            self.block_mimic[key] = AddressMapUint16(buffer={})
        self.block_mimic[key][block][0x409:0x412] = addr_map[0x409:0x412]

    def _roll_call_sync(self) -> [AddressMapUint16]:
        return self._roll

    async def _roll_call_async(self) -> [AddressMapUint16]:
        return self._roll

    async def _roll_call_force_async(self, address) -> [AddressMapUint16]:
        modules = self._roll
        dev_ids = await self.update_devices(modules)
        if dev_ids:
            self.update_topology()
        events.publish(
            "force_roll_call_complete", data=address, timestamp=datetime.utcnow()
        )
        return modules

    def _roll_call_force_sync(self, address) -> [AddressMapUint16]:
        modules = self._roll
        dev_ids = self.update_devices(modules)
        if dev_ids:
            self.update_topology()
        events.publish(
            "force_roll_call_complete", data=address, timestamp=datetime.utcnow()
        )
        return modules

    # @events.subscribe(topic="trigger_imac_poll")
    # async def poll_pipeline(self):
    #     """
    #     Pipeline that begins when a pipeline is published
    #     :param data:
    #     :return:
    #     """
    #     addr_map, timestamp = await self.poll_once()
    #     events.publish("imac_poll_data", data=addr_map, timestamp=timestamp)
    #     module_data = await self.process_module_data(addr_map, timestamp)
    #     # TODO process the imac metadata from poll here with asyncio.gather
    #     events.publish("imac_module_data", data=module_data, timestamp=timestamp)
    #     self.update_module_current_state(module_data)


def simulate_roll_call(*devices) -> [AddressMapUint16]:
    """
    Simulate a roll call of devices based on the
    :param dicts Each dict must have
        "generation_id": <0-3>,
        "serial_number": <16 bit>
        "module_type": <0-71>
        "imac_address": <0-255>
        "version": <0-255>
    :return:
    """
    resp = []
    for device in devices:
        addr_map = AddressMapUint16()
        addr_map[0x409:0x40D] = [0 for _ in range(0x409, 0x40D)]
        for param in device:
            roll_call_params[param].encode(device, addr_map)
        resp.append(addr_map)
    return resp


def simulate_gg2(serial_number, generation_id, number: int = 0) -> [AddressMapUint16]:
    if number == 0:
        addresses = [0, 0, 0]
    else:
        addresses = [number, number + 40, 0]
    return simulate_roll_call(
        *(
            {
                "generation_id": generation_id,
                "serial_number": serial_number,
                "version": 0,
                "imac_address": addr,
                "module_type": mod_type,
            }
            for addr, mod_type in zip(addresses, [61, 62, 63])
        )
    )
