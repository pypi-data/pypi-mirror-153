from __future__ import annotations
import sys
import enum
import typing
from datetime import datetime
import traceback
import logging
from dataclasses import dataclass, field
from pathlib import Path

import pyaware.events
from pyaware import async_wrap, from_coroutine, events

number = typing.Union[int, float]

log = logging.getLogger(__name__)


class CmdResponse(enum.IntEnum):
    ACK = 0
    PROGRESS = 1
    SUCCESS = 2
    ERROR = 3
    INVALID_DESTINATION = 4
    INVALID_COMMAND_NAME = 5
    INVALID_COMMAND_DATA = 6
    IO_ERROR = 7


class InvalidDestination(ValueError):
    pass


class InvalidCommandName(ValueError):
    pass


class InvalidCommandData(ValueError):
    pass


@dataclass
class Execute:
    """
    Basic action contracts to execute a handle with the command sequence
    """

    handle: typing.Callable
    return_id: typing.Union[str, None] = None
    kwargs: dict = field(default_factory=dict)
    from_read_params: dict = field(default_factory=dict)
    from_command_params: dict = field(default_factory=dict)

    def _do(self, cmd):
        kwargs = {
            k: cmd["parameters_read"][v]
            for k, v in self.from_read_params.items()
            if v in cmd["parameters_read"]
        }
        kwargs.update(
            {
                k: cmd["data"][v]
                for k, v in self.from_command_params.items()
                if v in cmd["data"]
            }
        )
        kwargs.update(self.kwargs)
        return kwargs

    async def do(self, cmd, *args, **kwargs):
        ret_val = await async_wrap(self.handle(**self._do(cmd)))
        if self.return_id:
            cmd["parameters_read"][self.return_id] = ret_val

    def __repr__(self):
        return f"Executing {self.handle.__name__}: -> {self.return_id}"


