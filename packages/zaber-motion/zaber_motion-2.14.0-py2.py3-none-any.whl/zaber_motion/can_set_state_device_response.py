# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import List  # pylint: disable=unused-import
from .protobufs import main_pb2
from .can_set_state_axis_response import CanSetStateAxisResponse


class CanSetStateDeviceResponse:
    """
    An object containing any setup issues that will prevent setting a state to a given device.
    """

    @property
    def error(self) -> str:
        """
        The error blocking applying this state to the given device.
        """

        return self._error

    @error.setter
    def error(self, value: str) -> None:
        self._error = value

    @property
    def axis_errors(self) -> List[CanSetStateAxisResponse]:
        """
        A list of errors that block setting state of device's axes.
        """

        return self._axis_errors

    @axis_errors.setter
    def axis_errors(self, value: List[CanSetStateAxisResponse]) -> None:
        self._axis_errors = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.CanSetStateDeviceResponse
    ) -> 'CanSetStateDeviceResponse':
        instance = CanSetStateDeviceResponse.__new__(
            CanSetStateDeviceResponse
        )  # type: CanSetStateDeviceResponse
        instance.error = pb_data.error
        instance.axis_errors = [CanSetStateAxisResponse.from_protobuf(item) for item in pb_data.axis_errors]
        return instance
