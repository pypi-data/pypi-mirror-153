from datetime import datetime
from collections import namedtuple, defaultdict

Deadline = namedtuple(
    "Deadline", ["deadline", "device", "param", "source", "time_delta"]
)
Deadline.__doc__ = """
A sortable deadline container
:param deadline: datetime. A timestamp in which the parameter has been marked to be read by
:param device: str. A device id in order to identify the device to be read from
:param source: str. The data source id in which to retrieve the data from 
:param param: str. The parameter name
:param time_delta: typing.Union[int, float]. The time in seconds in which to set the deadline after the last read
"""

collect_trigger_types = {"deadline": Deadline}


def build_collect_triggers(*, config: dict, device_id: str, **kwargs):
    # TODO make trigger build recursive with parameter children
    triggers = defaultdict(list)
    for param, data in config["parameters"].items():
        try:
            source = data["source"]
        except KeyError:
            continue
        for trig in data.get("triggers", {}).get("collect", {}).get("read", []):
            triggers[source].append(
                add_collect_trigger(source, device_id, param, trig, **kwargs)
            )
    return triggers


def add_collect_trigger(source: str, device_id: str, param: str, trig, **kwargs):
    """
    Uses the special methods __eq__ and __ne__ on the triggers to determine if a common trigger already exists
    :return:
    """
    if isinstance(trig, list):
        trig_type, *args = trig
        if trig_type == "deadline":
            return Deadline(
                datetime.utcfromtimestamp(0), device_id, param, source, args[0]
            )
    raise ValueError("Invalid collect trigger definition")