@dataclass
class Commands:
    commands: typing.Dict[str, list]
    sub_commands: typing.Dict[str, Commands] = field(default_factory=dict)
    meta_kwargs: typing.Union[dict, None] = field(default_factory=dict)
    device_id: str = ""
    command_destination: typing.Union[str, typing.List[str]] = ""

    def __post_init__(self):
        events.subscribe(self.on_command, topic=f"mqtt_command/{self.device_id}")
        if isinstance(self.command_destination, str):
            self.command_destination = [self.command_destination]

    def register(self, idx, cmd: list):
        self.commands[idx] = cmd

    def update(self, cmds: typing.Dict[str, list]):
        self.commands.update(cmds)

    def get_command(self, cmd: dict, kwargs: dict):
        kwargs.update(self.meta_kwargs)
        command_destination = cmd.get("destination", [])

        # If the destination is a string then convert it to an array
        if type(command_destination) is str:
            command_destination = list(Path(command_destination).parts)

        if command_destination and command_destination != self.command_destination:
            sub_command = command_destination.pop(0)
            cmd["destination"] = command_destination
            try:
                target = self.sub_commands[sub_command]
            except KeyError:
                raise InvalidDestination
            return target.get_command(cmd, kwargs)
        else:
            try:
                return self.commands[cmd["name"]]
            except KeyError:
                raise InvalidCommandName

    @staticmethod
    def cmd_error(cmd_id, msg="", error_code: CmdResponse = CmdResponse.ERROR):
        resp = {
            "id": cmd_id,
            "type": error_code,
            "timestamp": datetime.utcnow(),
        }
        if msg:
            resp["message"] = msg
        return resp

    @staticmethod
    def progress(cmd_id, msg=""):
        resp = {
            "id": cmd_id,
            "type": CmdResponse.PROGRESS,
            "timestamp": datetime.utcnow(),
        }
        if msg:
            resp["message"] = msg
        return resp

    @staticmethod
    def ack(cmd_id):
        return {
            "id": cmd_id,
            "type": CmdResponse.ACK,
            "timestamp": datetime.utcnow(),
        }

    @staticmethod
    def success(cmd_id, cmd):
        timestamp = cmd.pop("timestamp", datetime.utcnow())
        if cmd.get("return_values"):
            return {
                "id": cmd_id,
                "type": CmdResponse.SUCCESS,
                "timestamp": timestamp,
                "data": cmd["return_values"],
            }
        else:
            return {
                "id": cmd_id,
                "type": CmdResponse.SUCCESS,
                "timestamp": timestamp,
            }

    async def on_command(self, data, timestamp):
        log.info(f"Command received for {self.device_id}: {data}")
        await self.execute(data, self.on_callback)

    def on_callback(self, data):
        events.publish(
            f"mqtt_command_response",
            data=data,
            timestamp=datetime.utcnow(),
            device_id=self.device_id,
        )

    async def execute(self, cmd, response_cbf: typing.Callable = print):
        kwargs = {}
        cmd["parameters_read"] = {}
        cmd["parameters_written"] = {}
        cmd["return_values"] = {}
        response_cbf(self.ack(cmd["id"]))

        try:
            target = self.get_command(cmd, kwargs)
            if isinstance(target, list):
                await self.execute_actions(cmd, response_cbf, target, **kwargs)
            else:
                await async_wrap(
                    target.execute(cmd, response_cbf=response_cbf, **kwargs)
                )
            log.info(f"Command completed successfully for {self.device_id}: {cmd}")
        except InvalidDestination:
            log.info(f"Command has invalid destination {self.device_id}: {cmd}")
            response_cbf(
                self.cmd_error(cmd["id"], error_code=CmdResponse.INVALID_DESTINATION)
            )
        except InvalidCommandData:
            log.info(f"Command has invalid data {self.device_id}: {cmd}")
            response_cbf(
                self.cmd_error(cmd["id"], error_code=CmdResponse.INVALID_COMMAND_DATA)
            )
        except InvalidCommandName:
            log.info(f"Command has invalid command name {self.device_id}: {cmd}")
            response_cbf(
                self.cmd_error(cmd["id"], error_code=CmdResponse.INVALID_COMMAND_NAME)
            )
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tbe = traceback.TracebackException(
                exc_type,
                exc_value,
                exc_tb,
            )
            log.warning(
                f"Command failed to execute {self.device_id}: {cmd} {''.join(tbe.format())}"
            )
            response_cbf(self.cmd_error(cmd["id"], "".join(tbe.format())))

    async def execute_actions(
        self, cmd, response_cbf: typing.Callable, actions: list, **kwargs
    ):
        cmd_id = cmd["id"]
        for action in actions:
            await async_wrap(response_cbf(self.progress(cmd_id, repr(action))))
            await async_wrap(action.do(cmd, **kwargs))
        await async_wrap(response_cbf(self.success(cmd_id, cmd)))


@dataclass
class ValidateIn:
    iterable: typing.Iterable
    key: str = ""
    optional: bool = False

    def do(self, cmd: dict, *args, **kwargs):
        if self.key:
            try:
                val = cmd["data"][self.key]
            except KeyError:
                if self.optional:
                    return
                else:
                    raise InvalidCommandData(
                        f"Key {self.key} not present in command payload {cmd['data']}"
                    )
        else:
            val = list(cmd["data"].values())
            if len(val) > 1:
                raise InvalidCommandData(
                    "Need to specify key if multiple data keys are given"
                )
            val = val[0]
        if val not in self.iterable:
            raise InvalidCommandData(f"Data is invalid")

    def __repr__(self):
        return "Validating data"


@dataclass
class ValidateRange:
    start: typing.Union[int, float]
    stop: typing.Union[int, float]
    key: str = ""
    optional: bool = False
    allow_zero: bool = False

    def do(self, cmd: dict, *args, **kwargs):
        if self.key:
            try:
                val = cmd["data"][self.key]
            except KeyError:
                if self.optional:
                    return
                else:
                    raise InvalidCommandData(
                        f"Key {self.key} not present in command payload {cmd['data']}"
                    )
        else:
            val = list(cmd["data"].values())
            if len(val) > 1:
                raise InvalidCommandData(
                    "Need to specify key if multiple data keys are given"
                )
            val = val[0]
        try:
            if not (self.start <= val <= self.stop):
                if self.allow_zero and val == 0:
                    return
                raise InvalidCommandData(
                    f"Data {val} is not in range {self.start} - {self.stop}"
                )
        except TypeError:
            raise InvalidCommandData(f"Value is not a valid number")

    def __repr__(self):
        return "Validating data"


