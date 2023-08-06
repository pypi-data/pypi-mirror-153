from pyaware.controllers import Controller
from pyaware.commands import InvalidCommandData


class SetParameters:
    """
    Writes controller parameters by name and value and transformed by the parameter definitions
    """

    async def do(self, cmd: dict, controller: Controller, **kwargs):
        try:
            await controller.write_parameters(cmd["data"])
        except AssertionError as e:
            raise InvalidCommandData("".join(e.args)) from e

    def __repr__(self):
        return "Writing parameters"


class GetParameters:
    """
    Writes controller parameters by name and value and transformed by the parameter definitions
    """

    async def do(self, cmd: dict, controller: Controller, **kwargs):
        data = cmd["data"]
        if isinstance(data, dict):
            # CommandRequestV1 Compatibility
            command_params = set(data["parameters"])
        else:
            command_params = set(data)
        try:
            read_data = await controller.read_parameters(command_params)
        except AssertionError as e:
            raise InvalidCommandData("".join(e.args)) from e
        invalid = command_params.difference(set(read_data))
        if invalid:
            raise IOError(f"Failed to read parameters {','.join(invalid)}")
        cmd["return_values"] = read_data

    def __repr__(self):
        return "Reading parameters"
