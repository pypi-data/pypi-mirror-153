import typing


class ParamForm:
    """
    Base class to indicate that the class belongs as a parameter form
    """

    idx: str

    def decode(self, data: typing.Any) -> dict:
        return {}

    def encode(self, data: dict, encoded: typing.Any) -> typing.Any:
        return encoded
