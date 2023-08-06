# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import Optional  # pylint: disable=unused-import
from ..protobufs import main_pb2


class ServoTuningParam:
    """
    A parameter used to establish the servo tuning of an axis.
    """

    def __init__(
            self: 'ServoTuningParam',
            name: str,
            value: float
    ) -> None:
        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        """
        The name of the parameter to set.
        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def value(self) -> float:
        """
        The value to use for this parameter.
        """

        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.ServoTuningParam
    ) -> 'ServoTuningParam':
        instance = ServoTuningParam.__new__(
            ServoTuningParam
        )  # type: ServoTuningParam
        instance.name = pb_data.name
        instance.value = pb_data.value
        return instance

    @staticmethod
    def to_protobuf(source: 'Optional[ServoTuningParam]') -> main_pb2.ServoTuningParam:
        if source is None:
            return main_pb2.ServoTuningParam()

        if not isinstance(source, ServoTuningParam):
            raise TypeError("Provided value is not ServoTuningParam.")

        pb_data = main_pb2.ServoTuningParam()
        pb_data.name = source.name
        pb_data.value = source.value
        return pb_data
