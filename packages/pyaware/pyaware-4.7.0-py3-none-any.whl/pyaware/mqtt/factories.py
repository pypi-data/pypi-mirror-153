from copy import deepcopy
from typing import Callable


def get_factory(factory: dict) -> Callable:
    try:
        return globals()[factory["name"]]
    except (KeyError, TypeError):
        return default


def telemetry_v1(data, timestamp, **kwargs) -> dict:
    data = deepcopy(data)
    msg = {"dateTime": timestamp, "raw_values": data, "parameterValues": []}
    for item in data:
        name = item.pop("name")
        msg["parameterValues"].append({"parameterName": name, "data": item})
    return msg


def telemetry_v2(data, meta, timestamp, **kwargs) -> dict:
    msg = meta.copy()
    msg["timestamp"] = timestamp
    msg["values"] = data
    msg["raw_values"] = data
    return msg


def telemetry_v3(data, meta, timestamp, uid, **kwargs) -> dict:
    msg = meta.copy()
    msg["timestamp"] = timestamp
    msg["values"] = data
    msg["uid"] = uid
    return msg


def topology_v1(data, timestamp, **kwargs) -> dict:
    for serial, devices in data.items():
        payload = {
            "version": 1,
            "serial": serial,
            "type": "imac-controller-master",
            "timestamp": timestamp,
            "children": devices,
        }
        return payload


def default(data, **kwargs) -> dict:
    return data
