from __future__ import annotations

from abc import abstractmethod
from typing import Union, Protocol, TypeVar, ClassVar, runtime_checkable, _ProtocolMeta, _is_callable_members_only, _get_protocol_attrs

from structlib.byteorder import ByteOrder, resolve_byteorder
from structlib.errors import PrettyNotImplementedError

T = TypeVar("T")


# Because _abc_instancecheck is returning True, runtime_checkable is useless; to get around this, we don't fallback to ABC in this custom metaclass
#   Unfortunately, this means that if protocol recieves updates; this will become outdated
class AttrProtocolMeta(_ProtocolMeta):
    # the lack of __instancehook__.
    def __instancecheck__(cls, instance):
        # We need this method for situations where attributes are
        # assigned in __init__.
        if ((not getattr(cls, '_is_protocol', False) or
             _is_callable_members_only(cls)) and
                issubclass(instance.__class__, cls)):
            return True
        if cls._is_protocol:
            if all(hasattr(instance, attr) and
                   # All *methods* can be blocked by setting them to None.
                   (not callable(getattr(cls, attr, None)) or
                    getattr(instance, attr) is not None)
                   for attr in _get_protocol_attrs(cls)):
                return True
            else:
                return False


@runtime_checkable
class TypeDefSizable(Protocol, metaclass=AttrProtocolMeta):
    __typedef_native_size__: int


def native_size_of(typedef: TypeDefSizable):
    return typedef.__typedef_native_size__


@runtime_checkable
class TypeDefAlignable(Protocol):
    __typedef_alignment__: int

    @abstractmethod
    def __typedef_align_as__(self: T, alignment: int) -> T:
        raise PrettyNotImplementedError(self, self.__typedef_align_as__)


def align_of(typedef: TypeDefAlignable) -> int:
    return typedef.__typedef_alignment__


def align_as(typedef: T, alignment: Union[TypeDefAlignable, int]) -> T:
    if isinstance(alignment, TypeDefAlignable):
        alignment = align_of(alignment)
    return typedef.__typedef_align_as__(alignment)


class TypeDefSizableAndAlignable(TypeDefSizable, TypeDefAlignable, Protocol):
    ...


def padding_of(typedef: TypeDefSizableAndAlignable):
    alignment = align_of(typedef)
    native_size = native_size_of(typedef)
    return calculate_padding(alignment, native_size)


def size_of(typedef: TypeDefSizable):
    native_size = native_size_of(typedef)
    padding = 0
    if isinstance(typedef, TypeDefAlignable):
        alignment = align_of(typedef)
        padding = calculate_padding(alignment, native_size)
    return native_size + padding


@runtime_checkable
class TypeDefByteOrder(Protocol):
    __typedef_byteorder__: ClassVar[ByteOrder]

    @abstractmethod
    def __typedef_byteorder_as__(self: T, byteorder: ByteOrder) -> T:
        raise PrettyNotImplementedError(self, self.__typedef_byteorder_as__)


def byteorder_of(typedef: TypeDefByteOrder) -> ByteOrder:
    return typedef.__typedef_byteorder__


def byteorder_as(typedef: T, byteorder: Union[TypeDefByteOrder, ByteOrder]) -> T:
    if byteorder is None:
        byteorder = resolve_byteorder()  # For consistent behaviour, we don't just return NativeEndian
    if isinstance(byteorder, TypeDefByteOrder):
        byteorder = byteorder_of(byteorder)
    return typedef.__typedef_byteorder_as__(byteorder)


def calculate_padding(alignment: int, size_or_offset: int) -> int:
    """
    Calculates the padding required to align a buffer to a boundary.

    If using a size; the padding is the padding required to align the type to the end of it's next `over aligned` boundary (suffix padding).
    If using an offset; the padding required to align the type to the start of its next `over aligned` boundary (prefix padding).

    :param alignment: The alignment in bytes. Any multiple of this value is an alignment boundary.
    :param size_or_offset: The size/offset to calculate padding for.
    :return: The padding required in terms of bytes.
    """
    bytes_from_boundary = size_or_offset % alignment
    if bytes_from_boundary != 0:
        return alignment - bytes_from_boundary
    else:
        return 0
