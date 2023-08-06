# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
from typing import List
from ..protobufs import main_pb2
from ..call import call_sync
from ..units import Units
from .oscilloscope_capture_properties import OscilloscopeCaptureProperties


class OscilloscopeData:
    """
    Contains a block of contiguous recorded data for one channel of the device's oscilloscope.
    """

    @property
    def data_id(self) -> int:
        """
        Unique ID for this block of recorded data.
        """
        return self._data_id

    @property
    def setting(self) -> str:
        """
        The name of the recorded setting.
        """
        return self.__retrieve_properties().setting

    @property
    def axis_number(self) -> int:
        """
        The number of the axis the data was recorded from, or 0 for the controller.
        """
        return self.__retrieve_properties().axis_number

    def __init__(self, data_id: int):
        self._data_id = data_id

    def get_timebase(
            self,
            unit: Units = Units.NATIVE
    ) -> float:
        """
        Get the sample interval that this data was recorded with.

        Args:
            unit: Unit of measure to represent the timebase in.

        Returns:
            The timebase setting at the time the data was recorded.
        """
        request = main_pb2.OscilloscopeDataGetRequest()
        request.data_id = self.data_id
        request.unit = unit.value
        response = main_pb2.DoubleResponse()
        call_sync("oscilloscopedata/get_timebase", request, response)
        return response.value

    def get_delay(
            self,
            unit: Units = Units.NATIVE
    ) -> float:
        """
        Get the sample interval that this data was recorded with.

        Args:
            unit: Unit of measure to represent the delay in.

        Returns:
            The delay setting at the time the data was recorded.
        """
        request = main_pb2.OscilloscopeDataGetRequest()
        request.data_id = self.data_id
        request.unit = unit.value
        response = main_pb2.DoubleResponse()
        call_sync("oscilloscopedata/get_delay", request, response)
        return response.value

    def get_sample_time(
            self,
            index: int,
            unit: Units = Units.NATIVE
    ) -> float:
        """
        Calculate the time a sample was recorded, relative to when the recording was triggered.

        Args:
            index: 0-based index of the sample to calculate the time of.
            unit: Unit of measure to represent the calculated time in.

        Returns:
            The calculated time offset of the data sample at the given index.
        """
        request = main_pb2.OscilloscopeDataGetSampleTimeRequest()
        request.data_id = self.data_id
        request.index = index
        request.unit = unit.value
        response = main_pb2.DoubleResponse()
        call_sync("oscilloscopedata/get_sample_time", request, response)
        return response.value

    def get_data(
            self,
            unit: Units = Units.NATIVE
    ) -> List[float]:
        """
        Get the recorded data as an array of doubles.

        Args:
            unit: Unit of measure to convert the data to.

        Returns:
            The recorded data for one oscilloscope channel, converted to the units specified.
        """
        request = main_pb2.OscilloscopeDataGetRequest()
        request.data_id = self.data_id
        request.unit = unit.value
        response = main_pb2.OscilloscopeDataGetSamplesResponse()
        call_sync("oscilloscopedata/get_samples", request, response)
        return list(response.data)

    @staticmethod
    def __free(
            data_id: int
    ) -> None:
        """
        Releases native resources of an oscilloscope data buffer.

        Args:
            data_id: The ID of the data buffer to delete.
        """
        request = main_pb2.OscilloscopeDataIdentifier()
        request.data_id = data_id
        call_sync("oscilloscopedata/free", request)

    def __retrieve_properties(
            self
    ) -> OscilloscopeCaptureProperties:
        """
        Returns recording properties.

        Returns:
            Capture properties.
        """
        request = main_pb2.OscilloscopeDataIdentifier()
        request.data_id = self.data_id
        response = main_pb2.OscilloscopeCaptureProperties()
        call_sync("oscilloscopedata/get_properties", request, response)
        return OscilloscopeCaptureProperties.from_protobuf(response)

    def __del__(self) -> None:
        OscilloscopeData.__free(self.data_id)
