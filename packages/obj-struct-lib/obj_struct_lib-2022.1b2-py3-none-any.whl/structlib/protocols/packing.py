from abc import abstractmethod
from typing import Protocol, Tuple, TypeVar, Any, runtime_checkable, Type, Union

from structlib.errors import PrettyNotImplementedError, ArgCountError, pretty_func_name
from structlib.typing_ import WritableBuffer, ReadableBuffer, ReadableStream, WritableStream


@runtime_checkable
class Packable(Protocol):
    @abstractmethod
    def pack(self, args: Any) -> bytes:
        raise PrettyNotImplementedError(self, self.pack)

    @abstractmethod
    def unpack(self, buffer: bytes) -> Any:
        raise PrettyNotImplementedError(self, self.unpack)

    @abstractmethod
    def pack_buffer(self, buffer: WritableBuffer, args: Any, offset: int, origin: int) -> int:
        raise PrettyNotImplementedError(self, self.pack_buffer)

    @abstractmethod
    def unpack_buffer(self, buffer: ReadableBuffer, *, offset: int, origin: int) -> Tuple[int, Any]:
        raise PrettyNotImplementedError(self, self.unpack_buffer)

    @abstractmethod
    def pack_stream(self, stream: WritableStream, args: Any, origin: int) -> int:
        raise PrettyNotImplementedError(self, self.pack_stream)

    @abstractmethod
    def unpack_stream(self, stream: ReadableStream, *, origin: int) -> Tuple[int, Any]:
        raise PrettyNotImplementedError(self, self.unpack_stream)


@runtime_checkable
class IterPackable(Protocol):
    @abstractmethod
    def iter_pack(self, *args: Any) -> bytes:
        raise PrettyNotImplementedError(self, self.iter_pack)

    @abstractmethod
    def iter_unpack(self, buffer: bytes, iter_count: int) -> Any:
        raise PrettyNotImplementedError(self, self.iter_unpack)

    @abstractmethod
    def iter_pack_buffer(self, buffer: WritableBuffer, *args: Any, offset: int, origin: int) -> int:
        raise PrettyNotImplementedError(self, self.iter_pack_buffer)

    @abstractmethod
    def iter_unpack_buffer(self, buffer: ReadableBuffer, iter_count: int, *, offset: int, origin: int) -> Tuple[int, Any]:
        raise PrettyNotImplementedError(self, self.iter_unpack_buffer)

    @abstractmethod
    def iter_pack_stream(self, stream: WritableStream, *args: Any, origin: int) -> int:
        raise PrettyNotImplementedError(self, self.iter_pack_stream)

    @abstractmethod
    def iter_unpack_stream(self, stream: ReadableStream, iter_count: int, *, origin: int) -> Tuple[int, Any]:
        raise PrettyNotImplementedError(self, self.iter_unpack_stream)


TPrim = TypeVar("TPrim")
TPrimTuple = Tuple[TPrim, ...]


@runtime_checkable
class PrimitivePackable(Protocol):
    @abstractmethod
    def prim_pack(self, arg: TPrim) -> bytes:
        raise PrettyNotImplementedError(self, self.prim_pack)

    @abstractmethod
    def unpack_prim(self, buffer: bytes) -> TPrim:
        raise PrettyNotImplementedError(self, self.unpack_prim)

    @abstractmethod
    def prim_pack_buffer(self, buffer: WritableBuffer, arg: TPrim, *, offset: int = 0, origin: int = 0) -> int:
        raise PrettyNotImplementedError(self, self.prim_pack_buffer)

    @abstractmethod
    def unpack_prim_buffer(self, buffer: ReadableBuffer, *, offset: int = 0, origin: int = 0) -> Tuple[int, TPrim]:
        raise PrettyNotImplementedError(self, self.unpack_prim_buffer)

    @abstractmethod
    def prim_pack_stream(self, buffer: WritableStream, arg: TPrim, *, origin: int = 0) -> int:
        raise PrettyNotImplementedError(self, self.prim_pack_stream)

    @abstractmethod
    def unpack_prim_stream(self, buffer: ReadableStream, *, origin: int = 0) -> Tuple[int, TPrim]:
        raise PrettyNotImplementedError(self, self.unpack_prim_stream)


