from __future__ import annotations
import typing
from collections import defaultdict
from dataclasses import dataclass, field

import pyaware.data_types.abc
from pyaware import data_types
from pyaware import triggers
import pyaware.sequences.write
import logging

log = logging.getLogger(__name__)


@dataclass
class ParameterWrite:
    validators: typing.List[typing.Callable[[typing.Any], None]]
    sequence: typing.List[typing.Callable[[dict], typing.Awaitable[None]]]
    encoder_factory: typing.Optional[typing.Callable[[], typing.Any]] = None

    def __post_init__(self):
        self._handle = None

    @property
    def handle(self) -> typing.Callable[[typing.Any], typing.Awaitable[None]]:
        """
        Returns a write handle that takes the populated encoder from encoder factory and writes it out via the
        controller
        :return Write handle:
        """
        return self._handle

    @handle.setter
    def handle(self, value):
        self._handle = value


@dataclass
class ParameterRead:
    def __post_init__(self):
        self._handle = None

    @property
    def handle(self) -> typing.Callable[[], typing.Awaitable[None]]:
        """
        Returns a write handle that takes the populated encoder from encoder factory and writes it out via the
        controller
        :return Write handle:
        """
        return self._handle

    @handle.setter
    def handle(self, value):
        self._handle = value


@dataclass
class Parameter:
    """
    A parameter is a named parameter that can be used to decode information from reads and encode information for
    writes.
    """

    source: typing.Optional[str] = None
    form: typing.Optional[pyaware.data_types.abc.ParamForm] = None
    children: typing.List[Parameter] = field(default_factory=list)
    # TODO add triggers support to decode method
    # process_triggers: typing.List[typing.Callable[[dict, datetime.datetime], bool]]
    writer: typing.Optional[ParameterWrite] = None
    reader: typing.Optional[ParameterRead] = None
    parent: typing.Optional[Parameter] = None

    def __post_init__(self):
        if self.parent:
            self.current_state = self.parent.current_state
        else:
            self.current_state = {}
        self.store_state = None
        self.send_state = None
        if self.source is None:
            try:
                self.source = self.parent.source
            except AttributeError:
                self.source = None

    async def write(self, data: dict):
        """
        1. Returns if not the parent
        2. Validates the data for the children parameters
        3. Runs the sequence against the handle
        :param data:
        :return:
        """
        if self.parent:
            # Delegate writing to the Parent
            await self.parent.write(data)
            return
        # We are the parent parameter so run validation down the tree of parameters
        if not self.validate_write(data):
            # if no validators exist then validation fails
            assert False
        modified_data = {**self.current_state, **data}
        for step in self.writer.sequence:
            await step(modified_data)
        if not self.writer.sequence:
            encoder = self.writer.encoder_factory()
            encoded = self.encode(modified_data, encoder)
            await self.writer.handle(encoded)

    def validate_write(self, data: dict):
        validated = False
        for check in self.writer.validators:
            try:
                check(data[self.form.idx])
                validated = True
            except KeyError:
                pass
        if (
            self.form is not None
            and not self.writer.validators
            and self.form.idx in data
        ):
            assert False
        for child in self.children:
            validated |= child.validate_write(data)
        return validated

    async def read(self) -> typing.Optional[dict]:
        if self.parent:
            await self.parent.read()
            return  # Delegate reading to the Parent
        resp = self.decode(await self.reader.handle())
        return resp

    def decode(self, data: typing.Any) -> dict:
        """
        Decodes the data read. The children are decoded first, followed by the children.
        :param data:
        :return:
        """
        resp = {}
        for param in self.children:
            resp.update(param.decode(data))
        try:
            resp.update(self.form.decode(data))
        except AttributeError:
            pass
        # TODO process triggers
        self.current_state.update(resp)
        return resp

    def encode(self, data: dict, encoder: typing.Any) -> typing.Any:
        """
        Encodes the data to write. The parent is encoded first if it has a form. Followed by the children.
        This means if there is a conflict between the parent and children data, the children will get precedence.
        :param data:
        :param encoder:
        :return:
        """
        try:
            self.form.encode(data, encoder)
        except AttributeError:
            pass
        for param in self.children:
            param.encode(data, encoder)
        return encoder


def parse_validators(
    idx: str,
    validators: dict,
) -> typing.List[typing.Callable[[typing.Any], None]]:
    return [triggers.add_write_trigger(idx, validator) for validator in validators]


def parse_writer_sequence(
    idx: str,
    parameter_config: dict,
    parameters: typing.Dict[str, Parameter],
) -> typing.List[typing.Callable[[dict], typing.Awaitable[None]]]:
    if parameter_config.get("sequences", {}).get("write", []):
        return pyaware.sequences.write.parse_write_sequence(
            parameters, idx, parameter_config.get("sequences", {}).get("write", [])
        )
    else:
        return []


def parse_writer(
    idx: str, parameter_config: dict, parameters: typing.Dict[str, Parameter]
) -> ParameterWrite:
    try:
        validators = parameter_config["triggers"]["write"]["validators"]
    except KeyError:
        validators = []
    return ParameterWrite(
        parse_validators(idx, validators),
        parse_writer_sequence(idx, parameter_config, parameters),
    )


def parse_reader(parameter_config: dict) -> ParameterRead:
    return ParameterRead()


def parse_legacy_param_bits(idx: str, parameters: dict):
    """
    Replace ParamBits with the equivalent config setting
    :param idx:
    :param parameters:
    :return:
    """
    log.warning(
        "ParamBits found in config file. This is legacy for this parser. Converting internally to new api"
    )
    param = parameters[idx].copy()
    param.update(
        {
            "form": {
                "type": "Param",
                "address": parameters[idx]["form"]["address"],
                "idx": idx,
            },
            "children": {
                iden: {
                    "form": {
                        "type": "ParamBit",
                        "address": parameters[idx]["form"]["address"],
                        "idx": iden,
                        "bit": bit,
                    },
                    "triggers": parameters.get(iden, {}).get("triggers", {}),
                }
                for iden, bit in parameters[idx]["form"]["bitmask"].items()
            },
            "triggers": parameters[idx].get("triggers"),
        }
    )
    return param


def parse_parameters(
    parameters: dict, meta: dict, parent: typing.Optional[Parameter] = None
) -> typing.Dict[str, Parameter]:
    params = {}
    for idx, param in parameters.items():
        # Legacy check to ensure that ParamBits triggers don't override parameters
        if idx in params:
            continue
        writer = parse_writer(idx, param, params)
        reader = parse_reader(param)
        if param.get("form", {}).get("type") == "ParamBits":
            # For backwards compatibility with ParamBits, it will add the bitmask as children with ParamBit
            param = parse_legacy_param_bits(idx, parameters)
        try:
            form = data_types.parse_data_type_class(**param["form"], meta=meta)
        except KeyError:
            form = None
        # TODO add triggers here
        params[idx] = Parameter(
            param.get("source"), form, [], writer, reader, parent=parent
        )
        if param.get("children"):
            children = parse_parameters(param["children"], meta, params[idx])
            params.update(children)
            params[idx].children.extend(children.values())

    return params


def parse_parameters_by_source(parameters, meta: dict):
    params = parse_parameters(parameters, meta)
    new_params = defaultdict(dict)
    for idx, param in params.items():
        new_params[param.source][idx] = params[idx]
    return new_params