@dataclass
class ValidateHandle:
    handle: typing.Callable
    key: str = ""

    def do(self, cmd: dict, *args, **kwargs):
        if self.key:
            val = cmd["data"][self.key]
        else:
            val = list(cmd["data"].values())
            if len(val) > 1:
                raise InvalidCommandData(
                    "Need to specify key if multiple data keys are given"
                )
            val = val[0]
        try:
            if not self.handle(val):
                raise InvalidCommandData("Handle did not return truthy value")
        except:
            raise InvalidCommandData(f"Data is invalid")

    def __repr__(self):
        return "Validating data"


@dataclass
class ValidateAnyHandle:
    handles: [typing.Callable]
    key: str = ""

    def do(self, cmd: dict, *args, **kwargs):
        if self.key:
            val = cmd["data"][self.key]
        else:
            val = list(cmd["data"].values())
            if len(val) > 1:
                raise InvalidCommandData(
                    "Need to specify key if multiple data keys are given"
                )
            val = val[0]
        try:
            if not any(handle(val) for handle in self.handles):
                raise InvalidCommandData("Handle did not return truthy value")
        except:
            raise InvalidCommandData(f"Data is invalid")

    def __repr__(self):
        return "Validating data"


@dataclass
class ValidateGroup:
    validators: typing.Collection[
        typing.Union[ValidateIn, ValidateRange, ValidateHandle, ValidateAnyHandle]
    ]
    exclusive: bool = True

    def do(self, cmd: dict, *args, **kwargs):
        valids = [x for x in self.validators if x.key in cmd["data"]]
        if self.exclusive and len(valids) < len(cmd["data"]):
            raise InvalidCommandData("Arguments provided")
        for validator in valids:
            validator.do(cmd, *args, **kwargs)

    def __repr__(self):
        return "Validating data group"


class ValidationError(ValueError):
    pass


@dataclass
class PublishTopic:
    topic: str
    data_key: str = ""

    def do(self, cmd: dict, *args, **kwargs):
        if self.data_key:
            data = cmd["data"][self.data_key]
        else:
            data = cmd["data"]
        pyaware.events.publish(self.topic, data=data, timestamp=datetime.utcnow())

    def __repr__(self):
        return f"Publishing {self.topic}"


@dataclass
class WaitTopic:
    topic: str
    timeout: typing.Optional[number] = None

    async def do(self, cmd: dict, *args, **kwargs):
        cmd[f"{self.topic}_response"] = await pyaware.events.wait(
            self.topic, self.timeout
        )

    def __repr__(self):
        return f"Waiting for {self.topic}"


@dataclass
class TopicTask:
    """
    Publishes a topic and waits for all the associated subscriber handles to finish before returning
    :param topic The event topic to publish to
    :param key_map. Maps elements from the cmd["data"] -> publish(k=cmd["data"][v]) for k,v in key_map.items()
    eg. if key_map = {"hi": "world"} and cmd = {"world": "Hello"} then
    events.publish(self.topic, hi="Hello")
    :param timeout Timeout for all items to complete before returning a timeout error to the calling function
    """

    topic: str
    key_map: dict = field(default_factory=dict)
    timeout: typing.Optional[number] = None
    include_cmd_as_key: str = ""

    async def do(self, cmd: dict, *args, **kwargs):
        new_kwargs = {
            k: cmd["data"][v] for k, v in self.key_map.items() if v in cmd["data"]
        }
        if self.include_cmd_as_key:
            new_kwargs[self.include_cmd_as_key] = cmd
        await pyaware.events.publish(self.topic, **new_kwargs).all()

    def __repr__(self):
        return f"Completing task for {self.topic}"
