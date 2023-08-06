import typing
from dataclasses import dataclass, field

from pyaware.data_types.abc import ParamForm


@dataclass
class ParamDict(ParamForm):
    key: str
    idx: str
    table: dict = field(default_factory=dict)
    meta: dict = field(default_factory=dict)

    def decode(self, json_obj: dict):
        return {self.idx: self.table.get(json_obj[self.key], json_obj[self.key])}


@dataclass
class ParamStatic(ParamForm):
    idx: str
    value: typing.Any
    meta: dict = field(default_factory=dict)


PARAM_TYPES = {
    "ParamDict": ParamDict,
    "ParamStatic": ParamStatic,
    "Common.ParamDict": ParamDict,
    "Common.ParamStatic": ParamStatic,
}
