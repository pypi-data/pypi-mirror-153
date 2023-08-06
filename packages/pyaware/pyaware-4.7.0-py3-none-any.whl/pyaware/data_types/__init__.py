from __future__ import annotations
import typing
from collections import defaultdict
import ruamel.yaml
import pyaware.data_types.common as common
import pyaware.data_types.modbus as modbus
import pyaware.data_types.snmp as snmp


PARAM_TYPES = {**common.PARAM_TYPES, **modbus.PARAM_TYPES, **snmp.PARAM_TYPES}


def build_from_device_config(path):
    with open(path) as f:
        parsed = ruamel.yaml.safe_load(f)
    return parse_data_types(parsed["parameters"], {})


def resolve_param(reference: dict, meta: dict) -> typing.Any:
    if reference["type"] == "value":
        return reference["value"]
    elif reference["type"] == "ref_param":
        ref = meta[reference["param"]]
        try:
            if reference["null_ref"] == ref:
                return None
        except KeyError:
            pass
        offset = reference.get("offset", 0)
        try:
            data = ref + offset
        except TypeError:
            data = ref
        return data
    else:
        raise ValueError(f"Invalid type {reference['type']} specified")


def resolve_param_dict(reference: dict, meta: dict):
    resolved = {}
    if "type" in reference:
        return resolve_param(reference, meta)
    else:
        for k, v in reference.items():
            if isinstance(v, dict):
                resolved[k] = resolve_param_dict(v, meta)
            elif isinstance(v, list):
                resolved[k] = resolve_param_list(v, meta)
            else:
                resolved[k] = v
    return resolved


def resolve_param_list(reference: list, meta: dict) -> list:
    resolved = []
    for itm in reference:
        if isinstance(itm, dict):
            resolved.append(resolve_param_dict(itm, meta))
        elif isinstance(itm, list):
            resolved.append(resolve_param_list(itm, meta))
        else:
            resolved.append(itm)
    return resolved


def parse_data_type_class(*, type: str, meta: dict, **kwargs):
    cls = PARAM_TYPES[type]
    form = resolve_param_dict(kwargs, meta)
    inst = cls(**form)
    return inst


def parse_data_types(parameters, meta: dict):
    params = {}
    for idx, param in parameters.items():
        try:
            params[idx] = parse_data_type_class(**param["form"], meta=meta)
        except:
            continue
    return params


def parse_data_types_by_source(parameters, meta: dict):
    params = defaultdict(dict)
    for idx, param in parameters.items():
        try:
            params[param["source"]][idx] = parse_data_type_class(
                **param["form"], meta=meta
            )
        except KeyError:
            continue
    return params


def resolve_static_data_types(parameters, meta: dict):
    params = defaultdict(dict)
    for idx, param in parameters.items():
        try:
            if param["source"] == "static":
                params[idx] = parse_data_type_class(**param["form"], meta=meta).value
        except KeyError:
            continue
    return params
