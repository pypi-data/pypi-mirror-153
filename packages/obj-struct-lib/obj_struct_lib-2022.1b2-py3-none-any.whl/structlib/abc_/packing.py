from abc import ABC, abstractmethod
from typing import Tuple, BinaryIO, Any
from structlib.io import bufferio, streamio
from structlib.protocols.packing import Packable, IterPackable, StructPackable, PrimitivePackable, TPrim, DataclassPackable, DClassType, DClass, ConstPackable
from structlib.protocols.typedef import align_of, size_of, TypeDefAlignable, TypeDefSizable, T
from structlib.typing_ import WritableBuffer, ReadableBuffer, ReadableStream, WritableStream


class PackableABC(Packable, TypeDefSizable, TypeDefAlignable, ABC):
    """
    A Packable which uses pack/unpack and a fixed size typedef to perform buffer/stream operations.
    """

    def pack_buffer(self, buffer: WritableBuffer, *args: Any, offset: int, origin: int) -> int:
        packed = self.pack(*args)
        alignment = align_of(self)
        return bufferio.write(buffer, packed, alignment, offset, origin)

    def unpack_buffer(self, buffer: ReadableBuffer, *, offset: int, origin: int) -> Tuple[int, Any]:
        size = size_of(self)
        alignment = align_of(self)
        read, packed = bufferio.read(buffer, size, alignment, offset, origin)
        unpacked = self.unpack(packed)
        return read, unpacked

    def pack_stream(self, stream: BinaryIO, *args: Any, origin: int) -> int:
        packed = self.pack(*args)
        alignment = align_of(self)
        return streamio.write(stream, packed, alignment, origin)

    def unpack_stream(self, stream: BinaryIO, *, origin: int) -> Tuple[int, Any]:
        size = size_of(self)
        alignment = align_of(self)
        read, packed = streamio.read(stream, size, alignment, origin)
        unpacked = self.unpack(packed)
        return read, unpacked


class ConstPackableABC(ConstPackable, TypeDefSizable, TypeDefAlignable, ABC):
    """
    A ConstPackable which uses pack/unpack and a fixed size typedef to perform buffer/stream operations.
    """

    def const_pack_buffer(self, buffer: WritableBuffer, offset: int, origin: int) -> int:
        packed = self.const_pack()
        alignment = align_of(self)
        return bufferio.write(buffer, packed, alignment, offset, origin)

    def const_unpack_buffer(self, buffer: ReadableBuffer, *, offset: int, origin: int) -> Tuple[int, Any]:
        size = size_of(self)
        alignment = align_of(self)
        read, packed = bufferio.read(buffer, size, alignment, offset, origin)
        unpacked = self.const_unpack(packed)
        return read, unpacked

    def const_pack_stream(self, stream: BinaryIO, *args: Any, origin: int) -> int:
        packed = self.const_pack()
        alignment = align_of(self)
        return streamio.write(stream, packed, alignment, origin)

    def const_unpack_stream(self, stream: BinaryIO, *, origin: int) -> Tuple[int, Any]:
        size = size_of(self)
        alignment = align_of(self)
        read, packed = streamio.read(stream, size, alignment, origin)
        unpacked = self.const_unpack(packed)
        return read, unpacked


class IterPackableABC(IterPackable, TypeDefSizable, TypeDefAlignable, ABC):
    """
    An IterPackable which uses iter_pack/iter_unpack to perform buffer/stream operations.
    """

    def iter_pack_buffer(self, buffer: WritableBuffer, *args: Any, offset: int, origin: int) -> int:
        packed = self.iter_pack(*args)
        alignment = align_of(self)
        return bufferio.write(buffer, packed, alignment, offset, origin)

    def iter_unpack_buffer(self, buffer: ReadableBuffer, iter_count: int, *, offset: int, origin: int) -> Tuple[int, Any]:
        size = size_of(self) * iter_count
        alignment = align_of(self)
        read, packed = bufferio.read(buffer, size, alignment, offset, origin)
        unpacked = self.iter_unpack(packed, iter_count)
        return read, unpacked

    def iter_pack_stream(self, stream: BinaryIO, *args: Any, origin: int) -> int:
        packed = self.iter_pack(*args)
        alignment = align_of(self)
        return streamio.write(stream, packed, alignment, origin)

    def iter_unpack_stream(self, stream: BinaryIO, iter_count: int, *, origin: int) -> Tuple[int, Any]:
        size = size_of(self) * iter_count
        alignment = align_of(self)
        read, packed = streamio.read(stream, size, alignment, origin)
        unpacked = self.iter_unpack(packed, iter_count)
        return read, unpacked