DClass = TypeVar("DClass")
DClassType = Type[DClass]
DClassTuple = Tuple[DClass, ...]


@runtime_checkable
class DataclassPackable(Protocol):
    @abstractmethod
    def dclass_pack(self: DClass) -> bytes:
        raise PrettyNotImplementedError(self, self.dclass_pack)

    @classmethod
    @abstractmethod
    def dclass_unpack(cls: DClassType, buffer: bytes) -> DClass:
        raise PrettyNotImplementedError(cls, cls.dclass_unpack)

    @abstractmethod
    def dclass_pack_buffer(self: DClass, buffer: WritableBuffer, *, offset: int, origin: int) -> int:
        raise PrettyNotImplementedError(self, self.dclass_pack_buffer)

    @classmethod
    @abstractmethod
    def dclass_unpack_buffer(cls: DClassType, buffer: ReadableBuffer, *, offset: int, origin: int) -> Tuple[int, DClass]:
        raise PrettyNotImplementedError(cls, cls.dclass_unpack_buffer)

    @abstractmethod
    def dclass_pack_stream(self: DClass, stream: WritableStream, *, origin: int) -> int:
        raise PrettyNotImplementedError(self, self.dclass_pack_stream)

    @classmethod
    @abstractmethod
    def dclass_unpack_stream(cls: DClassType, stream: ReadableStream, *, origin: int) -> Tuple[int, DClass]:
        raise PrettyNotImplementedError(cls, cls.dclass_unpack_stream)


@runtime_checkable
class ConstPackable(Protocol):
    """
    A special packable for 'const' types; types that should know how to pack/unpack themselves without arguments.

    Padding / Constant Bytes / Data which should be ignored
    """

    @abstractmethod
    def const_pack(self) -> bytes:
        raise PrettyNotImplementedError(self, self.const_pack)

    @abstractmethod
    def const_unpack(self, buffer: bytes) -> None:
        raise PrettyNotImplementedError(self, self.const_unpack)

    @abstractmethod
    def const_pack_buffer(self, buffer: WritableBuffer, *, offset: int, origin: int) -> int:
        raise PrettyNotImplementedError(self, self.const_pack_buffer)

    @abstractmethod
    def const_unpack_buffer(self, buffer: ReadableBuffer, *, offset: int, origin: int) -> Tuple[int, None]:
        raise PrettyNotImplementedError(self, self.const_unpack_buffer)

    @abstractmethod
    def const_pack_stream(self, stream: WritableStream, *, origin: int) -> int:
        raise PrettyNotImplementedError(self, self.const_pack_stream)

    @abstractmethod
    def const_unpack_stream(self, stream: ReadableStream, *, origin: int) -> Tuple[int, None]:
        raise PrettyNotImplementedError(self, self.const_unpack_stream)


@runtime_checkable
class StructPackable(Protocol):
    @abstractmethod
    def struct_pack(self, *args: Any) -> bytes:
        raise PrettyNotImplementedError(self, self.struct_pack)

    @abstractmethod
    def struct_unpack(self, buffer: bytes) -> Tuple[Any, ...]:
        raise PrettyNotImplementedError(self, self.struct_unpack)

    @abstractmethod
    def struct_pack_buffer(self, buffer: WritableBuffer, *args: Any, offset: int, origin: int) -> int:
        raise PrettyNotImplementedError(self, self.struct_pack_buffer)

    @abstractmethod
    def struct_unpack_buffer(self, buffer: ReadableBuffer, *, offset: int, origin: int) -> Tuple[int, Tuple[Any, ...]]:
        raise PrettyNotImplementedError(self, self.struct_unpack_buffer)

    @abstractmethod
    def struct_pack_stream(self, stream: WritableStream, *args: Any, origin: int) -> int:
        raise PrettyNotImplementedError(self, self.struct_pack_stream)

    @abstractmethod
    def struct_unpack_stream(self, stream: ReadableStream, *, origin: int) -> Tuple[int, Tuple[Any, ...]]:
        raise PrettyNotImplementedError(self, self.struct_unpack_stream)


