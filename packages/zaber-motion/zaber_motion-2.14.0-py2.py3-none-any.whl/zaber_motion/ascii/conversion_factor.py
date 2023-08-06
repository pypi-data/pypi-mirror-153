# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import Optional  # pylint: disable=unused-import
from ..protobufs import main_pb2
from ..units import Units


class ConversionFactor:
    """
    Represents unit conversion factor for a single dimension.
    """

    def __init__(
            self: 'ConversionFactor',
            setting: str,
            value: float,
            unit: Units
    ) -> None:
        self._setting = setting
        self._value = value
        self._unit = unit

    @property
    def setting(self) -> str:
        """
        Setting representing the dimension.
        """

        return self._setting

    @setting.setter
    def setting(self, value: str) -> None:
        self._setting = value

    @property
    def value(self) -> float:
        """
        Value representing 1 native device unit in specified real-word units.
        """

        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value

    @property
    def unit(self) -> Units:
        """
        Units of the value.
        """

        return self._unit

    @unit.setter
    def unit(self, value: Units) -> None:
        self._unit = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def to_protobuf(source: 'Optional[ConversionFactor]') -> main_pb2.ConversionFactor:
        if source is None:
            return main_pb2.ConversionFactor()

        if not isinstance(source, ConversionFactor):
            raise TypeError("Provided value is not ConversionFactor.")

        pb_data = main_pb2.ConversionFactor()
        pb_data.setting = source.setting
        pb_data.value = source.value
        pb_data.unit = (source.unit or Units.NATIVE).value
        return pb_data
