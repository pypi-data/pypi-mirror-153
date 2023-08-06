# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
from typing import TYPE_CHECKING, List
from ..protobufs import main_pb2
from ..units import Units
from ..call import call, call_async
from .oscilloscope_data import OscilloscopeData

if TYPE_CHECKING:
    from .device import Device


class Oscilloscope:
    """
    Provides a convenient way to control the oscilloscope data recording feature of some devices.
    The oscilloscope can record the values of some settings over time at high resolution.
    """

    @property
    def device(self) -> 'Device':
        """
        Device that this Oscilloscope measures.
        """
        return self._device

    def __init__(self, device: 'Device'):
        self._device = device

    def add_channel(
            self,
            axis: int,
            setting: str
    ) -> None:
        """
        Select a setting to be recorded.

        Args:
            axis: The 1-based index of the axis to record the value from.
            setting: The name of a setting to record.
        """
        request = main_pb2.OscilloscopeAddChannelRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.axis = axis
        request.setting = setting
        call("oscilloscope/add_channel", request)

    async def add_channel_async(
            self,
            axis: int,
            setting: str
    ) -> None:
        """
        Select a setting to be recorded.

        Args:
            axis: The 1-based index of the axis to record the value from.
            setting: The name of a setting to record.
        """
        request = main_pb2.OscilloscopeAddChannelRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.axis = axis
        request.setting = setting
        await call_async("oscilloscope/add_channel", request)

    def clear(
            self
    ) -> None:
        """
        Clear the list of channels to record.
        """
        request = main_pb2.DeviceEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        call("oscilloscope/clear_channels", request)

    async def clear_async(
            self
    ) -> None:
        """
        Clear the list of channels to record.
        """
        request = main_pb2.DeviceEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        await call_async("oscilloscope/clear_channels", request)

    def get_timebase(
            self,
            unit: Units = Units.NATIVE
    ) -> float:
        """
        Get the current sampling interval.

        Args:
            unit: Unit of measure to represent the timebase in.

        Returns:
            The current sampling interval in the selected time units.
        """
        request = main_pb2.DeviceGetSettingRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.setting = "scope.timebase"
        request.unit = unit.value
        response = main_pb2.DoubleResponse()
        call("device/get_setting", request, response)
        return response.value

    async def get_timebase_async(
            self,
            unit: Units = Units.NATIVE
    ) -> float:
        """
        Get the current sampling interval.

        Args:
            unit: Unit of measure to represent the timebase in.

        Returns:
            The current sampling interval in the selected time units.
        """
        request = main_pb2.DeviceGetSettingRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.setting = "scope.timebase"
        request.unit = unit.value
        response = main_pb2.DoubleResponse()
        await call_async("device/get_setting", request, response)
        return response.value

    def set_timebase(
            self,
            interval: float,
            unit: Units = Units.NATIVE
    ) -> None:
        """
        Set the sampling interval.

        Args:
            interval: Sample interval for the next oscilloscope recording. Minimum value is 100µs.
            unit: Unit of measure the timebase is represented in.
        """
        request = main_pb2.DeviceSetSettingRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.setting = "scope.timebase"
        request.value = interval
        request.unit = unit.value
        call("device/set_setting", request)

    async def set_timebase_async(
            self,
            interval: float,
            unit: Units = Units.NATIVE
    ) -> None:
        """
        Set the sampling interval.

        Args:
            interval: Sample interval for the next oscilloscope recording. Minimum value is 100µs.
            unit: Unit of measure the timebase is represented in.
        """
        request = main_pb2.DeviceSetSettingRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.setting = "scope.timebase"
        request.value = interval
        request.unit = unit.value
        await call_async("device/set_setting", request)

    def get_delay(
            self,
            unit: Units = Units.NATIVE
    ) -> float:
        """
        Get the delay before oscilloscope recording starts.

        Args:
            unit: Unit of measure to represent the delay in.

        Returns:
            The current start delay in the selected time units.
        """
        request = main_pb2.DeviceGetSettingRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.setting = "scope.delay"
        request.unit = unit.value
        response = main_pb2.DoubleResponse()
        call("device/get_setting", request, response)
        return response.value

    async def get_delay_async(
            self,
            unit: Units = Units.NATIVE
    ) -> float:
        """
        Get the delay before oscilloscope recording starts.

        Args:
            unit: Unit of measure to represent the delay in.

        Returns:
            The current start delay in the selected time units.
        """
        request = main_pb2.DeviceGetSettingRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.setting = "scope.delay"
        request.unit = unit.value
        response = main_pb2.DoubleResponse()
        await call_async("device/get_setting", request, response)
        return response.value

    def set_delay(
            self,
            interval: float,
            unit: Units = Units.NATIVE
    ) -> None:
        """
        Set the sampling start delay.

        Args:
            interval: Delay time between triggering a recording and the first data point being recorded.
            unit: Unit of measure the delay is represented in.
        """
        request = main_pb2.DeviceSetSettingRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.setting = "scope.delay"
        request.value = interval
        request.unit = unit.value
        call("device/set_setting", request)

    async def set_delay_async(
            self,
            interval: float,
            unit: Units = Units.NATIVE
    ) -> None:
        """
        Set the sampling start delay.

        Args:
            interval: Delay time between triggering a recording and the first data point being recorded.
            unit: Unit of measure the delay is represented in.
        """
        request = main_pb2.DeviceSetSettingRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.setting = "scope.delay"
        request.value = interval
        request.unit = unit.value
        await call_async("device/set_setting", request)

    def start(
            self
    ) -> None:
        """
        Trigger data recording.
        """
        request = main_pb2.OscilloscopeStartStopRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.start = True
        call("oscilloscope/start_or_stop", request)

    async def start_async(
            self
    ) -> None:
        """
        Trigger data recording.
        """
        request = main_pb2.OscilloscopeStartStopRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.start = True
        await call_async("oscilloscope/start_or_stop", request)

    def stop(
            self
    ) -> None:
        """
        End data recording if currently in progress.
        """
        request = main_pb2.OscilloscopeStartStopRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.start = False
        call("oscilloscope/start_or_stop", request)

    async def stop_async(
            self
    ) -> None:
        """
        End data recording if currently in progress.
        """
        request = main_pb2.OscilloscopeStartStopRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.start = False
        await call_async("oscilloscope/start_or_stop", request)

    def read(
            self
    ) -> List[OscilloscopeData]:
        """
        Reads the last-recorded data from the oscilloscope. Will block until any in-progress recording completes.

        Returns:
            Array of recorded channel data arrays, in the order added.
        """
        request = main_pb2.DeviceEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        response = main_pb2.OscilloscopeReadResponse()
        call("oscilloscope/read", request, response)
        return list(map(OscilloscopeData, response.data_ids))

    async def read_async(
            self
    ) -> List[OscilloscopeData]:
        """
        Reads the last-recorded data from the oscilloscope. Will block until any in-progress recording completes.

        Returns:
            Array of recorded channel data arrays, in the order added.
        """
        request = main_pb2.DeviceEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        response = main_pb2.OscilloscopeReadResponse()
        await call_async("oscilloscope/read", request, response)
        return list(map(OscilloscopeData, response.data_ids))
