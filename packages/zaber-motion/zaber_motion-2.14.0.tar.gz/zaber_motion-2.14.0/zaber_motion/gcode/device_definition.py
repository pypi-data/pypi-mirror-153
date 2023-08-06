# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import List, Optional  # pylint: disable=unused-import
from ..protobufs import main_pb2
from .axis_definition import AxisDefinition
from ..measurement import Measurement


class DeviceDefinition:
    """
    Holds information about device and its axes for purpose of a translator.
    """

    def __init__(
            self: 'DeviceDefinition',
            device_id: int,
            axes: List[AxisDefinition],
            max_speed: Measurement
    ) -> None:
        self._device_id = device_id
        self._axes = axes
        self._max_speed = max_speed

    @property
    def device_id(self) -> int:
        """
        Device ID of the controller.
        Can be obtained from device settings.
        """

        return self._device_id

    @device_id.setter
    def device_id(self, value: int) -> None:
        self._device_id = value

    @property
    def axes(self) -> List[AxisDefinition]:
        """
        Applicable axes of the device.
        """

        return self._axes

    @axes.setter
    def axes(self, value: List[AxisDefinition]) -> None:
        self._axes = value

    @property
    def max_speed(self) -> Measurement:
        """
        The smallest of each axis' maxspeed setting value.
        This value becomes the traverse rate of the translator.
        """

        return self._max_speed

    @max_speed.setter
    def max_speed(self, value: Measurement) -> None:
        self._max_speed = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def to_protobuf(source: 'Optional[DeviceDefinition]') -> main_pb2.TranslatorDefinition:
        if source is None:
            return main_pb2.TranslatorDefinition()

        if not isinstance(source, DeviceDefinition):
            raise TypeError("Provided value is not DeviceDefinition.")

        pb_data = main_pb2.TranslatorDefinition()
        pb_data.device_id = source.device_id
        if source.axes is not None:
            pb_data.axes.extend(
                [AxisDefinition.to_protobuf(item) for item in source.axes])
        pb_data.max_speed.CopyFrom(Measurement.to_protobuf(source.max_speed))
        return pb_data
