from __future__ import annotations

import struct
import typing
from collections import namedtuple
from dataclasses import dataclass, field
from math import floor, log10

from pyaware import log
from pyaware.data_types.abc import ParamForm


def slice_list(slic):
    return [x for x in [slic.start, slic.stop, slic.step] if x is not None]


class ParamModbus(ParamForm):
    address: int

    def get_addresses(self) -> set:
        return {self.address}


def round_sig(x, sig=2):
    if x == 0:
        return x
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


class Endian:
    big = ">"
    little = "<"


c_decode = namedtuple("c_decode", ["format", "size"])
data_types = {
    "char": c_decode("c", 1),
    "schar": c_decode("b", 1),
    "uchar": c_decode("B", 1),
    "bool": c_decode("?", 1),
    "short": c_decode("h", 2),
    "ushort": c_decode("H", 2),
    "int": c_decode("i", 4),
    "uint": c_decode("I", 4),
    "long": c_decode("l", 4),
    "ulong": c_decode("L", 4),
    "longlong": c_decode("q", 8),
    "ulonglong": c_decode("Q", 8),
    "float": c_decode("f", 4),
    "double": c_decode("d", 8),
    "char[]": c_decode("s", None),
}


@dataclass
class Param(ParamModbus):
    address: int
    idx: str
    scale: float = 1
    block: typing.Any = None
    significant_figures: typing.Optional[int] = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        result = addr_map[self.address] * self.scale
        if self.significant_figures:
            result = round_sig(result, self.significant_figures)
        return {self.idx: result}

    def encode(self, data, addr_map: AddressMapUint16):
        try:
            value = data[self.idx]
        except KeyError:
            return addr_map

        value = round(value / self.scale)
        if value > 0xFFFF:
            raise OverflowError(
                f"Target value {data[self.idx]} when scaled 0x{value:02X} "
                f"is bigger than a 16 bit number"
            )
        addr_map[self.address] = value
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamBoolArray(ParamModbus):
    address: [int]
    idx: str
    length: int
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or any(
            [True for addr in self.address if addr_map[addr] is None]
        ):
            return {}
        bin_number = ""
        for addr in self.address:
            bin_number += f"{addr_map[addr]:0>16b}"[::-1]
        bin_number = bin_number[: self.length]
        bin_arr = [int(x) for x in bin_number]
        return {self.idx: bin_arr}

    def encode(self, data, addr_map: AddressMapUint16):
        # TODO
        try:
            addr_map[self.address] = data[self.idx]
        except KeyError:
            pass
        return addr_map

    def keys(self):
        return {self.idx}

    def get_addresses(self) -> set:
        return set(self.address)


@dataclass
class ParamEnumBoolArray(ParamModbus):
    address: [int]
    table: dict
    terminator: hex = None
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or any(
            [True for addr in self.address if addr_map[addr] is None]
        ):
            return {}
        params = {param: False for val, param in self.table.items()}
        for addr in self.address:
            value = addr_map[addr]
            # Assumes that values received are all 16 bit in size.
            value = struct.unpack("<H", struct.pack(">H", value))[0]
            if self.terminator is not None and value == self.terminator:
                break
            try:
                param = self.table[value]
            except KeyError:
                # Skip if value is not in enum i.e. not important
                continue
            params[param] = True
        return params

    def encode(self, data, addr_map: AddressMapUint16):
        # TODO: Implement an encode method for ParamEnumBoolArray
        raise NotImplementedError

    def get_addresses(self) -> set:
        return set(self.address)


