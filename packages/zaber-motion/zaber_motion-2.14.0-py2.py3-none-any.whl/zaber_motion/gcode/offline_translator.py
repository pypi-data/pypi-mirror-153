# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import List, Optional
from ..call import call, call_async, call_sync

from ..protobufs import main_pb2
from ..units import Units
from .device_definition import DeviceDefinition
from .translator_config import TranslatorConfig
from .translate_result import TranslateResult


class OfflineTranslator:
    """
    Represents an offline G-Code translator.
    It allows to translate G-Code blocks to Zaber ASCII protocol stream commands.
    This translator does not need a connected device to perform translation.
    """

    @property
    def translator_id(self) -> int:
        """
        The ID of the translator that serves to identify native resources.
        """
        return self._translator_id

    @property
    def coordinate_system(self) -> str:
        """
        Current coordinate system.
        """
        return self.__get_current_coordinate_system()

    def __init__(self, translator_id: int):
        self._translator_id = translator_id

    @staticmethod
    def setup(
            definition: DeviceDefinition,
            config: Optional[TranslatorConfig] = None
    ) -> 'OfflineTranslator':
        """
        Sets up translator from provided device definition and configuration.

        Args:
            definition: Definition of device and its peripherals.
                The definition must match a device that later performs the commands.
            config: Configuration of the translator.

        Returns:
            New instance of translator.
        """
        request = main_pb2.TranslatorCreateRequest()
        request.definition.CopyFrom(DeviceDefinition.to_protobuf(definition))
        request.config.CopyFrom(TranslatorConfig.to_protobuf(config))
        response = main_pb2.TranslatorCreateResponse()
        call("gcode/create", request, response)
        return OfflineTranslator(response.translator_id)

    @staticmethod
    async def setup_async(
            definition: DeviceDefinition,
            config: Optional[TranslatorConfig] = None
    ) -> 'OfflineTranslator':
        """
        Sets up translator from provided device definition and configuration.

        Args:
            definition: Definition of device and its peripherals.
                The definition must match a device that later performs the commands.
            config: Configuration of the translator.

        Returns:
            New instance of translator.
        """
        request = main_pb2.TranslatorCreateRequest()
        request.definition.CopyFrom(DeviceDefinition.to_protobuf(definition))
        request.config.CopyFrom(TranslatorConfig.to_protobuf(config))
        response = main_pb2.TranslatorCreateResponse()
        await call_async("gcode/create", request, response)
        return OfflineTranslator(response.translator_id)

    def translate(
            self,
            block: str
    ) -> TranslateResult:
        """
        Translates a single block (line) of G-code.

        Args:
            block: Block (line) of G-code.

        Returns:
            Result of translation containing the stream commands.
        """
        request = main_pb2.TranslatorTranslateRequest()
        request.translator_id = self.translator_id
        request.block = block
        response = main_pb2.TranslatorTranslateResponse()
        call_sync("gcode/translate", request, response)
        return TranslateResult.from_protobuf(response)

    def flush(
            self
    ) -> List[str]:
        """
        Flushes the remaining stream commands waiting in optimization buffer.
        The flush is also performed by M2 and M30 codes.

        Returns:
            The remaining stream commands.
        """
        request = main_pb2.TranslatorEmptyRequest()
        request.translator_id = self.translator_id
        response = main_pb2.TranslatorFlushResponse()
        call_sync("gcode/flush", request, response)
        return list(response.commands)

    def set_traverse_rate(
            self,
            traverse_rate: float,
            unit: Units
    ) -> None:
        """
        Sets the speed at which the device moves when traversing (G0).

        Args:
            traverse_rate: The traverse rate.
            unit: Units of the traverse rate.
        """
        request = main_pb2.TranslatorSetTraverseRateRequest()
        request.translator_id = self.translator_id
        request.traverse_rate = traverse_rate
        request.unit = unit.value
        call_sync("gcode/set_traverse_rate", request)

    def set_axis_position(
            self,
            axis: str,
            position: float,
            unit: Units
    ) -> None:
        """
        Sets position of translator's axis.
        Use this method to set position after performing movement outside of the translator.
        This method does not cause any movement.

        Args:
            axis: Letter of the axis.
            position: The position.
            unit: Units of position.
        """
        request = main_pb2.TranslatorSetAxisPositionRequest()
        request.translator_id = self.translator_id
        request.axis = axis
        request.position = position
        request.unit = unit.value
        call_sync("gcode/set_axis_position", request)

    def get_axis_position(
            self,
            axis: str,
            unit: Units
    ) -> float:
        """
        Gets position of translator's axis.
        This method does not query device but returns value from translator's state.

        Args:
            axis: Letter of the axis.
            unit: Units of position.

        Returns:
            Position of translator's axis.
        """
        request = main_pb2.TranslatorGetAxisPositionRequest()
        request.translator_id = self.translator_id
        request.axis = axis
        request.unit = unit.value
        response = main_pb2.DoubleResponse()
        call_sync("gcode/get_axis_position", request, response)
        return response.value

    def set_axis_home_position(
            self,
            axis: str,
            position: float,
            unit: Units
    ) -> None:
        """
        Sets the home position of translator's axis.
        This position is used by G28.

        Args:
            axis: Letter of the axis.
            position: The home position.
            unit: Units of position.
        """
        request = main_pb2.TranslatorSetAxisPositionRequest()
        request.translator_id = self.translator_id
        request.axis = axis
        request.position = position
        request.unit = unit.value
        call_sync("gcode/set_axis_home", request)

    def set_axis_secondary_home_position(
            self,
            axis: str,
            position: float,
            unit: Units
    ) -> None:
        """
        Sets the secondary home position of translator's axis.
        This position is used by G30.

        Args:
            axis: Letter of the axis.
            position: The home position.
            unit: Units of position.
        """
        request = main_pb2.TranslatorSetAxisPositionRequest()
        request.translator_id = self.translator_id
        request.axis = axis
        request.position = position
        request.unit = unit.value
        call_sync("gcode/set_axis_secondary_home", request)

    def get_axis_coordinate_system_offset(
            self,
            coordinate_system: str,
            axis: str,
            unit: Units
    ) -> float:
        """
        Gets offset of an axis in a given coordinate system.

        Args:
            coordinate_system: Coordinate system (e.g. G54).
            axis: Letter of the axis.
            unit: Units of position.

        Returns:
            Offset in translator units of the axis.
        """
        request = main_pb2.TranslatorGetAxisOffsetRequest()
        request.translator_id = self.translator_id
        request.coordinate_system = coordinate_system
        request.axis = axis
        request.unit = unit.value
        response = main_pb2.DoubleResponse()
        call_sync("gcode/get_axis_offset", request, response)
        return response.value

    def reset_after_stream_error(
            self
    ) -> None:
        """
        Resets internal state after device rejected generated command.
        Axis positions become uninitialized.
        """
        request = main_pb2.TranslatorEmptyRequest()
        request.translator_id = self.translator_id
        call_sync("gcode/reset_after_stream_error", request)

    def set_feed_rate_override(
            self,
            coefficient: float
    ) -> None:
        """
        Allows to scale feed rate of the translated code by a coefficient.

        Args:
            coefficient: Coefficient of the original feed rate.
        """
        request = main_pb2.TranslatorSetFeedRateOverrideRequest()
        request.translator_id = self.translator_id
        request.coefficient = coefficient
        call_sync("gcode/set_feed_rate_override", request)

    @staticmethod
    def __free(
            translator_id: int
    ) -> None:
        """
        Releases native resources of a translator.

        Args:
            translator_id: The ID of the translator.
        """
        request = main_pb2.TranslatorEmptyRequest()
        request.translator_id = translator_id
        call_sync("gcode/free", request)

    def __get_current_coordinate_system(
            self
    ) -> str:
        """
        Gets current coordinate system (e.g. G54).

        Returns:
            Current coordinate system.
        """
        request = main_pb2.TranslatorEmptyRequest()
        request.translator_id = self.translator_id
        response = main_pb2.StringResponse()
        call_sync("gcode/get_current_coordinate_system", request, response)
        return response.value

    def __del__(self) -> None:
        OfflineTranslator.__free(self.translator_id)
