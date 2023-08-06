from __future__ import annotations

from io import BytesIO
from typing import Any, Union, Tuple

from structlib.abc_.packing import StructPackableABC
from structlib.abc_.typedef import TypeDefAlignableABC, TypeDefSizableABC
from structlib.io import bufferio, streamio
from structlib.protocols.packing import nested_pack, unpack_buffer
from structlib.protocols.typedef import TypeDefSizable, TypeDefAlignable, align_of, TypeDefSizableAndAlignable, size_of, native_size_of, calculate_padding
from structlib.typedefs.array import AnyPackableTypeDef


def _max_align_of(*types: TypeDefAlignable):
    alignments = []
    for _type in types:
        alignment = align_of(_type)
        if alignment is None:  # type is not complete!
            return None
        else:
            alignments.append(alignment)
    return max(alignments) if len(alignments) > 0 else None


def _combined_size(*types: TypeDefSizableAndAlignable):
    size = 0
    max_align = 1
    for t in types:
        t_align = align_of(t)
        max_align = max(max_align, t_align)
        t_prefix_pad = calculate_padding(t_align, size)
        t_native_size = native_size_of(t)
        t_postfix_pad = calculate_padding(t_align, t_native_size)
        size += t_prefix_pad + t_native_size + t_postfix_pad

    pad_to_max = calculate_padding(max_align, size)
    size += pad_to_max
    return size


class Struct(StructPackableABC, TypeDefSizableABC, TypeDefAlignableABC):
    def struct_pack(self, *args: Any) -> bytes:
        if self._fixed_size:
            written = 0
            buffer = bytearray(size_of(self))
            for arg, t in zip(args, self._types):
                packed = nested_pack(t, arg)  # TODO; check if this fails when t is Struct because Tuple/List is wrapped
                written += bufferio.write(buffer, packed, align_of(t), written, origin=0)
            return buffer
        else:
            with BytesIO() as stream:
                for arg, t in zip(args, self._types):
                    packed = nested_pack(t, arg)  # TODO; check if this fails when t is Struct because Tuple/List is wrapped
                    streamio.write(stream, packed, align_of(t), origin=0)
                stream.seek(0)
                return stream.read()

    def struct_unpack(self, buffer: bytes) -> Tuple[Any, ...]:
        total_read = 0
        results = []
        for t in self._types:
            read, result = unpack_buffer(t, buffer, offset=total_read, origin=0)
            results.append(result)
            total_read += read
        return tuple(results)

    def __init__(self, *types: Union[AnyPackableTypeDef, AnyPackableTypeDef], alignment: int = None):
        if alignment is None:
            alignment = _max_align_of(*types)
        self._fixed_size = all(isinstance(t, TypeDefSizable) for t in types)
        if self._fixed_size:
            try:
                size = _combined_size(*types)
                TypeDefSizableABC.__init__(self, size)
            except:  # TODO narrow exception
                # delattr(self, "__typedef_native_size__")
                ...
        else:
            ...
            # delattr(self, "__typedef_native_size__")

        TypeDefAlignableABC.__init__(self, alignment)
        self._types = types

    def __eq__(self, other):
        if self is other:
            return True
        elif isinstance(other, Struct):
            return self._fixed_size == other._fixed_size and \
                   self.__typedef_alignment__ == other.__typedef_alignment__ and \
                   self.__typedef_native_size__ == other.__typedef_native_size__ and \
                   self._types == other._types