EXP_PRIM_ARGS = 1
EXP_DCLASS_ARGS = [0, 1]


def PrettyTypeError(self, proto):
    return TypeError(f"`{self.__class__.__name__}` does not implement an explicit `{proto.__class__.__name__}` protocol!")


AnyPackable = Union[Packable, StructPackable, PrimitivePackable, DataclassPackable]


@runtime_checkable
class DataclassIterPackable(Protocol):
    @classmethod
    @abstractmethod
    def iter_dclass_pack(cls: DClassType, *args: DClass) -> bytes:
        raise PrettyNotImplementedError(cls, cls.iter_dclass_pack)

    @classmethod
    @abstractmethod
    def iter_dclass_unpack(cls: DClassType, buffer: bytes, iter_count: int) -> DClassTuple:
        raise PrettyNotImplementedError(cls, cls.iter_dclass_unpack)

    @classmethod
    @abstractmethod
    def iter_dclass_pack_buffer(cls: DClassType, buffer: WritableBuffer, *args: DClass, offset: int, origin: int) -> int:
        raise PrettyNotImplementedError(cls, cls.iter_dclass_pack_buffer)

    @classmethod
    @abstractmethod
    def iter_dclass_unpack_buffer(cls: DClassType, buffer: ReadableBuffer, iter_count: int, *, offset: int, origin: int) -> Tuple[int, DClassTuple]:
        raise PrettyNotImplementedError(cls, cls.iter_dclass_unpack_buffer)

    @classmethod
    @abstractmethod
    def iter_dclass_pack_stream(cls: DClassType, stream: WritableStream, *args: DClass, origin: int) -> int:
        raise PrettyNotImplementedError(cls, cls.iter_dclass_pack_stream)

    @classmethod
    @abstractmethod
    def iter_dclass_unpack_stream(cls: DClassType, stream: ReadableStream, iter_count: int, *, origin: int) -> Tuple[int, DClassTuple]:
        raise PrettyNotImplementedError(cls, cls.iter_dclass_unpack_stream)


@runtime_checkable
class ConstIterPackable(Protocol):
    @classmethod
    @abstractmethod
    def iter_const_pack(cls, *args: DClass) -> bytes:
        raise PrettyNotImplementedError(cls, cls.iter_const_pack)

    @classmethod
    @abstractmethod
    def iter_const_unpack(cls, buffer: bytes, iter_count: int) -> None:
        raise PrettyNotImplementedError(cls, cls.iter_const_unpack)

    @classmethod
    @abstractmethod
    def iter_const_pack_buffer(cls, buffer: WritableBuffer, *, offset: int, origin: int) -> int:
        raise PrettyNotImplementedError(cls, cls.iter_const_pack_buffer)

    @classmethod
    @abstractmethod
    def iter_const_unpack_buffer(cls: DClassType, buffer: ReadableBuffer, iter_count: int, *, offset: int, origin: int) -> Tuple[int, None]:
        raise PrettyNotImplementedError(cls, cls.iter_dclass_unpack_buffer)

    @classmethod
    @abstractmethod
    def iter_const_pack_stream(cls, stream: WritableStream, *, origin: int) -> int:
        raise PrettyNotImplementedError(cls, cls.iter_const_pack_stream)

    @classmethod
    @abstractmethod
    def iter_const_unpack_stream(cls, stream: ReadableStream, iter_count: int, *, origin: int) -> Tuple[int, None]:
        raise PrettyNotImplementedError(cls, cls.iter_const_unpack_stream)


