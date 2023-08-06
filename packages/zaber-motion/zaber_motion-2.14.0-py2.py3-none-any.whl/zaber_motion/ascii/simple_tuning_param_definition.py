# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from ..protobufs import main_pb2


class SimpleTuningParamDefinition:
    """
    Information about a parameter used for the simple tuning method.
    """

    @property
    def name(self) -> str:
        """
        The name of the parameter.
        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def min_label(self) -> str:
        """
        The human readable description of the effect of a lower value on this setting.
        """

        return self._min_label

    @min_label.setter
    def min_label(self, value: str) -> None:
        self._min_label = value

    @property
    def max_label(self) -> str:
        """
        The human readable description of the effect of a higher value on this setting.
        """

        return self._max_label

    @max_label.setter
    def max_label(self, value: str) -> None:
        self._max_label = value

    @property
    def data_type(self) -> str:
        """
        How this parameter will be parsed by the tuner.
        """

        return self._data_type

    @data_type.setter
    def data_type(self, value: str) -> None:
        self._data_type = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.SimpleTuningParamDefinition
    ) -> 'SimpleTuningParamDefinition':
        instance = SimpleTuningParamDefinition.__new__(
            SimpleTuningParamDefinition
        )  # type: SimpleTuningParamDefinition
        instance.name = pb_data.name
        instance.min_label = pb_data.min_label
        instance.max_label = pb_data.max_label
        instance.data_type = pb_data.data_type
        return instance
