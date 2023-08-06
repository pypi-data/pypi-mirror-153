import typing


def factory_in_list(param, *, lst: list, **kwargs):
    def in_list(value: typing.Any):
        assert value in lst

    return in_list


def factory_range(
    param,
    *,
    min: int,
    max: int,
    step: typing.Union[int, float] = 1,
    scale: typing.Optional[float] = 1,
    **kwargs,
):
    if scale != 1:
        min = round(min * scale)
        max = round(max * scale)
        step = round(step * scale)
    rng = range(min, max + step, step)

    def in_range(value: int):
        assert round(value * scale) in rng

    return in_range


def factory_writable(param, **kwargs):
    return lambda x: None


def factory_by_comparison(
    param: str,
    *,
    ref_name: typing.Optional[str] = None,
    comp_type: str,
    comp_value: typing.Any = None,
    ref_key: typing.Optional[str] = None,
    comp_ref_value: typing.Any = None,
    **kwargs,
):
    ref_key = ref_key or param

    if comp_type == "e":

        def trig_comp_eq(value: typing.Any) -> None:
            if comp_value is not None:
                value = comp_value
            if comp_ref_value is not None:
                assert value == comp_ref_value
            else:
                assert value == kwargs[ref_name][ref_key]

        return trig_comp_eq
    elif comp_type == "ge":

        def trig_comp_ge(value: typing.Any) -> None:
            if comp_value is not None:
                value = comp_value
            if comp_ref_value is not None:
                assert value >= comp_ref_value
            else:
                assert value >= kwargs[ref_name][ref_key]

        return trig_comp_ge
    elif comp_type == "g":

        def trig_comp_ge(value: typing.Any) -> None:
            if comp_value is not None:
                value = comp_value
            if comp_ref_value is not None:
                assert value > comp_ref_value
            else:
                assert value > kwargs[ref_name][ref_key]

        return trig_comp_ge
    elif comp_type == "le":

        def trig_comp_le(value: typing.Any) -> None:
            if comp_value is not None:
                value = comp_value
            if comp_ref_value is not None:
                assert value <= comp_ref_value
            else:
                assert value <= kwargs[ref_name][ref_key]

        return trig_comp_le
    elif comp_type == "l":

        def trig_comp_l(value: typing.Any) -> None:
            if comp_value is not None:
                value = comp_value
            if comp_ref_value is not None:
                assert value < comp_ref_value
            else:
                assert value < kwargs[ref_name][ref_key]

        return trig_comp_l


write_trigger_types = {
    "range": factory_range,
    "writable": factory_writable,
    "in_list": factory_in_list,
    "comparison": factory_by_comparison,
}


def run_triggers(triggers: dict, data: dict):
    assert set(data).issubset(set(triggers))
    for k, v in data.items():
        for trig in triggers[k]:
            trig(v)


def add_write_trigger(param, trigger: dict, **kwargs) -> typing.Callable:
    return write_trigger_types[trigger["trig_type"]](param, **kwargs, **trigger)
