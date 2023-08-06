from __future__ import annotations
import typing
import time
from datetime import datetime
from dataclasses import dataclass, field

from pyaware.commands import (
    ValidateIn,
    ValidateRange,
    ValidationError,
    InvalidCommandData,
    TopicTask,
)
import pyaware.triggers.write

if typing.TYPE_CHECKING:
    from pyaware.protocol.imac2.modules import ImacModule


@dataclass
class WriteParam:
    parameter: str
    add: int = 0
    override: typing.Union[int, None] = None
    key: str = ""

    def __repr__(self):
        return "Writing parameter"

    async def _async_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        new_data = self._do(cmd)
        await imac_module.write_parameters({self.parameter: new_data})
        cmd["parameters_written"][self.parameter] = new_data

    def _sync_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        new_data = self._do(cmd)
        imac_module.write_parameters({self.parameter: new_data})
        cmd["parameters_written"][self.parameter] = new_data

    def _do(self, cmd):
        if self.override is not None:
            return self.override
        if self.key:
            val = cmd["data"][self.key]
        else:
            val = list(cmd["data"].values())
            if len(val) > 1:
                raise InvalidCommandData(
                    "Need to specify key if multiple data keys are given"
                )
            val = val[0]
        val = val + self.add
        return val

    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        return self._async_do(cmd, imac_module, **kwargs)


@dataclass
class WriteParamTimestamp:
    parameter: str
    add: int = 0
    override: typing.Union[int, None] = None
    key: str = ""

    def __repr__(self):
        return "Writing parameter timestamped"

    async def _async_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        new_data = self._do(cmd)
        await imac_module.write_parameters_no_check({self.parameter: new_data})
        cmd["timestamp"] = datetime.utcnow()
        await imac_module.protocol.wait_on_bit(0x409, 4, False)
        await imac_module.protocol.check_bit(0x409, 7, False)
        cmd["parameters_written"][self.parameter] = new_data

    def _do(self, cmd):
        if self.override is not None:
            return self.override
        if self.key:
            val = cmd["data"][self.key]
        else:
            val = list(cmd["data"].values())
            if len(val) > 1:
                raise InvalidCommandData(
                    "Need to specify key if multiple data keys are given"
                )
            val = val[0]
        val = val + self.add
        return val

    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        return self._async_do(cmd, imac_module, **kwargs)


@dataclass
class ReadParam:
    parameter: str

    def __repr__(self):
        return "Reading parameter"

    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        """
        Reads a parameter from an imac module
        :param cmd:
        :param imac_module:
        :param kwargs:
        :return:
        """
        return self._async_do(cmd, imac_module, **kwargs)

    async def _async_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        params = await imac_module.read_parameters({self.parameter})
        cmd["parameters_read"].update(params)


class ValidateParams:
    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        """
        Reads a parameter from an imac module
        :param cmd:
        :param imac_module:
        :param kwargs:
        :return:
        """
        invalid = {
            k
            for k in cmd["data"]["parameters"]
            if k not in imac_module.parameters.get("block", {})
        }
        if invalid:
            raise InvalidCommandData(
                f"Parameters do not exist in imac module {','.join(invalid)}"
            )

    def __repr__(self):
        return "Validating Parameters"


class ReadParams:
    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        """
        Reads a parameter from an imac module
        :param cmd:
        :param imac_module:
        :param kwargs:
        :return:
        """
        return self._async_do(cmd, imac_module, **kwargs)

    async def _async_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        params = await imac_module.read_parameters(set(cmd["data"]["parameters"]))
        cmd["parameters_read"].update(params)

    def __repr__(self):
        return "Reading Parameters"


@dataclass
class WriteParams:
    parameters: set = field(default_factory=set)

    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        """
        Reads a parameter from an imac module
        :param cmd:
        :param imac_module:
        :param kwargs:
        :return:
        """
        return self._async_do(cmd, imac_module, **kwargs)

    async def _async_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        invalid_params = set(cmd["data"]).difference(self.parameters)
        if invalid_params:
            raise InvalidCommandData(
                f"Command parameters provided are not valid: {invalid_params}"
            )
        await imac_module.write_parameters(cmd["data"])
        cmd["parameters_written"].update(cmd["data"])

    def __repr__(self):
        return "Writing Parameters"


class WriteAndValidateParams:
    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        """
        Reads a parameter from an imac module
        :param cmd:
        :param imac_module:
        :param kwargs:
        :return:
        """
        return self._async_do(cmd, imac_module, **kwargs)

    async def _async_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        await imac_module.write_parameters(cmd["data"])
        read_data = await imac_module.read_parameters(set(cmd["data"]))
        mismatched = [
            (param, value)
            for param, value in cmd["data"].items()
            if value != read_data[param]
        ]
        if mismatched:
            msg = "\n".join(
                f"Parameter '{param}' read back as {read_data[param]}, expected {value}"
                for param, value in mismatched
            )
            raise ValidationError(msg)

    def __repr__(self):
        return "Writing and Validating Parameters"


