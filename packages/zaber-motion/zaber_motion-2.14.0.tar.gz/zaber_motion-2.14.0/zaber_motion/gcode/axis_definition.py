# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import Optional  # pylint: disable=unused-import
from ..protobufs import main_pb2


class AxisDefinition:
    """
    Defines an axis of the translator.
    """

    def __init__(
            self: 'AxisDefinition',
            peripheral_id: int,
            microstep_resolution: Optional[int] = None
    ) -> None:
        self._peripheral_id = peripheral_id
        self._microstep_resolution = microstep_resolution

    @property
    def peripheral_id(self) -> int:
        """
        ID of the peripheral.
        """

        return self._peripheral_id

    @peripheral_id.setter
    def peripheral_id(self, value: int) -> None:
        self._peripheral_id = value

    @property
    def microstep_resolution(self) -> Optional[int]:
        """
        Microstep resolution of the axis.
        Can be obtained by reading the resolution setting.
        Leave empty if the axis does not have the setting.
        """

        return self._microstep_resolution

    @microstep_resolution.setter
    def microstep_resolution(self, value: Optional[int]) -> None:
        self._microstep_resolution = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.TranslatorAxisDefinition
    ) -> 'AxisDefinition':
        instance = AxisDefinition.__new__(
            AxisDefinition
        )  # type: AxisDefinition
        instance.peripheral_id = pb_data.peripheral_id
        instance.microstep_resolution = pb_data.microstep_resolution
        return instance

    @staticmethod
    def to_protobuf(source: 'Optional[AxisDefinition]') -> main_pb2.TranslatorAxisDefinition:
        if source is None:
            return main_pb2.TranslatorAxisDefinition()

        if not isinstance(source, AxisDefinition):
            raise TypeError("Provided value is not AxisDefinition.")

        pb_data = main_pb2.TranslatorAxisDefinition()
        pb_data.peripheral_id = source.peripheral_id
        if source.microstep_resolution is not None:
            pb_data.microstep_resolution = source.microstep_resolution
        return pb_data
