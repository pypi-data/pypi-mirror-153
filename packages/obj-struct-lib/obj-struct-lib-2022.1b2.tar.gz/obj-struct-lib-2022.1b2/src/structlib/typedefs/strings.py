from typing import Tuple, Any

from structlib.abc_.packing import PrimitivePackableABC, IterPackableABC, ConstPackableABC
from structlib.abc_.typedef import TypeDefSizableABC, TypeDefAlignableABC
from structlib.io import bufferio
from structlib.protocols.packing import TPrim, DataclassPackable, DClass, ConstPackable
from structlib.protocols.typedef import size_of, align_of
from structlib.typedefs.integer import IntegerDefinition
from structlib.typedefs.varlen import LengthPrefixedPrimitiveABC
from structlib.typing_ import ReadableBuffer, ReadableStream, WritableStream, WritableBuffer
from structlib.utils import default_if_none, auto_pretty_repr


class StringBuffer(PrimitivePackableABC, IterPackableABC, TypeDefSizableABC, TypeDefAlignableABC):
    """
    Represents a fixed-buffer string.

    When packing; the string will be padded to fill the buffer
    When unpacking; padding is preserved
    """

    def prim_pack(self, arg: str) -> bytes:
        encoded = arg.encode(self._encoding)
        buf = bytearray(encoded)
        size = size_of(self)
        if len(buf) > size:
            raise
        elif len(buf) < size:
            buf.extend([0x00] * (size - len(buf)))
        return buf

    def unpack_prim(self, buffer: bytes) -> str:
        return buffer.decode(encoding=self._encoding)

    def iter_pack(self, *args: str) -> bytes:
        parts = [self.prim_pack(arg) for arg in args]
        empty = bytearray()
        return empty.join(parts)

    def iter_unpack(self, buffer: bytes, iter_count: int) -> Tuple[str, ...]:
        size = size_of(self)
        partials = [buffer[i * size:(i + 1) * size] for i in range(iter_count)]
        unpacked = [self.unpack_prim(partial) for partial in partials]
        return tuple(unpacked)

    _DEFAULT_ENCODING = "ascii"

    def __init__(self, size: int, encoding: str = None, *, alignment: int = None):
        alignment = default_if_none(alignment, 1)
        TypeDefSizableABC.__init__(self, size)
        TypeDefAlignableABC.__init__(self, alignment)
        self._encoding = default_if_none(encoding, self._DEFAULT_ENCODING)

    def __eq__(self, other):
        if self is other:
            return True
        elif isinstance(other, StringBuffer):
            return self.__typedef_alignment__ == other.__typedef_alignment__ and \
                   self.__typedef_native_size__ == other.__typedef_native_size__ and \
                   self._encoding == other._encoding
        else:
            return False

    def __str__(self):
        name = f"String [{size_of(self)}] ({self._encoding})"
        alignment = align_of(self)
        align_str = f" @ {alignment}" if alignment != 1 else ""
        return f"{name}{align_str}"

    def __repr__(self):
        return auto_pretty_repr(self)


#


class PascalString(LengthPrefixedPrimitiveABC):
    """
    Represents a var-buffer string.
    """

    def _internal_pack(self, arg: TPrim) -> bytes:
        return arg.encode(self._encoding)

    def _internal_unpack(self, buffer: bytes) -> TPrim:
        return buffer.decode(self._encoding)

    _DEFAULT_ENCODING = "ascii"

    def __init__(self, size_type: IntegerDefinition, encoding: str = None, *, alignment: int = None, block_size: int = None):
        super().__init__(size_type, alignment, block_size)
        self._encoding = default_if_none(encoding, self._DEFAULT_ENCODING)

    def __eq__(self, other):
        if self is other:
            return True
        elif isinstance(other, PascalString):
            return self.__typedef_alignment__ == other.__typedef_alignment__ and \
                   self._encoding == other._encoding
        else:
            return False

    def __str__(self):
        block_info = f"-{self._block_size}" if self._block_size != 1 else ""
        name = f"PString{block_info} ({self._encoding})"
        alignment = align_of(self)
        align_str = f" @ {alignment}" if alignment != 1 else ""
        return f"{name}{align_str}"

    def __repr__(self):
        return auto_pretty_repr(self)


class CStringBuffer(StringBuffer):
    """
    A Fixed string buffer that will auto-strip trailing `\0` when unpacking.

    Otherwise, it functions identically to StringBuffer.
    """

    def unpack_prim(self, buffer: bytes) -> str:
        return buffer.decode(encoding=self._encoding).rstrip("\0")

    def __str__(self):
        return "C" + super(CStringBuffer, self).__str__()

    def __repr__(self):
        return auto_pretty_repr(self)


class MagicWord(ConstPackableABC, TypeDefAlignableABC, TypeDefSizableABC):
    """
    Represents a fixed-length magic word.
    """

    def const_pack(self) -> bytes:
        alignment = align_of(self)
        return bufferio.pad_data_to_boundary(self._magic, alignment)

    def const_unpack(self, buffer: bytes) -> None:
        d_size = len(self._magic)
        partial = buffer[:d_size]
        if partial != self._magic:
            raise AssertionError("Magic word wasn't unpacked!")  # TODO create magic error
        return None

    def __init__(self, magic: ReadableBuffer, alignment: int = None):
        size = len(magic)
        TypeDefSizableABC.__init__(self, size)
        TypeDefAlignableABC.__init__(self, default_if_none(alignment, size))
        self._magic = magic