def pack(self: AnyPackable, *args: Any) -> bytes:
    """
    Calls an appropriate 'Packable' implementation using the universal 'Packable' signature.

    The first Packable implementation found is used, and is checked in this order:
        Packable, StructPackable, PrimitivePackable, DataclassPackable

    Interpretation of args varies when using Struct, Primitive, Dataclass, or Packable.
        Packable: *args is not modified
        Struct: *args is not modified
        Primitive: only `args[0]` is used; raises ArgCountError if len(args) != 1
        Dataclass: `args[0]` is used IF specified; raises ArgCountError if len(args) not in [0,1]

    :param self: The `Packable` instance or class object
    :param args: The arguments to pass to the proper packable implementation
    :return:
    """
    arg_count = len(args)
    if isinstance(self, Packable):
        return self.pack(*args)
    elif isinstance(self, StructPackable):
        return self.struct_pack(*args)
    elif isinstance(self, PrimitivePackable):
        if arg_count != EXP_PRIM_ARGS:
            raise ArgCountError(pretty_func_name(self, self.prim_pack), arg_count, EXP_PRIM_ARGS)
        return self.prim_pack(args[0])
    elif isinstance(self, DataclassPackable):
        if arg_count not in EXP_DCLASS_ARGS:
            raise ArgCountError(pretty_func_name(self, self.dclass_pack), arg_count, EXP_DCLASS_ARGS)
        dclass_self: DataclassPackable = self if arg_count == 0 else args[0]
        return dclass_self.dclass_pack()
    else:
        raise PrettyTypeError(self, Packable)


def nested_pack(self: AnyPackable, args: Any) -> bytes:
    """
    A `safe` version of pack that will properly pack / unpack args when `parsing` args in a struct


    :param self: The `Packable` instance or class object
    :param args: The arguments to pass to the proper packable implementation
    :return:
    """
    if isinstance(self, Packable):
        return self.pack(*args)
    elif isinstance(self, StructPackable):
        return self.struct_pack(*args)
    elif isinstance(self, PrimitivePackable):
        return self.prim_pack(args)
    elif isinstance(self, DataclassPackable):
        dclass_self: DataclassPackable = self if args is None else args
        return dclass_self.dclass_pack()
    else:
        raise PrettyTypeError(self, Packable)


def unpack(self, buffer: bytes) -> Any:
    if isinstance(self, Packable):
        return self.unpack(buffer)
    elif isinstance(self, StructPackable):
        return self.struct_unpack(buffer)
    elif isinstance(self, PrimitivePackable):
        return self.unpack_prim(buffer)
    elif isinstance(self, DataclassPackable):
        return self.dclass_unpack(buffer)
    else:
        raise PrettyTypeError(self, Packable)


def pack_buffer(self, buffer: WritableBuffer, *args: Any, offset: int, origin: int) -> int:
    arg_count = len(args)
    if isinstance(self, Packable):
        return self.pack_buffer(buffer, *args, offset=offset, origin=origin)
    elif isinstance(self, StructPackable):
        return self.struct_pack_buffer(buffer, *args, offset=offset, origin=origin)
    elif isinstance(self, PrimitivePackable):
        if arg_count != EXP_PRIM_ARGS:
            raise ArgCountError(pretty_func_name(self, self.prim_pack_buffer), arg_count, EXP_PRIM_ARGS)
        return self.prim_pack_buffer(buffer, args[0], offset=offset, origin=origin)
    elif isinstance(self, DataclassPackable):
        if arg_count not in EXP_DCLASS_ARGS:
            raise ArgCountError(pretty_func_name(self, self.dclass_pack_buffer), arg_count, EXP_DCLASS_ARGS)
        dclass_self: DataclassPackable = self if arg_count == 0 else args[0]
        return dclass_self.dclass_pack_buffer(buffer, offset=offset, origin=origin)
    else:
        raise PrettyTypeError(self, Packable)


