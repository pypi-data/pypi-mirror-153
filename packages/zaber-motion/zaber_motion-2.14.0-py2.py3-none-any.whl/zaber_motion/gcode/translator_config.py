# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import List, Optional  # pylint: disable=unused-import
from ..protobufs import main_pb2
from .axis_mapping import AxisMapping
from .axis_transformation import AxisTransformation


class TranslatorConfig:
    """
    Configuration of a translator.
    """

    def __init__(
            self: 'TranslatorConfig',
            axis_mappings: Optional[List[AxisMapping]] = None,
            axis_transformations: Optional[List[AxisTransformation]] = None
    ) -> None:
        self._axis_mappings = axis_mappings
        self._axis_transformations = axis_transformations

    @property
    def axis_mappings(self) -> Optional[List[AxisMapping]]:
        """
        Optional custom mapping of translator axes to stream axes.
        """

        return self._axis_mappings

    @axis_mappings.setter
    def axis_mappings(self, value: Optional[List[AxisMapping]]) -> None:
        self._axis_mappings = value

    @property
    def axis_transformations(self) -> Optional[List[AxisTransformation]]:
        """
        Optional transformation of axes.
        """

        return self._axis_transformations

    @axis_transformations.setter
    def axis_transformations(self, value: Optional[List[AxisTransformation]]) -> None:
        self._axis_transformations = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def to_protobuf(source: 'Optional[TranslatorConfig]') -> main_pb2.TranslatorConfig:
        if source is None:
            return main_pb2.TranslatorConfig()

        if not isinstance(source, TranslatorConfig):
            raise TypeError("Provided value is not TranslatorConfig.")

        pb_data = main_pb2.TranslatorConfig()
        if source.axis_mappings is not None:
            pb_data.axis_mappings.extend(
                [AxisMapping.to_protobuf(item) for item in source.axis_mappings])
        if source.axis_transformations is not None:
            pb_data.axis_transformations.extend(
                [AxisTransformation.to_protobuf(item) for item in source.axis_transformations])
        return pb_data
