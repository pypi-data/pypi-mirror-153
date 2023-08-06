from copy import copy
from typing import List, Union, Type, Any, Tuple

from structlib.abc_.packing import PrimitivePackableABC, IterPackableABC
from structlib.byteorder import ByteOrder
from structlib.protocols.packing import iter_pack, pack_buffer, iter_unpack, unpack_buffer
from structlib.protocols.typedef import TypeDefSizable, TypeDefAlignable, TypeDefByteOrder, byteorder_as, size_of, align_as, T
from structlib.utils import auto_pretty_repr, pretty_repr

AnyPackableTypeDef = Any  # TODO


class FixedCollection(PrimitivePackableABC, IterPackableABC, TypeDefSizable, TypeDefAlignable, TypeDefByteOrder):
    @property
    def __typedef_native_size__(self) -> int:  # Native size == size for arrays
        return size_of(self._backing) * self._args

    @property
    def __typedef_alignment__(self) -> int:
        return self._backing.__typedef_alignment__

    @property
    def __typedef_byteorder__(self) -> int:
        return self._backing.__typedef_byteorder__

    def __typedef_align_as__(self, alignment: int):
        if self.__typedef_alignment__ != alignment:
            inst = copy(self)
            inst._backing = align_as(self._backing, alignment)
            return inst
        else:
            return self

    def __typedef_byteorder_as__(self, byteorder: ByteOrder):
        if self.__typedef_byteorder__ != byteorder:
            inst = copy(self)
            inst._backing = byteorder_as(self._backing, byteorder)
            return inst
        else:
            return self

    def __init__(self, args: int, data_type: Union[Type[AnyPackableTypeDef], AnyPackableTypeDef]):
        self._backing = data_type
        self._args = args

    @classmethod
    def Unsized(cls:T, data_type: Union[Type[AnyPackableTypeDef], AnyPackableTypeDef]) -> T:
        """
        Helper, returns an 'unsized' Array
        :param data_type: 
        :return: 
        """
        return cls(0,data_type)

    def __eq__(self, other):
        if self is other:
            return True
        elif isinstance(other, Array):
            return self._args == other._args and \
                   self._backing == other._backing
        else:
            return False

    def __str__(self):
        return f"Array[{self._args}] of `{self._backing}`"

    def __repr__(self):
        repr = super().__repr__()
        msg = str(self)
        return pretty_repr(repr, msg)

    def prim_pack(self, args: List) -> bytes:
        try:
            return iter_pack(self._backing, *args)
        except TypeError:
            size = size_of(self)
            buffer = bytearray(size)
            written = 0
            for arg in args:
                written += pack_buffer(self._backing, buffer, arg, offset=written, origin=0)
            return buffer

    def unpack_prim(self, buffer: bytes) -> List:
        try:
            return iter_unpack(self._backing, buffer, self._args)
        except TypeError:
            total_read = 0
            results = []
            for _ in range(self._args):
                read, unpacked = unpack_buffer(self._backing, buffer, offset=total_read, origin=0)
                total_read += read
                results.append(unpacked)
            return results

    def iter_pack(self, *args: List) -> bytes:
        parts = [self.prim_pack(arg) for arg in args]
        empty = bytearray()
        return empty.join(parts)

    def iter_unpack(self, buffer: bytes, iter_count: int) -> Tuple[List, ...]:
        size = size_of(self)
        partials = [buffer[i * size:(i + 1) * size] for i in range(iter_count)]
        parts = [self.unpack_prim(partial) for partial in partials]
        return tuple(parts)


class Array(FixedCollection):
    ...

# It's too annoying when using typing.Tuple
# class Tuple(FixedCollection):
#     def unpack(self, buffer: bytes) -> _Tuple:
#         return tuple(super().unpack(buffer))
