from typing import List, Union


class StructError(Exception):
    ...


def pretty_func_name(self, func):
    return f"{self.__class__.__name__}.{func.__name__}"


def PrettyNotImplementedError(self, func):
    return NotImplementedError(f"`{pretty_func_name(self, func)}` was not implemented!")


class UnpackError(StructError):
    ...


class PackError(StructError):
    ...


class ArgTypeError(PackError):
    ...


class ArgCountError(StructError):
    def __init__(self, class_or_func_name: str, received_args: int, expected_args: Union[List[int],int]):
        self.name = class_or_func_name
        self.received_args = received_args
        self.expected_args = expected_args

    def __str__(self):
        return f"'{self.name}' received '{self.received_args}' args, expected '{self.expected_args}' args!"


class UnpackBufferSizeError(UnpackError):
    def __init__(self, func_name: str, buf_size: int, expected_size: int):
        self.func_name = func_name
        self.buf_size = buf_size
        self.expected_size = expected_size

    def __str__(self):
        return f"'{self.func_name}' received a buffer with '{self.buf_size}', expected '{self.expected_size}'!"


class VarSizeError(StructError):
    def __str__(self):
        return "This struct has a variable size!"


class FixedBufferSizeError(StructError):
    def __init__(self, buf_size: int, expected_size: int):
        self.buf_size = buf_size
        self.expected_size = expected_size

    def __str__(self):
        return f"Buffer is '{self.buf_size}' bytes, expected '{self.expected_size}' bytes!"


class AlignmentError(StructError):
    ...
