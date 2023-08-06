# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from ..protobufs import main_pb2


class CommandTooLongExceptionData:
    """
    Information describing why the command could not fit.
    """

    @property
    def fit(self) -> str:
        """
        The part of the command that could be successfully fit in the space provided by the protocol.
        """

        return self._fit

    @fit.setter
    def fit(self, value: str) -> None:
        self._fit = value

    @property
    def remainder(self) -> str:
        """
        The part of the command that could not fit within the space provided.
        """

        return self._remainder

    @remainder.setter
    def remainder(self, value: str) -> None:
        self._remainder = value

    @property
    def packet_size(self) -> int:
        """
        The length of the ascii string that can be written to a single line.
        """

        return self._packet_size

    @packet_size.setter
    def packet_size(self, value: int) -> None:
        self._packet_size = value

    @property
    def packets_max(self) -> int:
        """
        The number of lines a command can be split over using continuations.
        """

        return self._packets_max

    @packets_max.setter
    def packets_max(self, value: int) -> None:
        self._packets_max = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.CommandTooLongExceptionData
    ) -> 'CommandTooLongExceptionData':
        instance = CommandTooLongExceptionData.__new__(
            CommandTooLongExceptionData
        )  # type: CommandTooLongExceptionData
        instance.fit = pb_data.fit
        instance.remainder = pb_data.remainder
        instance.packet_size = pb_data.packet_size
        instance.packets_max = pb_data.packets_max
        return instance
