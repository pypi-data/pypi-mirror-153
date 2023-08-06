import typing
from collections import defaultdict
from datetime import datetime, timedelta
import pyaware


def factory_by_time(
    param: str,
    *,
    ref_name: typing.Optional[str] = None,
    time: typing.Union[int, float],
    ref_key: typing.Optional[str] = None,
    data_key: typing.Optional[str] = None,
    default_ref_name: str,
    **kwargs
):
    ref_name = ref_name or default_ref_name
    ref_key = ref_key or param
    data_key = data_key or ref_key
    reference = kwargs[ref_name]

    def trig_time(data: dict, timestamp: datetime) -> bool:
        if data_key not in data:
            return False
        try:
            ref = max(reference[ref_key])
        except KeyError:
            return True
        if timestamp >= ref + timedelta(seconds=time):
            return True
        return False

    return trig_time


def factory_by_state(
    param: str,
    *,
    ref_name: typing.Optional[str] = None,
    ref_key: typing.Optional[str] = None,
    data_key: typing.Optional[str] = None,
    default_ref_name: str,
    **kwargs
):
    ref_name = ref_name or default_ref_name
    ref_key = ref_key or param
    data_key = data_key or ref_key
    reference = kwargs[ref_name]

    def trig_state(data: dict, timestamp: datetime) -> bool:
        if data_key not in data:
            return False
        try:
            ref = reference[ref_key][max(reference[ref_key])]
        except (IndexError, KeyError):
            return True
        value = data[data_key]
        if ref != value:
            return True
        return False

    return trig_state


def factory_by_delta(
    param: str,
    *,
    ref_name: typing.Optional[str] = None,
    delta: typing.Union[int, float],
    ref_key: typing.Optional[str] = None,
    data_key: typing.Optional[str] = None,
    default_ref_name: str,
    **kwargs
):
    ref_name = ref_name or default_ref_name
    ref_key = ref_key or param
    data_key = data_key or ref_key
    reference = kwargs[ref_name]

    def trig_delta(data: dict, timestamp: datetime) -> bool:
        if data_key not in data:
            return False
        value = data[data_key]
        try:
            ref = reference[ref_key][max(reference[ref_key])]
        except (IndexError, KeyError):
            return True
        if not (ref - delta < value < ref + delta):
            return True
        return False

    return trig_delta


def factory_by_always(param: str, **kwargs):
    def trig_always(data: dict, timestamp: datetime) -> bool:
        if param not in data:
            return False
        return True

    return trig_always


def factory_by_comparison(
    param: str,
    *,
    ref_name: typing.Optional[str] = None,
    comp_type: str,
    comp_value: typing.Union[None, bool, str, int, float],
    ref_key: typing.Optional[str] = None,
    data_key: typing.Optional[str] = None,
    default_ref_name: str,
    **kwargs
):
    ref_name = ref_name or default_ref_name
    ref_key = ref_key or param
    data_key = data_key or ref_key
    reference = kwargs[ref_name]

    if comp_type == "e":

        def trig_comp_eq(data: dict, timestamp: datetime) -> bool:
            if data_key not in data:
                return False
            value = data[data_key]
            try:
                ref = reference[ref_key][max(reference[ref_key])]
            except (IndexError, KeyError):
                return True
            except TypeError:
                ref = reference[ref_key]
            return comp_value == value

        return trig_comp_eq
    elif comp_type == "ge":

        def trig_comp_ge(data: dict, timestamp: datetime) -> bool:
            if data_key not in data:
                return False
            value = data[data_key]
            try:
                ref = reference[ref_key][max(reference[ref_key])]
            except (IndexError, KeyError):
                return True
            except TypeError:
                ref = reference[ref_key]
            return comp_value >= value

        return trig_comp_ge
    elif comp_type == "g":

        def trig_comp_g(data: dict, timestamp: datetime) -> bool:
            if data_key not in data:
                return False
            value = data[data_key]
            try:
                ref = reference[ref_key][max(reference[ref_key])]
            except (IndexError, KeyError):
                return True
            except TypeError:
                ref = reference[ref_key]
            return comp_value > value

        return trig_comp_g
    elif comp_type == "le":

        def trig_comp_le(data: dict, timestamp: datetime) -> bool:
            if data_key not in data:
                return False
            value = data[data_key]
            try:
                ref = reference[ref_key][max(reference[ref_key])]
            except (IndexError, KeyError):
                return True
            except TypeError:
                ref = reference[ref_key]
            return comp_value <= value

        return trig_comp_le
    elif comp_type == "l":

        def trig_comp_l(data: dict, timestamp: datetime) -> bool:
            if data_key not in data:
                return False
            value = data[data_key]
            try:
                ref = reference[ref_key][max(reference[ref_key])]
            except (IndexError, KeyError):
                return True
            except TypeError:
                ref = reference[ref_key]
            return comp_value < value

        return trig_comp_l


