# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import Union
from .command_too_long_exception_data import CommandTooLongExceptionData
from ..protobufs import main_pb2
from .motion_lib_exception import MotionLibException


class CommandTooLongException(MotionLibException):
    """
    Thrown when a command is too long to be written by the ASCII protocol, even when continued across multiple lines.
    """

    @property
    def details(self) -> CommandTooLongExceptionData:
        """
        Additional data for CommandTooLongException
        """
        return self._details

    def __init__(self, message: str, custom_data: Union[bytes, CommandTooLongExceptionData]):
        MotionLibException.__init__(self, message)

        if isinstance(custom_data, CommandTooLongExceptionData):
            self._details = custom_data
        else:
            protobuf_obj = main_pb2.CommandTooLongExceptionData()
            protobuf_obj.ParseFromString(custom_data)
            self._details = CommandTooLongExceptionData.from_protobuf(protobuf_obj)