class GetParameters:
    async def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        command_params = set(cmd["data"]["parameters"])
        invalid = command_params.difference(imac_module.config["parameters"])
        if invalid:
            raise InvalidCommandData(
                f"Parameters do not exist in imac module {','.join(invalid)}"
            )
        read_data = await imac_module.read_parameters(command_params)
        invalid = command_params.difference(set(read_data))
        if invalid:
            raise IOError(f"Failed to read parameters {','.join(invalid)}")
        cmd["return_values"] = read_data
        imac_module.update_specs()

    def __repr__(self):
        return "Validating and reading parameters"


class SetParameters:
    async def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        try:
            pyaware.triggers.write.run_triggers(
                imac_module.triggers["write"], cmd["data"]
            )
        except AssertionError as e:
            raise InvalidCommandData("".join(e.args)) from e
        await imac_module.write_parameters(cmd["data"])
        read_data = await imac_module.read_parameters(set(cmd["data"]))
        if self.is_mismatched(cmd["data"], read_data):
            # Retry reading the blocks
            read_data = await imac_module.read_parameters(set(cmd["data"]))
            mismatched = self.is_mismatched(cmd["data"], read_data)
            if mismatched:
                msg = "\n".join(
                    f"Parameter '{param}' read back as {read_data[param]}, expected {value}"
                    for param, value in mismatched
                )
                raise ValidationError(msg)
        imac_module.update_specs()

    @staticmethod
    def is_mismatched(source, destination) -> list:
        return [
            (param, value)
            for param, value in source.items()
            if value != destination[param]
        ]

    def __repr__(self):
        return "Writing and validating parameters"


@dataclass
class ValidateParam:
    parameter: str

    def __repr__(self):
        return "Validating parameter"

    def do(self, cmd: dict, **kwargs):
        read_value = cmd["parameters_read"][self.parameter]
        written_value = cmd["parameters_written"][self.parameter]
        if read_value != written_value:
            raise ValidationError(
                f"Parameter '{self.parameter}' read back as {read_value}, expected {written_value}"
            )


@dataclass
class UpdateMeta:
    parameter: str

    def __repr__(self):
        return "Updating metadata"

    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        imac_module.current_state[self.parameter] = cmd["parameters_read"][
            self.parameter
        ]


@dataclass
class UpdateSpecs:
    def __repr__(self):
        return "Updating module specifications"

    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        imac_module.update_specs()


@dataclass
class RespondParam:
    parameter: str
    read_key: str = ""

    def __repr__(self):
        return "Building Response"

    def do(self, cmd: dict, **kwargs):
        key = self.read_key or self.parameter
        cmd["return_values"][self.parameter] = cmd["parameters_read"][key]


@dataclass
class RespondParamsAll:
    def __repr__(self):
        return "Building Response"

    def do(self, cmd: dict, **kwargs):
        cmd["return_values"] = cmd["parameters_read"]


@dataclass
class WaitParam:
    parameter: str
    result: int
    mask: int = 0xFFFF
    timeout: typing.Union[int, None] = None
    error: typing.Union[int, None] = None

    def __repr__(self):
        return "Waiting for result"

    async def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        start = time.time()
        while True:
            resp = await imac_module.read_parameters({self.parameter})
            if resp[self.parameter] == self.result:
                break
            if time.time() - start > self.timeout:
                raise TimeoutError(
                    f"Parameter {self.parameter} failed to read in {self.timeout}s"
                )


@dataclass
class CheckParam:
    parameter: str
    result: int
    mask: int = 0xFFFF
    timeout: typing.Union[int, None] = None
    error: typing.Union[int, None] = None

    def __repr__(self):
        return "Checking parameter value"

    async def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        resp = await imac_module.read_parameters({self.parameter})
        if resp[self.parameter] != self.result:
            raise ValidationError(
                f"Parameter {self.parameter} is {resp[self.parameter]} expected {self.result}"
            )


def write_and_validate(parameter: str):
    return [WriteParam(parameter), ReadParam(parameter), ValidateParam(parameter)]


