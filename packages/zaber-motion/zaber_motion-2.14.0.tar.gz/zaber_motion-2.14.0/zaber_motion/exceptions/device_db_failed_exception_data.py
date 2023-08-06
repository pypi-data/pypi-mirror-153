# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from ..protobufs import main_pb2


class DeviceDbFailedExceptionData:
    """
    Contains additional data for a DeviceDbFailedException.
    """

    @property
    def code(self) -> str:
        """
        Code describing type of the error.
        """

        return self._code

    @code.setter
    def code(self, value: str) -> None:
        self._code = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.DeviceDbFailedExceptionData
    ) -> 'DeviceDbFailedExceptionData':
        instance = DeviceDbFailedExceptionData.__new__(
            DeviceDbFailedExceptionData
        )  # type: DeviceDbFailedExceptionData
        instance.code = pb_data.code
        return instance
