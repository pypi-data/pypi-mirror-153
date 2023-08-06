from __future__ import annotations

from copy import copy
from typing import TypeVar

from structlib.byteorder import ByteOrder
from structlib.protocols.typedef import TypeDefAlignable, TypeDefByteOrder, TypeDefSizable

T = TypeVar("T")


class TypeDefAlignableABC(TypeDefAlignable):
    def __init__(self, alignment: int):
        self.__typedef_alignment__ = alignment

    def __typedef_align_as__(self: T, alignment: int) -> T:
        if self.__typedef_alignment__ == alignment:
            return self
        else:
            inst = copy(self)
            inst.__typedef_alignment__ = alignment
            return inst


class TypeDefSizableABC(TypeDefSizable):
    def __init__(self, native_size: int):
        self.__typedef_native_size__ = native_size


class TypeDefByteOrderABC(TypeDefByteOrder):
    def __init__(self, byteorder: ByteOrder):
        self.__typedef_byteorder__ = byteorder

    def __typedef_byteorder_as__(self: T, byteorder: ByteOrder) -> T:
        if self.__typedef_byteorder__ == byteorder:
            return self
        else:
            inst = copy(self)
            inst.__typedef_byteorder__ = byteorder
            return inst

