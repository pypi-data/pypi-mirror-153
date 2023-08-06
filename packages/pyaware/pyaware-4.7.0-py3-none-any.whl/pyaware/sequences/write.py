from __future__ import annotations

"""
Change the default write behaviour of a parameter to be a sequence of operations.
To replicate the default write behaviour of a parameter, the default configuration would be:
```
param-name:
  sequences:
    write:
      - type: write
```
In order to ensure that a read happens before writing the parameter, the sequence would look like:
```
param-name:
  sequences:
    write:
      - type: read
      - type: write
```
In order to sequence a parameter to set the register to 0 before writing the payload value would be:
```
param-name:
  sequences:
    write:
      - type: write_value
        value: 0
      - type: write
```
In order to sequence a pulse like trigger it pulses to a negative value for 200ms
```
param-name:
  sequences:
    write:
      - type: write_value
        value: false
      - type: wait
        seconds: 0.2
      - type: write_value
        value: true
```
:param data: Dictionary of form parameter: value
:return:
"""
import asyncio
import typing

if typing.TYPE_CHECKING:
    from pyaware.parameters import Parameter


def factory_wait(
    parameters: typing.Dict[str, Parameter],
    idx: str,
    *,
    seconds: typing.Union[int, float],
):
    async def wait(data: dict):
        """
        Waits a predetermined amount of seconds before completing the next operation
        :param data:
        :return:
        """
        await asyncio.sleep(seconds)

    return wait


def factory_write(parameters: typing.Dict[str, Parameter], idx: str):
    async def write(data: dict):
        param = parameters[idx]
        encoder = param.writer.encoder_factory()
        encoded = param.encode(data, encoder)
        await param.writer.handle(encoded)

    return write


def factory_write_value(
    parameters: typing.Dict[str, Parameter], idx: str, *, value: typing.Any
):
    async def write_value(data: dict):
        new_data = data.copy()
        new_data[idx] = value
        param = parameters[idx]
        encoder = param.writer.encoder_factory()
        encoded = param.encode(new_data, encoder)
        await param.writer.handle(encoded)

    return write_value


def factory_write_parameter_value(
    parameters: typing.Dict[str, Parameter],
    idx: str,
    *,
    parameter: str,
    value: typing.Any,
):
    async def write_parameter_value(data: dict):
        new_data = data.copy()
        new_data[parameter] = value
        param = parameters[parameter]
        await param.write(new_data)

    return write_parameter_value


def factory_write_parameter(
    parameters: typing.Dict[str, Parameter],
    idx: str,
    *,
    parameter: str,
):
    async def write_parameter(data: dict):
        new_data = data.copy()
        new_data[parameter] = new_data[idx]
        param = parameters[parameter]
        await param.write(new_data)

    return write_parameter


sequences = {
    "write": factory_write,
    "write_value": factory_write_value,
    "write_parameter_value": factory_write_parameter_value,
    "write_parameter": factory_write_parameter,
    "wait": factory_wait,
}


def parse_write_sequence(
    parameters: typing.Dict[str, Parameter], idx: str, sequence: typing.List[dict]
) -> typing.List[typing.Callable[[dict], typing.Awaitable[None]]]:
    seqs = []
    for itm in sequence:
        seq = itm.copy()  # Preserve original
        typ = seq.pop("type")
        seqs.append(sequences[typ](parameters, idx, **seq))
    return seqs
