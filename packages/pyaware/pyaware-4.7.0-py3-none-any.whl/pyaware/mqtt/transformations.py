from typing import Iterable, Any, Dict
from datetime import datetime
from collections import defaultdict
from copy import deepcopy
from functools import partial


def get_transform(name, **kwargs):
    return partial(globals()[name], **kwargs)


def rename_keys(d: dict, keys: dict) -> dict:
    """
    Return a new dictionary with the keys changed from the **kwargs
    usage:
    >old_d = {"hello": "world"}
    >rename_keys(old_d, hello="world"})
    {'world': 'world'}
    >old_d = {"hello-world": "world"}
    >rename_keys(old_d, **{"hello-world": "world"})
    {'world': 'world'}
    :return:
    """
    d = deepcopy(d)
    for k, v in keys.items():
        try:
            d[v] = d.pop(k)
        except:
            pass
    return d


def remove_keys(d: dict, keys: set):
    """
    Returns a new dictionary with the keys removed
    :param d:
    :param keys:
    :param pattern:
    :return:
    """
    d = deepcopy(d)
    for k in keys:
        try:
            d.pop(k)
        except:
            pass
    return d


_aggregate_handles = {
    "samples": len,
    "latest": lambda x: x[max(x)],
    "min": lambda x: min(x.values()),
    "max": lambda x: max(x.values()),
    "sum": lambda x: sum(x.values()),
    "all": lambda x: x,
}


def aggregate(
    items: Dict[str, Dict[datetime, Any]], key: str, aggregates: Iterable[str]
) -> dict:
    """
    Aggregate the items provided into a dictionary based on the types of aggregation requested.
    Items that cannot have the aggregation applied will be skipped
    samples: int
    latest: Optional[Any] = None
    min: Union[None, int, float] = None
    max: Union[None, int, float] = None
    sum: Union[None, int, float] = None
    all: Optional[List[Any]] = None
    :return:
    """
    items = items.copy()
    if key:
        to_process = items[key]
    else:
        to_process = items
    resp = defaultdict(dict)
    for agg in aggregates:
        try:
            handle = _aggregate_handles[agg]
        except KeyError:
            raise ValueError(f"Invalid aggregate applied {agg}")
        for param, value in to_process.items():
            try:
                resp[param][agg] = handle(value)
            except:
                pass
    if key:
        items[key] = resp
    else:
        items = resp
    return items