class StructPackableABC(StructPackable, TypeDefSizable, TypeDefAlignable, ABC):
    """
    A Packable which uses pack/unpack to perform buffer/stream operations.
    """

    def struct_pack_buffer(self, buffer: WritableBuffer, *args: Any, offset: int, origin: int) -> int:
        packed = self.struct_pack(*args)
        alignment = align_of(self)
        return bufferio.write(buffer, packed, alignment, offset, origin)

    def struct_unpack_buffer(self, buffer: ReadableBuffer, *, offset: int, origin: int) -> Tuple[int, Any]:
        size = size_of(self)
        alignment = align_of(self)
        read, packed = bufferio.read(buffer, size, alignment, offset, origin)
        unpacked = self.struct_unpack(packed)
        return read, unpacked

    def struct_pack_stream(self, stream: BinaryIO, *args: Any, origin: int) -> int:
        packed = self.struct_pack(*args)
        alignment = align_of(self)
        return streamio.write(stream, packed, alignment, origin)

    def struct_unpack_stream(self, stream: BinaryIO, *, origin: int) -> Tuple[int, Any]:
        size = size_of(self)
        alignment = align_of(self)
        read, packed = streamio.read(stream, size, alignment, origin)
        unpacked = self.struct_unpack(packed)
        return read, unpacked


class PrimitivePackableABC(PrimitivePackable, TypeDefSizable, TypeDefAlignable, ABC):
    """
    A Packable which uses pack/unpack to perform buffer/stream operations.
    """

    def prim_pack_buffer(self, buffer: WritableBuffer, arg: TPrim, *, offset: int = 0, origin: int = 0) -> int:
        packed = self.prim_pack(arg)
        alignment = align_of(self)
        return bufferio.write(buffer, packed, alignment, offset, origin)

    def unpack_prim_buffer(self, buffer: ReadableBuffer, *, offset: int = 0, origin: int = 0) -> Tuple[int, TPrim]:
        size = size_of(self)
        alignment = align_of(self)
        read, packed = bufferio.read(buffer, size, alignment, offset, origin)
        unpacked = self.unpack_prim(packed)
        return read, unpacked

    def prim_pack_stream(self, stream: WritableStream, arg: TPrim, *, origin: int = 0) -> int:
        packed = self.prim_pack(arg)
        alignment = align_of(self)
        return streamio.write(stream, packed, alignment, origin)

    def unpack_prim_stream(self, stream: ReadableStream, *, origin: int = 0) -> Tuple[int, TPrim]:
        size = size_of(self)
        alignment = align_of(self)
        read, packed = streamio.read(stream, size, alignment, origin)
        unpacked = self.unpack_prim(packed)
        return read, unpacked


class DataclassPackableABC(DataclassPackable, TypeDefSizable, TypeDefAlignable, ABC):
    """
    A Packable which uses pack/unpack to perform buffer/stream operations.
    """

    def dclass_pack_buffer(self, buffer: WritableBuffer, *, offset: int = 0, origin: int = 0) -> int:
        packed = self.dclass_pack()
        alignment = align_of(self)
        return bufferio.write(buffer, packed, alignment, offset, origin)

    @classmethod
    def dclass_unpack_buffer(cls: DClassType, buffer: ReadableBuffer, *, offset: int = 0, origin: int = 0) -> Tuple[int, DClass]:
        size = size_of(cls)
        alignment = align_of(cls)
        read, packed = bufferio.read(buffer, size, alignment, offset, origin)
        unpacked = cls.dclass_unpack(packed)
        return read, unpacked

    def dclass_pack_stream(self, stream: WritableStream, *, origin: int = 0) -> int:
        packed = self.dclass_pack()
        alignment = align_of(self)
        return streamio.write(stream, packed, alignment, origin)

    @classmethod
    def dclass_unpack_stream(cls: DClassType, stream: ReadableStream, *, origin: int = 0) -> Tuple[int, DClass]:
        size = size_of(cls)
        alignment = align_of(cls)
        read, packed = streamio.read(stream, size, alignment, origin)
        unpacked = cls.dclass_unpack(packed)
        return read, unpacked
