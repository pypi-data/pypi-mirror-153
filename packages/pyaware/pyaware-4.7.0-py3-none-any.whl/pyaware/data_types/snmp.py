import puresnmp.types
from dataclasses import dataclass, field
from pyaware.data_types.abc import ParamForm
from typing import Set, Dict, TYPE_CHECKING, Union

if TYPE_CHECKING:
    import puresnmp.typevars


class ParamSnmp(ParamForm):
    oid: str

    def get_oids(self) -> Set[str]:
        """
        Get the Object ID (OID) from the parameter.

        :return: Set containing the parameter OID.
        """
        return {self.oid}


@dataclass
class Integer32(ParamSnmp):
    oid: str
    idx: str
    meta: dict = field(default_factory=dict)

    def decode(
        self,
        encoded_data: Dict[
            str, Union[puresnmp.typevars.PyType, puresnmp.types.Integer]
        ],
    ) -> Dict[str, puresnmp.typevars.PyType]:
        if self.oid in encoded_data.keys():
            value = encoded_data[self.oid]
            if isinstance(value, puresnmp.types.Integer):
                value = value.pythonize()
            return {self.idx: value}
        return {}

    def encode(
        self,
        data_to_encode: Dict[str, puresnmp.typevars.PyType],
        encoded_data: Dict[str, puresnmp.types.Integer],
    ) -> Dict[str, puresnmp.types.Integer]:
        if self.idx not in data_to_encode.keys():
            return encoded_data
        parameter_value = data_to_encode[self.idx]
        encoded_data[self.oid] = puresnmp.types.Integer(parameter_value)
        return encoded_data


@dataclass
class String(ParamSnmp):
    """
    Assumes that the output bytestring from puresnmp is of ascii encoding.
    This is a common use case for the Octet String. But there are cases where hex strings are used instead.
    https://snmpsharpnet.com/index.php/working-with-octet-strings/
    TODO: Review the SNMP String decoding/encoding.
    """

    oid: str
    idx: str
    meta: dict = field(default_factory=dict)

    def decode(
        self,
        encoded_data: Dict[
            str, Union[puresnmp.typevars.PyType, puresnmp.types.OctetString]
        ],
    ) -> Dict[str, puresnmp.typevars.PyType]:
        if self.oid in encoded_data.keys():
            value = encoded_data[self.oid]
            if isinstance(value, puresnmp.types.OctetString):
                value = value.pythonize()
            return {self.idx: value.decode(encoding="ascii")}
        return {}

    def encode(
        self,
        data_to_encode: Dict[str, puresnmp.typevars.PyType],
        encoded_data: Dict[str, puresnmp.types.OctetString],
    ) -> Dict[str, puresnmp.types.OctetString]:
        if self.idx not in data_to_encode.keys():
            return encoded_data
        parameter_value = data_to_encode[self.idx].encode(encoding="ascii")
        encoded_data[self.oid] = puresnmp.types.OctetString(parameter_value)
        return encoded_data


PARAM_TYPES = {
    "Snmp.Integer32": Integer32,
    "Snmp.String": String,
}
