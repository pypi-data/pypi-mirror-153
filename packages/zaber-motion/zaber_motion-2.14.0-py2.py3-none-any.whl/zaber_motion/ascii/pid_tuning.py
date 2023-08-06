# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from ..protobufs import main_pb2


class PidTuning:
    """
    The tuning of this axis represented by PID parameters.
    """

    @property
    def type(self) -> str:
        """
        The tuning algorithm used to tune this axis.
        """

        return self._type

    @type.setter
    def type(self, value: str) -> None:
        self._type = value

    @property
    def version(self) -> int:
        """
        The version of the tuning algorithm used to tune this axis.
        """

        return self._version

    @version.setter
    def version(self, value: int) -> None:
        self._version = value

    @property
    def p(self) -> float:
        """
        The positional tuning argument.
        """

        return self._p

    @p.setter
    def p(self, value: float) -> None:
        self._p = value

    @property
    def i(self) -> float:
        """
        The integral tuning argument.
        """

        return self._i

    @i.setter
    def i(self, value: float) -> None:
        self._i = value

    @property
    def d(self) -> float:
        """
        The derivative tuning argument.
        """

        return self._d

    @d.setter
    def d(self, value: float) -> None:
        self._d = value

    @property
    def fc(self) -> float:
        """
        The frequency cutoff for the tuning.
        """

        return self._fc

    @fc.setter
    def fc(self, value: float) -> None:
        self._fc = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.PidTuning
    ) -> 'PidTuning':
        instance = PidTuning.__new__(
            PidTuning
        )  # type: PidTuning
        instance.type = pb_data.type
        instance.version = pb_data.version
        instance.p = pb_data.p
        instance.i = pb_data.i
        instance.d = pb_data.d
        instance.fc = pb_data.fc
        return instance