@dataclass
class ParamText(ParamModbus):
    address: int
    idx: str
    length: int
    block: typing.Any = None
    padding: typing.Union[bytes, int] = b"\x00"
    null_byte: bool = True
    swap_bytes: bool = False
    swap_words: bool = False
    strip_leading: str = ""
    strip_lagging: str = ""
    meta: dict = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.padding, int):
            byt = bytearray(1)
            byt[0] = self.padding
            self.padding = bytes(byt)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        dec_str = bytearray()
        for x in addr_map[self.address : self.address + self.length]:
            if self.swap_bytes:
                dec_str.append((x & 0xFF00) >> 8)
                dec_str.append(x & 0xFF)
            else:
                dec_str.append(x & 0xFF)
                dec_str.append((x & 0xFF00) >> 8)
        dec_str = dec_str.strip(self.padding)
        dec_str = dec_str.replace(b"\x00", b"").decode("utf-8", "ignore")
        if self.strip_leading:
            dec_str = dec_str.lstrip(self.strip_leading)
        if self.strip_lagging:
            dec_str = dec_str.rstrip(self.strip_lagging)
        return {self.idx: dec_str}

    def encode(self, data, addr_map: AddressMapUint16):
        if len(data[self.idx]) > self.length * 2:
            raise ValueError(
                f"Invalid string length to pack into {self.idx} starting @ address: {self.address}"
            )
        addr_map[self.address : self.address + self.length * 2] = (
            [self.padding] * self.length * 2
        )
        for index, byt in data[self.idx].encode("utf-8"):
            addr_map[self.address + index // 2] += byt << (8 * index % 2)
        return addr_map

    def keys(self):
        return {self.idx}

    def get_addresses(self) -> set:
        return {addr for addr in range(self.address, self.address + self.length)}


@dataclass
class ParamBits(ParamModbus):
    address: int
    bitmask: dict
    idx: typing.Optional[str] = None
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        parameter_value = addr_map[self.address]
        return {
            idx: bool(parameter_value & (1 << bit)) for idx, bit in self.bitmask.items()
        }

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        for idx, bit_shift in self.bitmask.items():
            try:
                data_bit = data[idx]
            except KeyError:
                # Data not relevant
                continue
            # Initialise the address map with the address if the address is not initialised already.
            # NOTE: This is required for the bit wise operations below.
            if self.address not in addr_map._buf:
                addr_map[self.address] = 0
            if data_bit:
                addr_map[self.address] |= 1 << bit_shift
            else:
                addr_map[self.address] &= ~(1 << bit_shift)
        return addr_map

    def keys(self):
        return set(self.bitmask)


@dataclass
class ParamBit(ParamModbus):
    address: int
    idx: str
    bit: int
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        parameter_value = addr_map[self.address]
        return {self.idx: bool(parameter_value & (1 << self.bit))}

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        if self.idx not in data:
            return addr_map
        if self.address not in addr_map._buf:
            addr_map[self.address] = 0
        if data[self.idx]:
            # Set bit
            addr_map[self.address] |= 1 << self.bit
        else:
            # Clear bit
            addr_map[self.address] &= ~(1 << self.bit)
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamBool(ParamModbus):
    address: int
    idx: str
    block: typing.Any = None

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        return {self.idx: bool(addr_map[self.address])}

    def encode(self, data: dict, addr_map: AddressMapUint16):
        try:
            value = data[self.idx]
        except KeyError:
            return addr_map
        addr_map[self.address] = bool(value)


@dataclass
class ParamMask(ParamModbus):
    address: int
    idx: str
    mask: int = 0xFFFF
    rshift: int = 0
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        return {self.idx: ((addr_map[self.address] & self.mask) >> self.rshift)}

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            value = data[self.idx]
        except KeyError:
            return addr_map
        if value << self.rshift > self.mask:
            raise OverflowError(
                f"Target value 0x{value:02X} when shifted 0x{value << self.rshift:02X} "
                f"is bigger than the target mask 0x{self.mask:02X}"
            )
        if self.address not in addr_map:
            addr_map[self.address] = 0
        addr_map[self.address] &= ~self.mask
        addr_map[self.address] |= value << self.rshift
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamOffset(ParamModbus):
    offset: int = 0

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        resp = super(ParamOffset, self).decode(addr_map, block)
        resp[self.idx] += self.offset
        return resp

    def encode(self, data: dict, addr_map: AddressMapUint16):
        data = data.copy()
        data[self.idx] -= self.offset
        return super(ParamOffset, self).encode(data, addr_map)

    def keys(self):
        return {self.idx}


class ParamMaskBool(ParamMask):
    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        decoded = super().decode(addr_map, block)
        try:
            decoded[self.idx] = bool(decoded[self.idx])
        except KeyError:
            pass
        return decoded


@dataclass
class ParamMaskScale(ParamModbus):
    address: int
    idx: str
    mask: int = 0xFFFF
    rshift: int = 0
    block: typing.Any = None
    scale: float = 1.0
    significant_figures: typing.Optional[int] = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        result = ((addr_map[self.address] & self.mask) >> self.rshift) * self.scale
        if self.significant_figures:
            result = round_sig(result, self.significant_figures)
        return {self.idx: result}

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            value = round(data[self.idx] / self.scale)
        except KeyError:
            return addr_map
        if value << self.rshift > self.mask:
            raise OverflowError(
                f"Target value {value} when shifted 0x{value << self.rshift:02X} "
                f"is bigger than the target mask 0x{self.mask:02X}"
            )
        addr_map[self.address] &= ~self.mask
        addr_map[self.address] |= value << self.rshift
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamLookup(ParamModbus):
    address: int
    idx: str
    table: dict
    table_reversed: dict
    mask: int = 0xFFFF
    rshift: int = 0
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        try:
            assert block == self.block
            return {
                self.idx: self.table[
                    (addr_map[self.address] & self.mask) >> self.rshift
                ]
            }
        except (AssertionError, KeyError, TypeError):
            return {}

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            if type(data[self.idx]) == bytes or type(data[self.idx]) == bytearray:
                data[self.idx] = data[self.idx].decode()
        except KeyError:
            return addr_map
        try:
            value = self.table_reversed[data[self.idx]]
        except KeyError:
            return addr_map
        # Initialise the address map with the address if the address is not initialised already.
        # NOTE: This is required for the bit wise operations below.
        if self.address not in addr_map._buf:
            addr_map[self.address] = 0
        addr_map[self.address] &= ~self.mask
        addr_map[self.address] |= value << self.rshift
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamCType(ParamModbus):
    address: int
    idx: str
    data_type: str = "ushort"
    byte_order: str = ">"
    word_order: str = ">"
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        param_type = data_types[self.data_type]
        data = addr_map[self.address : self.address + ((param_type.size + 1) // 2)]
        if any((x is None for x in data)) or block != self.block:
            return {}
        if self.word_order != ">":
            data = data[::-1]
        data_bytes = struct.pack(self.byte_order + "H" * len(data), *data)
        if self.byte_order == ">":
            data_bytes = data_bytes[len(data_bytes) - param_type.size :]
        else:
            data_bytes = data_bytes[: param_type.size]
        param = struct.unpack(f"{self.byte_order}{param_type.format}", data_bytes)[0]
        return {self.idx: param}

    def encode(self, data: dict, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            value = data[self.idx]
        except KeyError:
            return addr_map
        param_type = data_types[self.data_type]
        data_bytes = bytearray(param_type.size)
        offset = 0
        if self.byte_order == ">":
            byte_order = "<"
        else:
            byte_order = ">"
        if param_type.format == "c":
            value = bytes(value, "utf-8")
        try:
            struct.pack_into(byte_order + param_type.format, data_bytes, offset, value)
        except struct.error as e:
            log.exception(e)
            log.warning(
                f"Failed to encode ParamCType {self.idx}. Which produced this error -> {e}"
            )
        if param_type.size > 1:
            cast = "H"
        elif param_type.format == "c":
            cast = "b"
        else:
            cast = param_type.format
        param = memoryview(data_bytes).cast(cast).tolist()
        if self.word_order == ">":
            param = param[::-1]
        addr_map[self.address : self.address + ((param_type.size + 1) // 2)] = param
        return addr_map

    def get_addresses(self) -> set:
        param_type = data_types[self.data_type]
        start = self.address
        end = self.address + ((param_type.size + 1) // 2)
        return {x for x in range(start, end)}

    def keys(self):
        return {self.idx}


@dataclass
class ParamCTypeScale(ParamCType):
    scale: float = 1.0
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        decoded = super().decode(addr_map, block)
        decoded[self.idx] = decoded[self.idx] * self.scale
        return decoded

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            return super().encode(
                {self.idx: int(data[self.idx] / self.scale)}, addr_map
            )
        except KeyError:
            return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamCTypeScaleModulus(ParamCType):
    modulus: int = 65535
    scale: float = 1.0
    invert_on_overflow: bool = False
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        decoded = super().decode(addr_map, block)
        val = decoded[self.idx] % self.modulus
        if val != decoded[self.idx] and self.invert_on_overflow:
            val = -val
        decoded[self.idx] = val * self.scale
        return decoded

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        return super().encode(int(data / self.scale) % self.modulus, addr_map)

    def keys(self):
        return {self.idx}


@dataclass
class ParamArray:
    address: int
    count: int
    idx: typing.Optional[str] = None
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or any(
            True
            for val in addr_map[self.address : self.address + self.count]
            if val is None
        ):
            return {}
        return {self.idx: addr_map[self.address : self.address + self.count]}

    def encode(self, data: dict, addr_map: AddressMapUint16) -> AddressMapUint16:
        if self.idx in data:
            if len(data[self.idx]) == self.count:
                addr_map[self.address : self.address + self.count] = data[self.idx]
        return addr_map


PARAM_TYPES = {
    "ParamForm": ParamForm,
    "ParamModbus": ParamModbus,
    "Param": Param,
    "ParamArray": ParamArray,
    "ParamBoolArray": ParamBoolArray,
    "ParamEnumBoolArray": ParamEnumBoolArray,
    "ParamText": ParamText,
    "ParamBits": ParamBits,
    "ParamBit": ParamBit,
    "ParamBool": ParamBool,
    "ParamMask": ParamMask,
    "ParamOffset": ParamOffset,
    "ParamMaskBool": ParamMaskBool,
    "ParamMaskScale": ParamMaskScale,
    "ParamLookup": ParamLookup,
    "ParamCType": ParamCType,
    "ParamCTypeScale": ParamCTypeScale,
    "ParamCTypeScaleModulus": ParamCTypeScaleModulus,
    "Modbus.ParamForm": ParamForm,
    "Modbus.ParamModbus": ParamModbus,
    "Modbus.Param": Param,
    "Modbus.ParamArray": ParamArray,
    "Modbus.ParamBoolArray": ParamBoolArray,
    "Modbus.ParamEnumBoolArray": ParamEnumBoolArray,
    "Modbus.ParamText": ParamText,
    "Modbus.ParamBits": ParamBits,
    "Modbus.ParamBit": ParamBit,
    "Modbus.ParamBool": ParamBool,
    "Modbus.ParamMask": ParamMask,
    "Modbus.ParamOffset": ParamOffset,
    "Modbus.ParamMaskBool": ParamMaskBool,
    "Modbus.ParamMaskScale": ParamMaskScale,
    "Modbus.ParamLookup": ParamLookup,
    "Modbus.ParamCType": ParamCType,
    "Modbus.ParamCTypeScale": ParamCTypeScale,
    "Modbus.ParamCTypeScaleModulus": ParamCTypeScaleModulus,
}


class AddressMap:
    def __init__(self, buffer: dict = None):
        if buffer is None:
            self._buf = {}
        else:
            self._buf = buffer

    def __getitem__(self, addr):
        """
        :param addr: Address int or slice of addresses to return
        :return:
        """
        if isinstance(addr, int):
            if addr < 0:
                raise TypeError("Address should be >= 0.")
            return self._buf[addr]
        elif isinstance(addr, slice):
            return [self._buf.get(i) for i in range(*slice_list(addr))]
        else:
            raise TypeError("Address has unsupported type")

    def __setitem__(self, key, value):
        """
        :param key: Int of the address
        :param value: Set the value of the item if the value is not None
        :return:
        """
        if isinstance(key, slice):
            for index, addr in enumerate(range(*slice_list(key))):
                if value[index] is not None:
                    self._buf[addr] = value[index]
        else:
            if value is not None:
                self._buf[key] = value

    def __contains__(self, item):
        return item in self._buf

    def __delitem__(self, key):
        try:
            del self._buf[key]
        except KeyError:
            pass

    def __delslice__(self, i, j):
        for x in range(i, j):
            try:
                del self._buf[x]
            except KeyError:
                pass

    def __bool__(self):
        return bool(self._buf)

    def __eq__(self, another: AddressMap):
        """
        Used for tests to compare the buffers of two address maps.

        :param another: Address map to compare buffers with
        :returns: True if buffers are equal, False otherwise
        """
        return self._buf == another._buf

    def merge(self, addr: AddressMap):
        """
        Merges another address map into this existing address map

        :param addr: Address Map to merge into the selected map.
        :return: Merged Address Map
        """
        overlap = set(self._buf.keys()).intersection(set(addr._buf.keys()))
        if overlap:
            raise ValueError(
                "Cannot join AddressMap with overlapping addresses: {}".format(overlap)
            )

        self._buf.update(addr._buf)

    def update(self, addr: AddressMap, force: bool = False):
        """
        Updates another address map with this existing address map

        :param addr: Address Map to update the selected map with.
        :param force: If true the address map will be forced to update with the new address maps keys and values. If
        false the address map will not update if keys in the new address map did not exist in the base. Defaults to
        false.
        :return: Merged Address Map
        """
        if set(addr._buf).difference(set(self._buf)) and not force:
            raise ValueError(
                "Cannot add new keys to the address map. If you require this functionality enable the force option."
            )
        self._buf.update(addr._buf)

    def save_block(self, start_addr, values):
        for index, itm in enumerate(values):
            self._buf[start_addr + index] = itm

    def __repr__(self):
        return f"AddressMap: {self._buf}"

    def copy(self):
        return self.__class__(self._buf)


class AddressMapUint16(AddressMap):
    def __setitem__(self, key, value):
        """
        :param key: Int of the address
        :param value: Set the value of the item if the value is not None
        :return:
        """
        if isinstance(key, slice):
            if any(
                x
                for x in slice_list(key)
                if x is not None and not (0 <= x < 1 << 16) and not isinstance(x, int)
            ):
                raise OverflowError("Values provided are not UINT16 compatible")
        else:
            if (
                value is not None
                and not (0 <= value < 1 << 16)
                and not isinstance(value, int)
            ):
                raise OverflowError("Value provided is not UINT16 compatible")
        super().__setitem__(key, value)
