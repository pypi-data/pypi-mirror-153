from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
import typing
import pyaware.config
from pyaware.triggers.collect import add_collect_trigger, build_collect_triggers
from pyaware.triggers.process import add_process_trigger, build_process_triggers
from pyaware.triggers.write import add_write_trigger

number = typing.Union[float, str]


def nested_dict():
    return defaultdict(nested_dict)


def build_from_device_config(path, **kwargs):
    parsed = pyaware.config.load_yaml_config(path)
    triggers = {
        "process": build_process_triggers(config=parsed, **kwargs),
        "collect": build_collect_triggers(config=parsed, **kwargs),
        "write": defaultdict(list),
    }

    # TODO Remove write triggers when all parameters are parsed in parameters.py
    for param, data in parsed["parameters"].items():
        for trig in data.get("triggers", {}).get("write", {}).get("validators", []):
            triggers["write"][param].append(add_write_trigger(param, trig, **kwargs))
    return triggers


class Validator:
    pass


class Parser:
    """
    Extracts data from a topic
    """

    def __call__(self, data):
        return data


@dataclass
class DictParser:
    """ """

    key: str = ""

    def __call__(self, data):
        if self.key:
            return data[self.key].copy()
        else:
            return data.copy()
