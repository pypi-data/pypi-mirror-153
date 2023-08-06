import time
from datetime import datetime
import logging
from enum import Flag
import typing
import asyncio

import aiohttp
import aiomodbus.tcp
import aiomodbus.serial

import pyaware.triggers
import pyaware.aggregations
from pyaware import events
from pyaware.data_types.modbus import AddressMapUint16, Param, ParamMask
from pyaware.protocol.imac2 import ModuleStatus
from pyaware.protocol.modbus import modbus_exception_codes
from pyaware import watchdog

try:
    import rapidjson as json
except ImportError:
    import json

if typing.TYPE_CHECKING:
    pass

log = logging.getLogger(__file__)
# Address 1036
generation_bits = {0: 0, 1: 0b1 << 8, 2: 0b1 << 9, 3: 0b11 << 8}


class ModuleStatusBits(Flag):
    ON_SCAN = 1 << 0
    L1_CLASH = 1 << 1
    GLOBAL_SELECT = 1 << 2
    L1_OWNED = 1 << 3
    L2_OWNED = 1 << 4
    SYSTEM_OWNED = 1 << 5
    L2_CLASH = 1 << 6
    BYTE_OWNED = 1 << 7


STATUS_MAP = {
    0b00000000: ModuleStatus.NEVER_ONLINE,
    0b00000001: ModuleStatus.OFFLINE,
    0b00000010: ModuleStatus.CLASH,
    0b00000011: ModuleStatus.CLASH,
    0b00000100: ModuleStatus.NEVER_ONLINE,
    0b00000101: ModuleStatus.OFFLINE,
    0b00000110: ModuleStatus.CLASH,
    0b00000111: ModuleStatus.CLASH,
    0b00001000: ModuleStatus.NEVER_ONLINE,
    0b00001001: ModuleStatus.ONLINE,
    0b00001010: ModuleStatus.CLASH,
    0b00001011: ModuleStatus.CLASH,
    0b00001100: ModuleStatus.L1_OWNED,
    0b00001101: ModuleStatus.L1_OWNED,
    0b00001110: ModuleStatus.CLASH,
    0b00001111: ModuleStatus.CLASH,
    0b00010000: ModuleStatus.NEVER_ONLINE,
    0b00010001: ModuleStatus.OFFLINE,
    0b00010010: ModuleStatus.CLASH,
    0b00010011: ModuleStatus.CLASH,
    0b00010100: ModuleStatus.L2_OWNED,
    0b00010101: ModuleStatus.L2_OWNED,
    0b00010110: ModuleStatus.CLASH,
    0b00010111: ModuleStatus.CLASH,
    0b00011000: ModuleStatus.NEVER_ONLINE,
    0b00011001: ModuleStatus.ONLINE,
    0b00011010: ModuleStatus.CLASH,
    0b00011011: ModuleStatus.CLASH,
    0b00011100: ModuleStatus.L1_OWNED,
    0b00011101: ModuleStatus.L1_OWNED,
    0b00011110: ModuleStatus.CLASH,
    0b00011111: ModuleStatus.CLASH,
    0b00100000: ModuleStatus.SYSTEM,
    0b00100001: ModuleStatus.SYSTEM,
    0b00100010: ModuleStatus.CLASH,
    0b00100011: ModuleStatus.CLASH,
    0b00100100: ModuleStatus.SYSTEM,
    0b00100101: ModuleStatus.SYSTEM,
    0b00100110: ModuleStatus.CLASH,
    0b00100111: ModuleStatus.CLASH,
    0b00101000: ModuleStatus.SYSTEM,
    0b00101001: ModuleStatus.SYSTEM,
    0b00101010: ModuleStatus.CLASH,
    0b00101011: ModuleStatus.CLASH,
    0b00101100: ModuleStatus.SYSTEM,
    0b00101101: ModuleStatus.SYSTEM,
    0b00101110: ModuleStatus.CLASH,
    0b00101111: ModuleStatus.CLASH,
    0b00110000: ModuleStatus.SYSTEM,
    0b00110001: ModuleStatus.SYSTEM,
    0b00110010: ModuleStatus.CLASH,
    0b00110011: ModuleStatus.CLASH,
    0b00110100: ModuleStatus.SYSTEM,
    0b00110101: ModuleStatus.SYSTEM,
    0b00110110: ModuleStatus.CLASH,
    0b00110111: ModuleStatus.CLASH,
    0b00111000: ModuleStatus.SYSTEM,
    0b00111001: ModuleStatus.SYSTEM,
    0b00111010: ModuleStatus.CLASH,
    0b00111011: ModuleStatus.CLASH,
    0b00111100: ModuleStatus.SYSTEM,
    0b00111101: ModuleStatus.SYSTEM,
    0b00111110: ModuleStatus.CLASH,
    0b00111111: ModuleStatus.CLASH,
    0b01000000: ModuleStatus.CLASH,
    0b01000001: ModuleStatus.CLASH,
    0b01000010: ModuleStatus.CLASH,
    0b01000011: ModuleStatus.CLASH,
    0b01000100: ModuleStatus.CLASH,
    0b01000101: ModuleStatus.CLASH,
    0b01000110: ModuleStatus.CLASH,
    0b01000111: ModuleStatus.CLASH,
    0b01001000: ModuleStatus.CLASH,
    0b01001001: ModuleStatus.CLASH,
    0b01001010: ModuleStatus.CLASH,
    0b01001011: ModuleStatus.CLASH,
    0b01001100: ModuleStatus.CLASH,
    0b01001101: ModuleStatus.CLASH,
    0b01001110: ModuleStatus.CLASH,
    0b01001111: ModuleStatus.CLASH,
    0b01010000: ModuleStatus.CLASH,
    0b01010001: ModuleStatus.CLASH,
    0b01010010: ModuleStatus.CLASH,
    0b01010011: ModuleStatus.CLASH,
    0b01010100: ModuleStatus.CLASH,
    0b01010101: ModuleStatus.CLASH,
    0b01010110: ModuleStatus.CLASH,
    0b01010111: ModuleStatus.CLASH,
    0b01011000: ModuleStatus.CLASH,
    0b01011001: ModuleStatus.CLASH,
    0b01011010: ModuleStatus.CLASH,
    0b01011011: ModuleStatus.CLASH,
    0b01011100: ModuleStatus.CLASH,
    0b01011101: ModuleStatus.CLASH,
    0b01011110: ModuleStatus.CLASH,
    0b01011111: ModuleStatus.CLASH,
    0b01100000: ModuleStatus.CLASH,
    0b01100001: ModuleStatus.CLASH,
    0b01100010: ModuleStatus.CLASH,
    0b01100011: ModuleStatus.CLASH,
    0b01100100: ModuleStatus.CLASH,
    0b01100101: ModuleStatus.CLASH,
    0b01100110: ModuleStatus.CLASH,
    0b01100111: ModuleStatus.CLASH,
    0b01101000: ModuleStatus.CLASH,
    0b01101001: ModuleStatus.CLASH,
    0b01101010: ModuleStatus.CLASH,
    0b01101011: ModuleStatus.CLASH,
    0b01101100: ModuleStatus.CLASH,
    0b01101101: ModuleStatus.CLASH,
    0b01101110: ModuleStatus.CLASH,
    0b01101111: ModuleStatus.CLASH,
    0b01110000: ModuleStatus.CLASH,
    0b01110001: ModuleStatus.CLASH,
    0b01110010: ModuleStatus.CLASH,
    0b01110011: ModuleStatus.CLASH,
    0b01110100: ModuleStatus.CLASH,
    0b01110101: ModuleStatus.CLASH,
    0b01110110: ModuleStatus.CLASH,
    0b01110111: ModuleStatus.CLASH,
    0b01111000: ModuleStatus.CLASH,
    0b01111001: ModuleStatus.CLASH,
    0b01111010: ModuleStatus.CLASH,
    0b01111011: ModuleStatus.CLASH,
    0b01111100: ModuleStatus.CLASH,
    0b01111101: ModuleStatus.CLASH,
    0b01111110: ModuleStatus.CLASH,
    0b01111111: ModuleStatus.CLASH,
}
# Address 1042
remote_key = {
    0: " No Key",
    1: " ESC Key ESC_KEY",
    2: " Alarm Key ALARM_KEY",
    3: " Menu Key MENU_KEY",
    5: " F1 Key F1_KEY",
    6: " F2 Key F2_KEY",
    7: " F3 Key F3_KEY",
    8: " F4 Key F4_KEY",
    9: " Left Arrow Key LEFT_KEY",
    10: " Up Arrow Key UP_KEY",
    11: " Right Arrow Key RIGHT_KEY",
    12: " Down Arrow Key DOWN_KEY",
    13: " Enter Key ENTER_KEY",
    16: " Shift Mode Key SHIFT_MOD",
}


