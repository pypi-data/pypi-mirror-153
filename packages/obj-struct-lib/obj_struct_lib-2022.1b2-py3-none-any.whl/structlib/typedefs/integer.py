from __future__ import annotations

from typing import List, Any, Tuple

from structlib.abc_.packing import IterPackableABC, PrimitivePackableABC
from structlib.abc_.typedef import TypeDefAlignableABC, TypeDefByteOrderABC, TypeDefSizableABC
from structlib.byteorder import ByteOrder, resolve_byteorder
from structlib.protocols.packing import TPrim
from structlib.protocols.typedef import native_size_of, byteorder_of, align_of, calculate_padding
from structlib.utils import default_if_none, pretty_str, auto_pretty_repr


class IntegerDefinition(PrimitivePackableABC, IterPackableABC, TypeDefSizableABC, TypeDefAlignableABC, TypeDefByteOrderABC):
    def _to_bytes(self, *args: int):
        native_size = native_size_of(self)
        byteorder = byteorder_of(self)
        signed = self._signed
        alignment = align_of(self)
        padding = calculate_padding(alignment, native_size)
        padding_buffer = bytearray([0x00] * padding)
        packed = [int.to_bytes(arg, native_size, byteorder, signed=signed) for arg in args]
        result = padding_buffer.join(packed)  # apply suffix padding to every element except Nth
        result.extend(padding_buffer)  # Apply suffix padding to Nth element
        return result

    def _from_bytes(self, buffer: bytes, arg_count: int) -> List[int]:
        native_size = native_size_of(self)
        byteorder = byteorder_of(self)
        signed = self._signed
        alignment = align_of(self)
        padding = calculate_padding(alignment, native_size)
        size = native_size + padding
        partials = [buffer[i * size:i * size + native_size] for i in range(arg_count)]
        results = [int.from_bytes(partial, byteorder, signed=signed) for partial in partials]
        return results

    def prim_pack(self, arg: TPrim) -> bytes:
        return self._to_bytes(arg)

    def unpack_prim(self, buffer: bytes) -> int:
        return self._from_bytes(buffer, 1)[0]

    def iter_pack(self, *args: Tuple[Any, ...]) -> bytes:
        return self._to_bytes(*args)

    def iter_unpack(self, buffer: bytes, iter_count: int) -> Tuple[int, ...]:
        results = self._from_bytes(buffer, iter_count)
        return tuple(results)

    def __init__(self, byte_size: int, signed: bool, *, alignment: int = None, byteorder: ByteOrder = None):
        if byte_size < 1:
            raise ValueError("Integer cannot have a size less than 1 byte!")
        byteorder = resolve_byteorder(byteorder)
        alignment = default_if_none(alignment,byte_size)
        TypeDefSizableABC.__init__(self,byte_size)
        TypeDefAlignableABC.__init__(self,alignment)
        TypeDefByteOrderABC.__init__(self,byteorder)
        self._signed = signed

    def __eq__(self, other):
        if self is other:
            return True
        elif isinstance(other, IntegerDefinition):
            return self._signed == other._signed and \
                   self.__typedef_byteorder__ == other.__typedef_byteorder__ and \
                   self.__typedef_alignment__ == other.__typedef_alignment__ and \
                   self.__typedef_native_size__ == other.__typedef_native_size__
        else:
            return False

    def __str__(self):
        name = 'Int' if self._signed else 'Uint'
        native_size = native_size_of(self)
        size = native_size * 8
        endian = byteorder_of(self)
        alignment = align_of(self)
        return pretty_str(f"{name}{size}", endian, alignment)

    def __repr__(self):
        return auto_pretty_repr(self)


Int8 = IntegerDefinition(1, True)
Int16 = IntegerDefinition(2, True)
Int32 = IntegerDefinition(4, True)
Int64 = IntegerDefinition(8, True)
Int128 = IntegerDefinition(16, True)

UInt8 = IntegerDefinition(1, False)
UInt16 = IntegerDefinition(2, False)
UInt32 = IntegerDefinition(4, False)
UInt64 = IntegerDefinition(8, False)
UInt128 = IntegerDefinition(16, False)
