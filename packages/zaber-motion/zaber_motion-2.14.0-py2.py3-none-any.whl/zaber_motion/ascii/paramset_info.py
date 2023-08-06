# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import List  # pylint: disable=unused-import
from ..protobufs import main_pb2
from .servo_tuning_param import ServoTuningParam


class ParamsetInfo:
    """
    The raw parameters currently saved to a given paramset.
    """

    @property
    def type(self) -> str:
        """
        The tuning algorithm used for this axis.
        """

        return self._type

    @type.setter
    def type(self, value: str) -> None:
        self._type = value

    @property
    def params(self) -> List[ServoTuningParam]:
        """
        The raw tuning parameters of this device.
        """

        return self._params

    @params.setter
    def params(self, value: List[ServoTuningParam]) -> None:
        self._params = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.ParamsetInfo
    ) -> 'ParamsetInfo':
        instance = ParamsetInfo.__new__(
            ParamsetInfo
        )  # type: ParamsetInfo
        instance.type = pb_data.type
        instance.params = [ServoTuningParam.from_protobuf(item) for item in pb_data.params]
        return instance
