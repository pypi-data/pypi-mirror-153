import typing
import datetime
from pathlib import Path

from pyaware.events import subscribe, enable
from pyaware.controllers.modbus import ModbusDevice
from pyaware import log

numeric = typing.Union[int, float]


@enable
class ComApInteliliteMRS16(ModbusDevice):
    def __init__(
        self,
        client,
        device_id: str,
        config: Path,
        unit=0,
        address_shift=0,
        poll_intervals: typing.Optional[typing.Dict[str, numeric]] = None,
    ):
        super().__init__(
            client=client,
            device_id=device_id,
            config=config,
            unit=unit,
            address_shift=address_shift,
            poll_intervals=poll_intervals,
        )
        self.fault_reset = {
            "command-code": 1,
            "argument": 2295,
            "return-value": 150470656,
        }
        for param, meta in self.parameter_metadata.items():
            param_kind = meta.get("kind", "")
            if param_kind == "alarm":
                subscribe(
                    self.acknowledge_alarms,
                    topic=f"parameter_trigger/{self.device_id}/{param}",
                )

    async def execute_command(self, command: dict) -> bool:
        """
        Comap Command Procedure:\n
        1. (Optional) If the unit has a password this will be written to register 4211 using function code 6
        (Write Single Holding Register). A password requirement is dependent upon configuration access rules.\n
        2. Write command argument to registers 4207-4208. Using function code 16 (Write Multiple Holding Registers).\n
        3. Write command code into register 4209. Using function code 6.\n
        4. Read command return value from registers (4207-4208). Using function code 3 (Read Holding Registers).
        This determines command success or failure.\n
        5. Check the return value against the the expected return value. If an error was received it should have
        returned either of the following,
        0x00000001 - Invalid Argument
        0x00000002 - Command Refused\n
        :param command: Vaild ComAp command as a dictionary [str, hex] in the format,
        {"command-code": 0xXX, "argument": 0xXXXXXXXX, "return-value": 0xXXXXXXXX}
        """
        # Write password
        try:
            # Write fault reset command argument
            await self.process_write(
                "holding",
                {"command-argument-register": command["argument"]},
            )
            # Write command code
            await self.process_write(
                "holding",
                {"command-code-register": command["command-code"]},
            )
            # Read command value
            command_argument_register = self.parameters["command-argument-register"]
            return_value = await self.read_registers(
                self.read_handles.get("holding"),
                command_argument_register.form.address,
                2,
            )
            return_value = self.parameters["command-argument-register"].decode(
                return_value
            )["command-argument-register"]
        except BaseException as e:
            log.exception(f"Failed to reset alarms -> {e}")
            return False

        if return_value == command["return-value"]:
            log.info(f"Successfully acknowledged Comap Device {self.device_id} alarms")
            return True
        elif return_value == 0x00010000:
            log.warning(
                f"Invalid Argument sent to Comap Device {self.device_id} while attempting alarm "
                f"acknowledgment"
            )
            return False
        elif return_value == 0x00020000:
            log.warning(
                f"Command refused while attempting Comap Device {self.device_id} alarm acknowledgment"
            )
            return False
        else:
            log.exception(
                f"Unknown return value while attempting to acknowledge Comap Device {self.device_id} "
                f"alarms -> {return_value}"
            )
            return False

    async def acknowledge_alarms(
        self, data: bool, timestamp: datetime.datetime
    ) -> None:
        """
        Alarms are set to active and cleared as inactive by the controller. Users have input on these alarms as well,
        they are required to acknowledge each alarm event.\n
        Comap alarms have four states in which to report a boolean value via modbus,\n
        1. Active and Unacknowledged ->  Reports True
        2. Active and Acknowledged -> Reports True
        3. Inactive and Unacknowledged -> Reports True
        4. Inactive and Acknowledged -> Reports False\n
        The third state raises an issue. As the alarm is cleared by the controller but is still reported as active
        via modbus. So if we acknowledge each alarm as they come in we will receive accurate alarm information.\n
        NOTE: This does not clear active alarms. It only acknowledges that the alarms have happened.\n
        :param data: The current state of the triggered alarm as a boolean.
        :param timestamp: Timestamp at which the alarm was triggered.
        """
        if data:
            log.info("Acknowledging comap alarms")
            command_status = await self.execute_command(self.fault_reset)
            if not command_status:
                log.warning(
                    f"Command Acknowledge alarms on Comap Device {self.device_id} failed to execute."
                )
        return None
