from abc import ABC, abstractmethod
import typing


class Controller(ABC):
    triggers: dict
    parameters: dict
    sequences: dict

    @abstractmethod
    async def write_parameters(self, data: typing.Dict[str, typing.Any]):
        """
        Write parameters through the controller process flow. This will run through write validation triggers and also
        the write sequence in order to complete the write on each parameter
        :param data:
        :return:
        """
        return NotImplemented

    @abstractmethod
    async def read_parameters(self, parameters: set) -> typing.Dict[str, typing.Any]:
        """
        Read parameters through the controller process flow. This will run through read process triggers and return the
        key value pairs of the data read
        :param keys:
        :return: dictionary of parameters read
        """
        return NotImplemented

    @abstractmethod
    async def set_parameter(self, parameter: str, value: typing.Any):
        """
        Directly sets the parameter using the data type encode method. Assumes that all validation checks are completed.
        :param parameter: Parameter id to get from self.parameters
        :param value: The value to encode
        :return:
        """
        return NotImplemented

    @abstractmethod
    async def get_parameter(self, parameter: str) -> typing.Any:
        """
        Directly gets the parameter using the data type decode method. Assumes that all validation checks are completed.
        :param parameter: Parameter id to get from self.parameters
        :return: Return the value of the parameter read
        """
        return NotImplemented

    @abstractmethod
    async def set_parameters(self, parameters: typing.Dict[str, typing.Any]):
        """
        Directly sets the parameters using the data type encode method. Assumes that all validation checks are completed
        and ignores the write sequencing of the parameter. Care should be used when setting parameters that share a
        write block as any parameters not included will not have default values. In the case of modbus, this will erase
        any other parameters present in the register if not included.
        :param data: Key value pairs of the parameters to set
        :return:
        """
        return NotImplemented

    @abstractmethod
    async def get_parameters(self, parameters: set) -> typing.Dict[str, typing.Any]:
        """
        Directly gets the parameter using the data type decode method. Assumes that all validation checks are completed.
        :param keys: Set of keys to read
        :return: Return the value of the parameter read
        """
        return NotImplemented
