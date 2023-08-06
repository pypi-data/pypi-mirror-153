from typing import List, Tuple

from structlib.abc_.packing import IterPackableABC, PrimitivePackableABC
from structlib.abc_.typedef import TypeDefSizableABC, TypeDefAlignableABC
from structlib.protocols.typedef import align_of
from structlib.utils import default_if_none, auto_pretty_repr


class BooleanDefinition(PrimitivePackableABC, IterPackableABC, TypeDefSizableABC, TypeDefAlignableABC):
    NATIVE_SIZE = 1  # Booleans are always 1 byte

    TRUE = 0x01
    TRUE_BUF = bytes([TRUE])
    FALSE = 0x00
    FALSE_BUF = bytes([FALSE])

    def __init__(self, *, alignment: int = None):
        """
        Creates a 'class' used to pack/unpack booleans.

        :param alignment: The alignment for this type, since booleans are always 1-byte, the over-aligned buffer will always be this size.
        """
        alignment = default_if_none(alignment, self.NATIVE_SIZE)
        TypeDefSizableABC.__init__(self, self.NATIVE_SIZE)
        TypeDefAlignableABC.__init__(self, alignment)

    def __eq__(self, other):
        if self is other:
            return True
        elif isinstance(other,BooleanDefinition):
            return self.__typedef_alignment__ == other.__typedef_alignment__
        else:
            return False

    def _to_bytes(self, *args: bool) -> bytes:
        alignment = align_of(self)
        padding = alignment - self.NATIVE_SIZE
        padding_buffer = bytearray([0x00] * padding)
        packed = [self.TRUE_BUF if arg else self.FALSE_BUF for arg in args]
        result = padding_buffer.join(packed)  # apply suffix padding to every element except Nth
        result.extend(padding_buffer)  # Apply suffix padding to Nth element
        return result

    def _from_bytes(self, buffer: bytes, arg_count: int) -> List[bool]:
        alignment = align_of(self)
        size = alignment
        partials = [buffer[i * size] for i in range(arg_count)]
        results = [False if partial == self.FALSE else True for partial in partials]
        return results

    def prim_pack(self, arg: bool) -> bytes:
        return self._to_bytes(arg)

    def unpack_prim(self, buffer: bytes) -> bool:
        return self._from_bytes(buffer, 1)[0]

    def iter_pack(self, *args: Tuple[bool, ...]) -> bytes:
        return self._to_bytes(*args)

    def iter_unpack(self, buffer: bytes, iter_count: int) -> Tuple[bool, ...]:
        r = self._from_bytes(buffer, iter_count)
        return tuple(r)

    def __str__(self):
        alignment = align_of(self)
        str_align = f' @{alignment}' if alignment is None else ''
        return f"Boolean{str_align}"

    def __repr__(self):
        return auto_pretty_repr(self)


Boolean = BooleanDefinition()
