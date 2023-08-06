# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
from typing import List
from ..protobufs import main_pb2
from ..call import call, call_async
from .axis import Axis
from .servo_tuning_paramset import ServoTuningParamset
from .paramset_info import ParamsetInfo
from .servo_tuning_param import ServoTuningParam
from .simple_tuning_param_definition import SimpleTuningParamDefinition
from .pid_tuning import PidTuning


class ServoTuner:
    """
    Exposes the capabilities to inspect and edit an axis' servo tuning.
    """

    @property
    def axis(self) -> Axis:
        """
        The axis that will be tuned.
        """
        return self._axis

    def __init__(self, axis: Axis):
        self._axis = axis

    def get_startup_paramset(
            self
    ) -> ServoTuningParamset:
        """
        Get the paramset that this device uses by default when it starts up.

        Returns:
            The paramset used at when the device restarts.
        """
        request = main_pb2.AxisEmptyRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        response = main_pb2.IntResponse()
        call("servotuning/get_startup_set", request, response)
        return ServoTuningParamset(response.value)

    async def get_startup_paramset_async(
            self
    ) -> ServoTuningParamset:
        """
        Get the paramset that this device uses by default when it starts up.

        Returns:
            The paramset used at when the device restarts.
        """
        request = main_pb2.AxisEmptyRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        response = main_pb2.IntResponse()
        await call_async("servotuning/get_startup_set", request, response)
        return ServoTuningParamset(response.value)

    def set_startup_paramset(
            self,
            paramset: ServoTuningParamset
    ) -> None:
        """
        Set the paramset that this device uses by default when it starts up.

        Args:
            paramset: The paramset to use at startup.
        """
        request = main_pb2.ServoTuningRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        call("servotuning/set_startup_set", request)

    async def set_startup_paramset_async(
            self,
            paramset: ServoTuningParamset
    ) -> None:
        """
        Set the paramset that this device uses by default when it starts up.

        Args:
            paramset: The paramset to use at startup.
        """
        request = main_pb2.ServoTuningRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        await call_async("servotuning/set_startup_set", request)

    def load_paramset(
            self,
            to_paramset: ServoTuningParamset,
            from_paramset: ServoTuningParamset
    ) -> None:
        """
        Load the values from one paramset into another.

        Args:
            to_paramset: The paramset to load into.
            from_paramset: The paramset to load from.
        """
        request = main_pb2.LoadParamset()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.to_paramset = to_paramset.value
        request.from_paramset = from_paramset.value
        call("servotuning/load_paramset", request)

    async def load_paramset_async(
            self,
            to_paramset: ServoTuningParamset,
            from_paramset: ServoTuningParamset
    ) -> None:
        """
        Load the values from one paramset into another.

        Args:
            to_paramset: The paramset to load into.
            from_paramset: The paramset to load from.
        """
        request = main_pb2.LoadParamset()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.to_paramset = to_paramset.value
        request.from_paramset = from_paramset.value
        await call_async("servotuning/load_paramset", request)

    def get_tuning(
            self,
            paramset: ServoTuningParamset
    ) -> ParamsetInfo:
        """
        Get the full set of tuning parameters used by the firmware driving this axis.

        Args:
            paramset: The paramset to get tuning for.

        Returns:
            The raw representation of the current tuning.
        """
        request = main_pb2.ServoTuningRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        response = main_pb2.ParamsetInfo()
        call("servotuning/get_raw", request, response)
        return ParamsetInfo.from_protobuf(response)

    async def get_tuning_async(
            self,
            paramset: ServoTuningParamset
    ) -> ParamsetInfo:
        """
        Get the full set of tuning parameters used by the firmware driving this axis.

        Args:
            paramset: The paramset to get tuning for.

        Returns:
            The raw representation of the current tuning.
        """
        request = main_pb2.ServoTuningRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        response = main_pb2.ParamsetInfo()
        await call_async("servotuning/get_raw", request, response)
        return ParamsetInfo.from_protobuf(response)

    def set_tuning(
            self,
            paramset: ServoTuningParamset,
            tuning_params: List[ServoTuningParam]
    ) -> None:
        """
        Set individual tuning parameters.
        Only use this method if you have a strong understanding of Zaber specific tuning parameters.

        Args:
            paramset: The paramset to set tuning of.
            tuning_params: The params to set.
        """
        request = main_pb2.SetServoTuningRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        request.tuning_params.extend([ServoTuningParam.to_protobuf(a) for a in tuning_params])
        call("servotuning/set_raw", request)

    async def set_tuning_async(
            self,
            paramset: ServoTuningParamset,
            tuning_params: List[ServoTuningParam]
    ) -> None:
        """
        Set individual tuning parameters.
        Only use this method if you have a strong understanding of Zaber specific tuning parameters.

        Args:
            paramset: The paramset to set tuning of.
            tuning_params: The params to set.
        """
        request = main_pb2.SetServoTuningRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        request.tuning_params.extend([ServoTuningParam.to_protobuf(a) for a in tuning_params])
        await call_async("servotuning/set_raw", request)

    def set_pid_tuning(
            self,
            paramset: ServoTuningParamset,
            p: float,
            i: float,
            d: float,
            fc: float
    ) -> PidTuning:
        """
        Sets the tuning of a paramset using the PID method.

        Args:
            paramset: The paramset to get tuning for.
            p: The proportional gain. Must be in units of N/m.
            i: The integral gain. Must be in units of N/m⋅s.
            d: The derivative gain. Must be in units of N⋅s/m.
            fc: The cutoff frequency. Must be in units of Hz.

        Returns:
            The PID representation of the current tuning after your changes have been applied.
        """
        request = main_pb2.SetServoTuningPIDRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        request.p = p
        request.i = i
        request.d = d
        request.fc = fc
        response = main_pb2.PidTuning()
        call("servotuning/set_pid", request, response)
        return PidTuning.from_protobuf(response)

    async def set_pid_tuning_async(
            self,
            paramset: ServoTuningParamset,
            p: float,
            i: float,
            d: float,
            fc: float
    ) -> PidTuning:
        """
        Sets the tuning of a paramset using the PID method.

        Args:
            paramset: The paramset to get tuning for.
            p: The proportional gain. Must be in units of N/m.
            i: The integral gain. Must be in units of N/m⋅s.
            d: The derivative gain. Must be in units of N⋅s/m.
            fc: The cutoff frequency. Must be in units of Hz.

        Returns:
            The PID representation of the current tuning after your changes have been applied.
        """
        request = main_pb2.SetServoTuningPIDRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        request.p = p
        request.i = i
        request.d = d
        request.fc = fc
        response = main_pb2.PidTuning()
        await call_async("servotuning/set_pid", request, response)
        return PidTuning.from_protobuf(response)

    def get_pid_tuning(
            self,
            paramset: ServoTuningParamset
    ) -> PidTuning:
        """
        Gets the PID representation of this paramset's servo tuning.

        Args:
            paramset: The paramset to get tuning for.

        Returns:
            The PID representation of the current tuning.
        """
        request = main_pb2.ServoTuningRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        response = main_pb2.PidTuning()
        call("servotuning/get_pid", request, response)
        return PidTuning.from_protobuf(response)

    async def get_pid_tuning_async(
            self,
            paramset: ServoTuningParamset
    ) -> PidTuning:
        """
        Gets the PID representation of this paramset's servo tuning.

        Args:
            paramset: The paramset to get tuning for.

        Returns:
            The PID representation of the current tuning.
        """
        request = main_pb2.ServoTuningRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        response = main_pb2.PidTuning()
        await call_async("servotuning/get_pid", request, response)
        return PidTuning.from_protobuf(response)

    def get_simple_tuning_param_definitions(
            self
    ) -> List[SimpleTuningParamDefinition]:
        """
        Gets the parameters that are required to tune this device.

        Returns:
            The tuning parameters.
        """
        request = main_pb2.AxisEmptyRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        response = main_pb2.GetSimpleTuningParamDefinitionResponse()
        call("servotuning/get_simple_params_definition", request, response)
        return [SimpleTuningParamDefinition.from_protobuf(a) for a in response.params]

    async def get_simple_tuning_param_definitions_async(
            self
    ) -> List[SimpleTuningParamDefinition]:
        """
        Gets the parameters that are required to tune this device.

        Returns:
            The tuning parameters.
        """
        request = main_pb2.AxisEmptyRequest()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        response = main_pb2.GetSimpleTuningParamDefinitionResponse()
        await call_async("servotuning/get_simple_params_definition", request, response)
        return [SimpleTuningParamDefinition.from_protobuf(a) for a in response.params]

    def set_simple_tuning(
            self,
            paramset: ServoTuningParamset,
            tuning_params: List[ServoTuningParam],
            load_mass: float,
            carriage_mass: float = -1.0
    ) -> None:
        """
        Set the tuning of this device using the simple input method.

        Args:
            paramset: The paramset to set tuning for.
            tuning_params: The params used to tune this device.
                To get what parameters are expected, call GetSimpleTuningParamList.
                All values must be between 0 and 1.
            load_mass: The mass loaded on the stage (excluding the mass of the carriage itself) in kg.
            carriage_mass: The mass of the carriage in kg. If this value is not set the default carriage mass is used.
        """
        request = main_pb2.SetSimpleTuning()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        request.tuning_params.extend([ServoTuningParam.to_protobuf(a) for a in tuning_params])
        request.load_mass = load_mass
        request.carriage_mass = carriage_mass
        call("servotuning/set_simple_tuning", request)

    async def set_simple_tuning_async(
            self,
            paramset: ServoTuningParamset,
            tuning_params: List[ServoTuningParam],
            load_mass: float,
            carriage_mass: float = -1.0
    ) -> None:
        """
        Set the tuning of this device using the simple input method.

        Args:
            paramset: The paramset to set tuning for.
            tuning_params: The params used to tune this device.
                To get what parameters are expected, call GetSimpleTuningParamList.
                All values must be between 0 and 1.
            load_mass: The mass loaded on the stage (excluding the mass of the carriage itself) in kg.
            carriage_mass: The mass of the carriage in kg. If this value is not set the default carriage mass is used.
        """
        request = main_pb2.SetSimpleTuning()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        request.tuning_params.extend([ServoTuningParam.to_protobuf(a) for a in tuning_params])
        request.load_mass = load_mass
        request.carriage_mass = carriage_mass
        await call_async("servotuning/set_simple_tuning", request)

    def is_using_simple_tuning(
            self,
            paramset: ServoTuningParamset,
            tuning_params: List[ServoTuningParam],
            load_mass: float,
            carriage_mass: float = -1.0
    ) -> bool:
        """
        Checks if the provided simple tuning is being stored by this paramset.

        Args:
            paramset: The paramset to set tuning for.
            tuning_params: The params used to tune this device.
                To get what parameters are expected, call GetSimpleTuningParamList.
                All values must be between 0 and 1.
            load_mass: The mass loaded on the stage (excluding the mass of the carriage itself) in kg.
            carriage_mass: The mass of the carriage in kg. If this value is not set the default carriage mass is used.

        Returns:
            True if the provided simple tuning is currently stored in this paramset.
        """
        request = main_pb2.SetSimpleTuning()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        request.tuning_params.extend([ServoTuningParam.to_protobuf(a) for a in tuning_params])
        request.load_mass = load_mass
        request.carriage_mass = carriage_mass
        response = main_pb2.BoolResponse()
        call("servotuning/is_using_simple_tuning", request, response)
        return response.value

    async def is_using_simple_tuning_async(
            self,
            paramset: ServoTuningParamset,
            tuning_params: List[ServoTuningParam],
            load_mass: float,
            carriage_mass: float = -1.0
    ) -> bool:
        """
        Checks if the provided simple tuning is being stored by this paramset.

        Args:
            paramset: The paramset to set tuning for.
            tuning_params: The params used to tune this device.
                To get what parameters are expected, call GetSimpleTuningParamList.
                All values must be between 0 and 1.
            load_mass: The mass loaded on the stage (excluding the mass of the carriage itself) in kg.
            carriage_mass: The mass of the carriage in kg. If this value is not set the default carriage mass is used.

        Returns:
            True if the provided simple tuning is currently stored in this paramset.
        """
        request = main_pb2.SetSimpleTuning()
        request.interface_id = self.axis.device.connection.interface_id
        request.device = self.axis.device.device_address
        request.axis = self.axis.axis_number
        request.paramset = paramset.value
        request.tuning_params.extend([ServoTuningParam.to_protobuf(a) for a in tuning_params])
        request.load_mass = load_mass
        request.carriage_mass = carriage_mass
        response = main_pb2.BoolResponse()
        await call_async("servotuning/is_using_simple_tuning", request, response)
        return response.value