class TopicLock(asyncio.Lock):
    def __init__(
        self,
        *args,
        topic: str,
        acquire_state: bool = True,
        data_key: str = "",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.topic = topic
        self.data_key = data_key
        self.acquire_state = acquire_state

    async def __aenter__(self):
        aenter = await super().__aenter__()
        if self.data_key:
            parameters = {self.data_key: self.acquire_state}
        else:
            parameters = self.acquire_state
        pyaware.events.publish(self.topic, data=parameters, timestamp=datetime.utcnow())
        log.debug("Roll call lock acquired")
        return aenter

    async def __aexit__(self, *args, **kwargs):
        aexit = await super().__aexit__(*args, **kwargs)
        if self.data_key:
            parameters = {self.data_key: not self.acquire_state}
        else:
            parameters = not self.acquire_state
        pyaware.events.publish(self.topic, data=parameters, timestamp=datetime.utcnow())
        log.debug("Roll call lock released")
        return aexit


class ConditionalLock:
    """
    Implements conditional lock acquisition for asyncio.Lock()
    usage:
    >>>x = 1
    >>>l = ConditionalLock(lambda: x == 2)
    >>>async def set_x():
    >>>    await asyncio.sleep(5)
    >>>    global x
    >>>    x = 2
    >>>async def main():
    >>>    global x
    >>>    x = 1
    >>>    asyncio.create_task(set_x())
    >>>    async with l:
    >>>        print(f"Acquired @ x=={x}")
    >>>
    >>>asyncio.create_task(main())

    :param predicate A callable that should return True when the lock should be acquired
    :param lock A asyncio Lock that can be shared across multiple conditional locks. If not provided, will use as new
    :param check_condition_after Time to wait after a failed predicate call before trying to reacquire the lock
    lock
    """

    def __init__(
        self,
        predicate: typing.Callable,
        *args,
        lock: typing.Optional[asyncio.Lock] = None,
        check_condition_after: float = 0.1,
        **kwargs,
    ):
        self.lock = lock or asyncio.Lock()
        self.predicate = predicate
        self.check_condition_after = check_condition_after
        super().__init__(*args, **kwargs)

    async def __aenter__(self):
        try:
            while True:
                aenter = await self.lock.acquire()
                if self.predicate():
                    break
                self.lock.release()
                await asyncio.sleep(self.check_condition_after)
        except BaseException:
            if self.lock.locked():
                self.lock.release()
            raise
        log.debug("Acquired block lock")
        return aenter

    async def __aexit__(self, *args, **kwargs):
        if self.lock.locked():
            log.debug("Released block lock")
            self.lock.release()


@events.enable
class Imac2Protocol:
    name = "Imac Controller"
    module_type = "imac-controller-master"
    config_name = "imac_controller_parameter_spec.yaml"

    def __init__(self, client_ser, client_eth=None, unit=1):
        """
        :param client_ser: Client connected to the iMAC serial interface
        :param client_eth: Client connection to the iMAC2 Ethernet connection
        :param unit: Modbus unit id for the ModbusRTU connection
        """
        self.client_ser = client_ser
        self.client_eth = client_eth
        self.unit = unit
        self._block_lock = asyncio.Lock()
        self.block_condition = {
            None: ConditionalLock(lambda: True, lock=self._block_lock),
            0: ConditionalLock(
                lambda: self.roll_call_gen in [None, 0], lock=self._block_lock
            ),
            1: ConditionalLock(
                lambda: self.roll_call_gen in [None, 1], lock=self._block_lock
            ),
            2: ConditionalLock(
                lambda: self.roll_call_gen in [None, 2], lock=self._block_lock
            ),
            3: ConditionalLock(
                lambda: self.roll_call_gen in [None, 3], lock=self._block_lock
            ),
        }
        self.roll_call_gen = None
        self.auto_discover_lock = asyncio.Lock()
        self.roll_call_lock = TopicLock(
            topic="imac_controller_data",
            data_key="roll-call-active",
            acquire_state=True,
        )
        self.roll_call_params = {
            "generation_id": ParamMask(
                0x409, "generation_id", mask=0b11 << 8, rshift=8
            ),
            "serial_number": Param(0x40B, "serial_number"),
            "module_type": ParamMask(0x40C, "module_type", mask=0xFF),
            "imac_address": ParamMask(0x40A, "imac_address", mask=0xFF),
            "version": ParamMask(0x40C, "version", mask=0xFF00, rshift=8),
        }

    async def roll_call(self) -> [AddressMapUint16]:
        """
        Roll call the imac to discover the modules on the line
        1. Assert the “Reset Rollcall” bit (0x409: Bit 0) and wait for the bit to be cleared by the system.
        2. Read the Rollcall Control Word.
        3. Assert the “Next Rollcall” bit (0x409: Bit 1), preserving bits 8 to 15 you read in the previous step, and
           wait for the bit to be cleared by the system.
        4. Confirm that the “Rollcall Fail” (0x409: Bit 5) bit is not set.
        5. Module data will now be available in registers 1033 to 1041 (0x409 to 0x411). Richard says false
        6. The next module can be rollcalled by repeating steps 2 to 5. This process can be repeated until the
           Serial Number register (0x40B) reads as 0, indicating that all modules have been rollcalled. Modules
           will roll call in order of address followed by serial number, from highest to lowest.
        :return: List of address map parameters from addresses 0x409-0x411
        """
        # 1 Asset reset roll call
        async with self.roll_call_lock:
            async with self.block_condition[None]:
                await self.set_bit(0x409, 0, check=False)
                await self.wait_on_bit(0x409, 0, check_to=False)
                self.roll_call_gen = None
                log.debug(f"Roll call system reset")

            # Return modules as they are found
            async for mod in self.roll_call_next():
                yield mod
            self.roll_call_gen = None

    async def roll_call_next(self) -> typing.AsyncIterable[AddressMapUint16]:
        prev_roll = [0] * 4
        while True:
            # 3 Assert next roll call bit
            async with self.block_condition[None]:
                await self.set_bit(0x409, 1, check=False)
                await self.wait_on_bit(0x409, 1, check_to=False, timeout=10)
                # 4 Check for roll call fail bit
                await self.check_bit(0x409, 5, check_to=False)
                addr_map = await self.read_ser(0x409, 9)
                self.roll_call_gen = (addr_map[0x409] & (0b11 << 8)) >> 8

            if addr_map[0x40B] == 0:
                # 6 All modules have been roll called
                break
            new_roll = addr_map[0x409:0x40D]
            if new_roll != prev_roll:
                log.debug(f"Roll call system read {new_roll}")
                yield addr_map
            prev_roll = new_roll

    async def roll_call_force(self, address) -> [AddressMapUint16]:
        """
        Roll call the imac to discover the modules on the line
        1. Assert the “Reset Rollcall” bit (0x409: Bit 0) and wait for the bit to be cleared by the system.
        2. Read the Rollcall Control Word.
        3. Assert the “Next Rollcall” bit (0x409: Bit 2), preserving bits 8 to 15 you read in the previous step, and
           wait for the bit to be cleared by the system.
        4. Confirm that the “Rollcall Fail” (0x409: Bit 5) bit is not set.
        5. Module data will now be available in registers 1033 to 1041 (0x409 to 0x411). Richard says false
        6. The next module can be rollcalled by repeating steps 2 to 5. This process can be repeated until the
           Serial Number register (0x40B) reads as 0, indicating that all modules have been rollcalled. Modules
           will roll call in order of address followed by serial number, from highest to lowest.
        :return: List of address map parameters from addresses 0x409-0x411
        """
        # 1 Asset reset roll call
        async with self.roll_call_lock:
            async with self.block_condition[None]:
                await self.write(0x40A, address)
                await self.set_bit(0x409, 0, check=False)
                await self.wait_on_bit(0x409, 0, check_to=False)
                self.roll_call_gen = None
                log.debug(f"Roll call force reset")
                modules = []
                async for mod in self.roll_call_force_next():
                    modules.append(mod)
                self.roll_call_gen = None
                return modules

    async def roll_call_force_next(self) -> typing.AsyncIterable[AddressMapUint16]:
        prev_roll = [0] * 4
        while True:
            # 3 Assert next roll call bit
            await self.set_bit(0x409, 2, check=False)
            await self.wait_on_bit(0x409, 2, check_to=False, timeout=10)
            # 4 Check for roll call fail bit
            await self.check_bit(0x409, 5, check_to=False)
            addr_map = await self.read_ser(0x409, 9)
            self.roll_call_gen = (addr_map[0x409] & (0b11 << 8)) >> 8
            if addr_map[0x40B] == 0:
                # 6 All modules have been roll called
                break
            new_roll = addr_map[0x409:0x40D]
            if new_roll != prev_roll:
                log.debug(f"Roll call force read {new_roll}")
                yield addr_map
            prev_roll = new_roll

    def decode_roll_call(self, roll_call: [AddressMapUint16]) -> [dict]:
        return [self.decode_roll_call_single(roll) for roll in roll_call]

    def decode_roll_call_single(self, roll_call: AddressMapUint16) -> dict:
        params = {}
        for param in self.roll_call_params.values():
            params.update(param.decode(roll_call))
        params["dev_id"] = f"{params['serial_number']}-G{params['generation_id'] + 1}"
        return params

    async def read_by_serial_number(
        self, serial_number, generation, block=0
    ) -> AddressMapUint16:
        """
        :param serial_number: 16 bit serial number excluding generation
        :param generation: imac module generation indexed from zero. ie. Gen 2 is 1
        :param block:
        Read the parameters of a serial numbered item
        1. Ensure that the Rollcall Serial Number register (40Bh), the Generation ID (409h bits 8 & 9) and the
           Rollcall Block Number register (40Dh) are set up as per the module that is to be read.
        2. Assert the “Read Serial Number” bit (409h: Bit 3), preserving Generation ID bits 8 & 9 setup in step
        1, and wait for the bit to be cleared by the system
        3. Confirm that the “Read SN Fail” (409h: Bit 6) bit is not set.
        4. Module Parameters 1, 2, 3 and 4 will now be available in registers 1038 to 1041 (40Eh to 411h).
        :return: Address map of 4 parameters from registers 0x40E to 0x411
        """
        async with self.block_condition[generation]:
            reg_roll_coll = await self.read_ser_single(0x409)
            await self.write(0x40B, serial_number)
            await self.write(0x409, (reg_roll_coll & ~(0b11 << 8)) | (generation << 8))
            await self.write(0x40D, block)
            # 2 Assert read serial number
            await self.set_bit(0x409, 3)
            await self.wait_on_bit(0x409, 3, False)
            await self.check_bit(0x409, 6, False)
            return await self.read_ser(0x409, 9)

    async def write_by_serial_number(
        self, serial_number, generation, block, addr_map: AddressMapUint16
    ):
        """
        1. Ensure that the Rollcall Serial Number register (40Bh), the Generation ID (409h bits 8 & 9) and the
           Rollcall Block Number register (40Dh) are set up as per the module that is to be written.
        2. Ensure the parameters that are to be written to the module are set up in registers 1038 to 1041
           (40Eh to 410h).
        3. Assert the “Write Serial Number” bit (409h: Bit 4), preserving Generation ID bits 8 & 9 setup in step
           1, and wait for the bit to be cleared by the system.
        4. Confirm that the “Write SN Fail” (409h: Bit 7) bit is not set.
        External to this command, a check should be performed to ensure that the parameters were successfully written.
        5. Wait for block scan register 0x406 increment twice (Heartbeat).
           Note: can take a while so you can write multiple serials and then bulk check them after the 2 block scans
        6. Module Parameters 1,2,3, and 4 will now have been successfully written to the module from
        registers 1038 to 1041 (40Eh to 411h).
        :return:
        """
        async with self.block_condition[generation]:
            reg_roll_coll = await self.read_ser_single(0x409)
            await self.write(0x40B, serial_number)
            await self.write(0x409, (reg_roll_coll & ~(0b11 << 8)) | (generation << 8))
            await self.write(0x40D, block)
            await self.write(0x409, *addr_map[0x409:0x412])
            # 3 Assert write serial number
            await self.set_bit(0x409, 4)
            await self.wait_on_bit(0x409, 4, False)
            # 4 Confirm write SN Fail bit not set
            await self.check_bit(0x409, 7, False)

    async def write_by_serial_number_no_check(
        self, serial_number, generation, block, addr_map: AddressMapUint16
    ):
        """
        Does a write by serial number with no confirmation of the bit 4 being cleared. This can be done for more time
        critical writes where it will be obvious it has not
        1. Ensure that the Rollcall Serial Number register (40Bh), the Generation ID (409h bits 8 & 9) and the
           Rollcall Block Number register (40Dh) are set up as per the module that is to be written.
        2. Ensure the parameters that are to be written to the module are set up in registers 1038 to 1041
           (40Eh to 410h).
        :return:
        """
        async with self.block_condition[generation]:
            reg_roll_coll = await self.read_ser_single(0x409)
            await self.write(0x40B, serial_number)
            await self.write(0x409, (reg_roll_coll & ~(0b11 << 8)) | (generation << 8))
            await self.write(0x40D, block)
            await self.write(0x409, *addr_map[0x409:0x412])
            # 3 Assert write serial number
            await self.set_bit(0x409, 4)

    async def read(self, client, address: int, count: int = 1) -> AddressMapUint16:
        """
        Reads modbus holding registers and returns an address map of the response
        :param address:
        :param count:
        :return:
        """
        addr_map = AddressMapUint16()
        addr_map[address : address + count] = await client.read_holding_registers(
            address, count, unit=self.unit
        )
        return addr_map

    @watchdog.watch("imac_eth_status", starve_on_exception=3)
    async def read_eth(
        self, address: int, count: int = 1
    ) -> typing.Union[AddressMapUint16, typing.Awaitable]:
        """
        Reads modbus holding registers and returns an address map of the response
        :param address:
        :param count:
        :return:
        """
        return await self.read(self.client_eth, address, count)

    async def read_ser_single(self, address) -> int:
        read = await self.read_ser(address, 1)
        return read[address]

    async def write_bit(self, address, bit, value):
        if isinstance(self.client_ser, aiomodbus.serial.ModbusSerialClient):
            await self.client_ser.write_single_coil(
                address * 16 + bit, value, unit=self.unit
            )
        else:
            wr = await self.client_ser.protocol.write_coil(
                address * 16 + bit, value, unit=self.unit
            )
            if wr.isError():
                raise modbus_exception_codes.get(wr.exception_code, IOError)

    async def set_bit(self, address, bit, check=True):
        await self.write_bit(address, bit, 1)
        if check:
            if not (1 << bit) & await self.read_ser_single(address):
                raise IOError(
                    "Bit not set correctly, check if someone is interfering with the device"
                )

    async def clear_bit(self, address, bit):
        await self.write_bit(address, bit, 0)
        if not (1 << bit) & ~await self.read_ser_single(address):
            raise IOError(
                "Bit not cleared correctly, check if someone is interfering with the device"
            )

    async def check_bit(self, address, bit, check_to):
        if not await self.read_ser_single(address) >> bit & 1 == check_to:
            raise ValueError(
                "Bit check failed, imac module failed to communicate with the master"
            )

    async def wait_on_bit(self, address, bit, check_to, timeout=3):
        start = time.time()
        last_attempt = False
        while True:
            try:
                await self.check_bit(address, bit, check_to)
                return
            except (IOError, ValueError):
                if time.time() - start > timeout:
                    if last_attempt:
                        break
                    last_attempt = True
        raise TimeoutError("Timeout waiting for bit check")

    @watchdog.watch("imac_ser_status", starve_on_exception=3)
    async def read_ser(self, address: int, count: int = 1) -> AddressMapUint16:
        """
        Reads modbus holding registers and returns an address map of the response
        :param address:
        :param count:
        :return:
        """
        return await self.read(self.client_ser, address, count)

    @watchdog.watch("imac_ser_status", starve_on_exception=3)
    async def write(self, address, *values):
        await self.client_ser.write_multiple_registers(address, *values, unit=self.unit)

    @staticmethod
    def parse_status(value):
        return STATUS_MAP[value & 0x7F]

    @staticmethod
    def parse_address_bypass(value):
        """
        Parses the address bypass status.

        :param value: Integer representing the DI4 address. Bit 0 correlates to local bypass. Bit 8 correlates to remote bypass.
        :return: 1 if unit is bypassed. 0 if unit is not bypassed.
        """
        # Check if bit one is set -> Unit is in local bypass
        is_local_bypass = bool(value & (1 << 0))
        # Check if bit 9 is set -> Unit is in remote bypass
        is_remote_bypass = bool(value & (1 << 8))
        if is_local_bypass or is_remote_bypass:
            return 1
        else:
            return 0

    @watchdog.watch("imac_rest_status")
    async def read_rest_data(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://{self.client_eth.host}/cgi-bin/deviceinfo.cgi"
            ) as response:
                text_obj = await response.read()
                return json.loads(text_obj.decode("utf-8", "ignore"))
