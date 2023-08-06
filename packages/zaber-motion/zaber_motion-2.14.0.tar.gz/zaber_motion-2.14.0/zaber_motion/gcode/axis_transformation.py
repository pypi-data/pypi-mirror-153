# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import Optional  # pylint: disable=unused-import
from ..protobufs import main_pb2
from ..measurement import Measurement


class AxisTransformation:
    """
    Represents a transformation of a translator axis.
    """

    def __init__(
            self: 'AxisTransformation',
            axis_letter: str,
            scaling: Optional[float] = None,
            translation: Optional[Measurement] = None
    ) -> None:
        self._axis_letter = axis_letter
        self._scaling = scaling
        self._translation = translation

    @property
    def axis_letter(self) -> str:
        """
        Letter of the translator axis (X,Y,Z,A,B,C,E).
        """

        return self._axis_letter

    @axis_letter.setter
    def axis_letter(self, value: str) -> None:
        self._axis_letter = value

    @property
    def scaling(self) -> Optional[float]:
        """
        Scaling factor.
        """

        return self._scaling

    @scaling.setter
    def scaling(self, value: Optional[float]) -> None:
        self._scaling = value

    @property
    def translation(self) -> Optional[Measurement]:
        """
        Translation distance.
        """

        return self._translation

    @translation.setter
    def translation(self, value: Optional[Measurement]) -> None:
        self._translation = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def to_protobuf(source: 'Optional[AxisTransformation]') -> main_pb2.TranslatorAxisTransformation:
        if source is None:
            return main_pb2.TranslatorAxisTransformation()

        if not isinstance(source, AxisTransformation):
            raise TypeError("Provided value is not AxisTransformation.")

        pb_data = main_pb2.TranslatorAxisTransformation()
        pb_data.axis_letter = source.axis_letter
        if source.scaling is not None:
            pb_data.scaling = source.scaling
        pb_data.translation.CopyFrom(Measurement.to_protobuf(source.translation))
        return pb_data
