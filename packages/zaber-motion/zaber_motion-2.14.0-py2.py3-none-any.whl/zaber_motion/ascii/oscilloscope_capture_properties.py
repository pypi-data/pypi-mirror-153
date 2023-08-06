# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from ..protobufs import main_pb2


class OscilloscopeCaptureProperties:
    """
    The public properties of one channel of recorded oscilloscope data.
    """

    @property
    def setting(self) -> str:
        """
        The name of the recorded setting.
        """

        return self._setting

    @setting.setter
    def setting(self, value: str) -> None:
        self._setting = value

    @property
    def axis_number(self) -> int:
        """
        The number of the axis the data was recorded from, or 0 for the controller.
        """

        return self._axis_number

    @axis_number.setter
    def axis_number(self, value: int) -> None:
        self._axis_number = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.OscilloscopeCaptureProperties
    ) -> 'OscilloscopeCaptureProperties':
        instance = OscilloscopeCaptureProperties.__new__(
            OscilloscopeCaptureProperties
        )  # type: OscilloscopeCaptureProperties
        instance.setting = pb_data.setting
        instance.axis_number = pb_data.axis_number
        return instance