def factory_by_and(
    param: str, *, trig_type: str, triggers: typing.List[typing.Dict], **kwargs
):
    trigs: typing.List[typing.Callable] = []
    for trig in triggers:
        trigs.append(add_process_trigger(param=param, trigger=trig, **kwargs))

    def trig_and(data: dict, timestamp: datetime) -> bool:
        results = [trig(data=data, timestamp=timestamp) for trig in trigs]
        return all(results)

    return trig_and


process_trigger_types = {
    "state": factory_by_state,
    "time": factory_by_time,
    "delta": factory_by_delta,
    "always": factory_by_always,
    "and": factory_by_and,
    "comparison": factory_by_comparison,
}


def _build_process_triggers_recursive(
    config_parameters: dict, triggers: dict, **kwargs
):
    for param, data in config_parameters.items():
        if data.get("children"):
            _build_process_triggers_recursive(data["children"], triggers, **kwargs)
        for trig in data.get("triggers", {}).get("process", {}).get("store", []):
            triggers["store"][param].append(
                add_process_trigger(
                    param, trig, default_ref_name="store_state", **kwargs
                )
            )
        for trig in data.get("triggers", {}).get("process", {}).get("send", []):
            triggers["send"][param].append(
                add_process_trigger(
                    param, trig, default_ref_name="send_state", **kwargs
                )
            )
        for trig in data.get("triggers", {}).get("process", {}).get("event", []):
            triggers["event"][param].append(
                add_process_trigger(
                    param, trig, default_ref_name="event_state", **kwargs
                )
            )


def build_process_triggers(*, config, **kwargs) -> dict:
    triggers = defaultdict(lambda: defaultdict(list))
    _build_process_triggers_recursive(config["parameters"], triggers, **kwargs)
    return triggers


def add_process_trigger(
    param, trigger: typing.Union[list, dict], **kwargs
) -> typing.Callable:
    if isinstance(trigger, list):
        trig_type, *trig_params = trigger
        if trig_type == "state":
            return factory_by_state(param, **kwargs)
        elif trig_type == "time":
            return factory_by_time(param, time=trig_params[0], **kwargs)
        elif trig_type == "value":
            return factory_by_delta(param, delta=trig_params[0], **kwargs)
        elif trig_type == "always":
            return factory_by_always(param, **kwargs)
        elif trig_type == "comparison":
            return factory_by_comparison(param, **kwargs)
        else:
            raise ValueError
    else:
        return process_trigger_types[trigger["trig_type"]](param, **kwargs, **trigger)


@pyaware.async_threaded
def run_triggers(
    triggers: dict, data: dict, timestamp: datetime
) -> typing.Union[typing.Awaitable[dict], dict]:
    keys = triggers.keys() & data.keys()
    return {
        k: {timestamp: data[k]}
        for k in keys
        if any((trig(data=data, timestamp=timestamp) for trig in triggers[k]))
    }