gasguard_2 = {
    "action-reset-to-idle": [
        CheckParam("command-register-result", result=0),
        WriteParam("command-register-code", override=0x00),
        WriteParam("command-register-result", override=1 << 7),
    ],
    "action-catalytic-latch-reset": [
        CheckParam("command-register-result", result=0),
        WriteParam("command-register-code", override=0x1E),
        WriteParam("command-register-result", override=1 << 7),
    ],
    "action-remote-telemetry-test": [
        CheckParam("command-register-result", result=0),
        WriteParam("command-register-code", override=0x2D),
        WriteParam("command-register-result", override=1 << 7),
    ],
    "get-linearity-test-time": [
        ReadParam("linearity-test-time"),
        RespondParam("linearity-test-time"),
    ],
    "get-rtc-time": [
        ReadParam("rtc-time"),
        RespondParam("rtc-time"),
    ],
    "get-t90-test-time": [
        ReadParam("t90-test-time"),
        RespondParam("t90-test-time"),
    ],
    "get-serial-detector": [
        ReadParam("detector-serial-number"),
        RespondParam("detector-serial-number"),
    ],
    "get-telemetry-test-time": [
        ReadParam("telemetry-test-time"),
        RespondParam("telemetry-test-time"),
    ],
    "set-aim-compatibility-mode": [
        ValidateIn(range(2)),
        *write_and_validate("aim-compatibility-mode"),
        UpdateMeta("aim-compatibility-mode"),
        # TODO Should require update to specs for the AIM vs GG2 mode for power
        UpdateSpecs(),
    ],
    "set-exception-trigger": [
        ValidateIn(range(20001)),
        *write_and_validate("exception-trigger"),
    ],
    # TODO investigate
    "set-imac-address-rtgm": [
        ValidateIn(range(1, 41)),
        WriteParam("address-power", override=0),
        WriteParam("address-analog", add=40),
        WriteParam("address-flags"),
        ReadParam("address-flags"),
        ReadParam("address-analog"),
        ReadParam("address-power"),
        UpdateMeta("address-flags"),
        UpdateMeta("address-analog"),
        UpdateMeta("address-power"),
        UpdateSpecs(),
        ValidateParam("address-flags"),
        ValidateParam("address-analog"),
        ValidateParam("address-power"),
    ],
    "set-gas-point-1": [
        ValidateIn(range(20001)),
        *write_and_validate("set-point-1"),
    ],
    "set-gas-point-2": [
        ValidateIn(range(20001)),
        *write_and_validate("set-point-2"),
    ],
    "set-gas-point-3": [
        ValidateIn(range(20001)),
        *write_and_validate("set-point-3"),
    ],
    "set-gas-points": [
        ValidateIn(range(20001), key="set-point-1"),
        ValidateIn(range(20001), key="set-point-2"),
        ValidateIn(range(20001), key="set-point-3"),
        WriteParams(parameters={"set-point-1", "set-point-2", "set-point-3"}),
        ReadParam("set-point-1"),
        ValidateParam("set-point-1"),
        ValidateParam("set-point-2"),
        ValidateParam("set-point-3"),
    ],
    "set-healthy-state": [
        ValidateIn(range(5)),
        *write_and_validate("healthy-config"),
    ],
    "set-hysteresis": [
        ValidateIn(range(16)),
        *write_and_validate("hysteresis-config"),
    ],
    "set-imac-address-analog": [
        ValidateIn(range(256)),
        *write_and_validate("address-analog"),
        UpdateMeta("address-analog"),
        UpdateSpecs(),
    ],
    "set-imac-address-flags": [
        ValidateIn(range(256)),
        *write_and_validate("address-flags"),
        UpdateMeta("address-flags"),
        UpdateSpecs(),
    ],
    "set-imac-address-power": [
        ValidateIn(range(256)),
        *write_and_validate("address-power"),
        UpdateMeta("address-power"),
        UpdateSpecs(),
    ],
    "set-imac-address-bypass": [
        ValidateIn(list(range(81, 121)) + [0]),
        *write_and_validate("address-bypass"),
        UpdateSpecs(),
    ],
    "set-imac-address-rtc": [
        ValidateIn([x for x in range(256) if x % 4 != 3]),
        *write_and_validate("address-rtc"),
    ],
    "set-power-point-alarm": [
        ValidateRange(0, 24),
        *write_and_validate("power-point-alarm"),
    ],
    "set-power-point-trip": [
        ValidateRange(0, 24),
        *write_and_validate("power-point-trip"),
    ],
    "set-power-points": [
        ValidateRange(8, 24, key="power-point-trip"),
        ValidateRange(10, 24, key="power-point-alarm"),
        WriteParams(parameters={"power-point-trip", "power-point-alarm"}),
        ReadParam("power-point-trip"),
        ValidateParam("power-point-trip"),
        ValidateParam("power-point-alarm"),
    ],
    "set-warmup-config": [ValidateIn(range(2)), *write_and_validate("warmup-config")],
    "remote-bypass": [
        ValidateIn(range(1, 41), key="address"),
        ValidateIn(range(2), key="value"),
        TopicTask(
            topic="remote_bypass_gg2",
            key_map={"logical_address": "address", "value": "value"},
        ),
    ],
}
