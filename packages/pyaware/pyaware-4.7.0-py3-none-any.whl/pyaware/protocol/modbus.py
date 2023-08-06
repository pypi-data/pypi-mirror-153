from __future__ import annotations
import logging
import typing

from pymodbus.server.asyncio import ModbusTcpServer
from pymodbus.datastore import ModbusServerContext
from pymodbus.datastore import ModbusSlaveContext, ModbusSparseDataBlock

import pyaware.data_types.modbus
import pyaware.triggers.process
from pyaware import events
import pyaware.triggers
import pyaware.data_types
import pyaware.aggregations
import pyaware.config
from pyaware.data_types.modbus import AddressMapUint16

log = logging.getLogger(__file__)

if typing.TYPE_CHECKING:
    pass


class RequestException(ValueError):
    pass


class IllegalFunction(RequestException):
    pass


class IllegalDataAddress(RequestException):
    pass


class IllegalDataValue(RequestException):
    pass


class MemoryParityError(IOError):
    pass


class SlaveDeviceFailure(IOError):
    pass


class AcknowledgeError(IOError):
    pass


class DeviceBusy(IOError):
    pass


class NegativeAcknowledgeError(IOError):
    pass


class GatewayPathUnavailable(IOError):
    pass


class GatewayDeviceFailedToRespond(IOError):
    pass


modbus_exception_codes = {
    1: IllegalFunction,
    2: IllegalDataAddress,
    3: IllegalDataValue,
    4: SlaveDeviceFailure,
    5: AcknowledgeError,
    6: DeviceBusy,
    7: NegativeAcknowledgeError,
    8: MemoryParityError,
    10: GatewayPathUnavailable,
    11: GatewayDeviceFailedToRespond,
    12: ConnectionError,
}


class ModbusException(IOError):
    pass


@events.enable
class ModbusAsyncTcpServer:
    """
    Asynchronous Modbus Server to serve over TCP/IP."
    """

    def __init__(
        self,
        host: str,
        server_id: str,
        coil_register_blocks: typing.List = None,
        discrete_input_register_blocks: typing.List = None,
        holding_register_blocks: typing.List = None,
        input_register_blocks: typing.List = None,
        port: int = 502,
    ):
        self.host = host
        self.port = port
        self.server_id = server_id
        # Initialises data blocks to ensure bounds are maintained
        self.ir = self._initialise_addresses(input_register_blocks)
        self.ir_blocks = ModbusSparseDataBlock(self.ir._buf)
        self.hr = self._initialise_addresses(holding_register_blocks)
        self.hr_blocks = ModbusSparseDataBlock(self.hr._buf)
        self.di = self._initialise_addresses(discrete_input_register_blocks)
        self.di_blocks = ModbusSparseDataBlock(self.di._buf)
        self.coil = self._initialise_addresses(coil_register_blocks)
        self.coil_blocks = ModbusSparseDataBlock(self.coil._buf)
        # TODO: Work out a method to set unused data blocks to nothing.
        # Initialise slave context
        self.block_store = self.ModbusSlaveContext(
            ir=self.ir_blocks,
            hr=self.hr_blocks,
            di=self.di_blocks,
            co=self.coil_blocks,
            zero_mode=True,
        )
        self.server = None
        self.context = self._initialise_data_block()
        # Subscribes to server update events
        events.subscribe(self.update_modbus_server, topic=f"update_server/{id(self)}")
        events.subscribe(
            self.write_request, topic=f"server_write/{id(self.block_store)}"
        )

    # --------------------------------------------------------------------
    # Pymodbus patch to get data from server writes
    # --------------------------------------------------------------------
    @events.enable
    class ModbusSlaveContext(ModbusSlaveContext):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def setValues(self, fx, address, values):
            if not self.zero_mode:
                address = address + 1
            events.publish(
                f"server_write/{id(self)}", start_addr=address, values=values
            )
            self.store[self.decode(fx)].setValues(address, values)

    # --------------------------------------------------------------------

    def _initialise_addresses(
        self, blocks: typing.List, initialise_as: int = 0
    ) -> AddressMapUint16:
        """
        Initialises addresses to 0 based on a set of address blocks.

        :param blocks: Address blocks in the format [[start_addr1, end_addr1], [start_addr2, end_addr2], ...]
        :param initialise_as: Value to initialise the addresses to as an integer. Defaults to 0.
        :return: Initialised address map
        """
        if blocks is None:
            return pyaware.data_types.modbus.AddressMapUint16(
                {i: initialise_as for i in range(0, 65536)}
            )
        map = {}
        for block in blocks:
            d = {k: initialise_as for k in range(block[0], block[1] + 1)}
            map.update(d)
        return pyaware.data_types.modbus.AddressMapUint16(map)

    def _initialise_data_block(self):
        """
        Initialises data block of modbus server to self.block values with device config mapping information
        """
        context = ModbusServerContext(slaves=self.block_store, single=True)
        return context

    async def update_modbus_server(
        self, addr_map: AddressMapUint16, register: str
    ) -> None:
        """
        Updates the current block of values with the received address map values

        :param addr_map: Address Map of values to update the server with.
        """
        if register == "holding":
            self.hr.update(addr_map)
            self.hr_blocks.values.update(self.hr._buf)
        if register == "input":
            self.ir.update(addr_map)
            self.ir_blocks.values.update(self.ir._buf)
        elif register == "discrete":
            self.di.update(addr_map)
            self.di_blocks.values.update(self.di._buf)
        elif register == "coils":
            self.coil.update(addr_map)
            self.coil_blocks.values.update(self.coil._buf)
        return

    async def write_request(self, start_addr, values):
        log.info(
            f"Request to write to server {self.server_id} received at start address: {start_addr}"
        )
        await events.publish(
            f"device_update/{id(self)}",
            start_addr=start_addr,
            values=values,
            server_id=self.server_id,
        ).all()

    async def start(self):
        """
        Start Modbus TCP Server
        """
        log.info("Starting Modbus TCP Server at %s:%s." % (self.host, self.port))
        self.server = ModbusTcpServer(
            context=self.context, address=(self.host, self.port)
        )
        await self.server.serve_forever()