def unpack_buffer(self, buffer: ReadableBuffer, *, offset: int, origin: int) -> Tuple[int, Any]:
    if isinstance(self, Packable):
        return self.unpack_buffer(buffer, offset=offset, origin=origin)
    elif isinstance(self, StructPackable):
        return self.struct_unpack_buffer(buffer, offset=offset, origin=origin)
    elif isinstance(self, PrimitivePackable):
        return self.unpack_prim_buffer(buffer, offset=offset, origin=origin)
    elif isinstance(self, DataclassPackable):
        return self.dclass_unpack_buffer(buffer, offset=offset, origin=origin)
    else:
        raise PrettyTypeError(self, Packable)


def pack_stream(self, stream: WritableStream, *args: Any, origin: int) -> int:
    arg_count = len(args)
    if isinstance(self, Packable):
        return self.pack_stream(stream, *args, origin=origin)
    elif isinstance(self, StructPackable):
        return self.struct_pack_stream(stream, *args, origin=origin)
    elif isinstance(self, PrimitivePackable):
        if arg_count != EXP_PRIM_ARGS:
            raise ArgCountError(pretty_func_name(self, self.prim_pack_stream), arg_count, EXP_PRIM_ARGS)
        return self.prim_pack_stream(stream, args[0], origin=origin)
    elif isinstance(self, DataclassPackable):
        if arg_count not in EXP_DCLASS_ARGS:
            raise ArgCountError(pretty_func_name(self, self.dclass_pack_stream), arg_count, EXP_DCLASS_ARGS)
        dclass_self: DataclassPackable = self if arg_count == 0 else args[0]
        return dclass_self.dclass_pack_stream(stream, origin=origin)
    else:
        raise PrettyTypeError(self, Packable)


def unpack_stream(self, stream: ReadableStream, *, origin: int) -> Tuple[int, Any]:
    if isinstance(self, Packable):
        return self.unpack_stream(stream, origin=origin)
    elif isinstance(self, StructPackable):
        return self.struct_unpack_stream(stream, origin=origin)
    elif isinstance(self, PrimitivePackable):
        return self.unpack_prim_stream(stream, origin=origin)
    elif isinstance(self, DataclassPackable):
        return self.dclass_unpack_stream(stream, origin=origin)
    else:
        raise PrettyTypeError(self, Packable)


def iter_pack(self, *args: Any) -> bytes:
    if isinstance(self, IterPackable):
        return self.iter_pack(*args)
    else:
        raise PrettyTypeError(self, IterPackable)


def iter_unpack(self, buffer: bytes, iter_count: int) -> Any:
    if isinstance(self, IterPackable):
        return self.iter_unpack(buffer, iter_count)
    else:
        raise PrettyTypeError(self, IterPackable)


def iter_pack_buffer(self, buffer: WritableBuffer, *args: Any, offset: int, origin: int) -> int:
    if isinstance(self, IterPackable):
        return self.iter_pack_buffer(buffer, *args, offset=offset, origin=origin)
    else:
        raise PrettyTypeError(self, IterPackable)


def iter_unpack_buffer(self, buffer: ReadableBuffer, iter_count: int, *, offset: int, origin: int) -> Tuple[int, Any]:
    if isinstance(self, IterPackable):
        return self.iter_unpack_buffer(buffer, iter_count, offset=offset, origin=origin)
    else:
        raise PrettyTypeError(self, IterPackable)


def iter_pack_stream(self, stream: WritableStream, *args: Any, origin: int) -> int:
    if isinstance(self, IterPackable):
        return self.iter_pack_stream(stream, *args, origin=origin)
    else:
        raise PrettyTypeError(self, IterPackable)


def iter_unpack_stream(self, stream: ReadableStream, iter_count: int, *, origin: int) -> Tuple[int, Any]:
    if isinstance(self, IterPackable):
        return self.iter_unpack_stream(stream, iter_count, origin=origin)
    else:
        raise PrettyTypeError(self, IterPackable)
