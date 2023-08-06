from abc import abstractmethod
from io import BytesIO
from typing import Tuple, Any

from structlib.abc_.packing import IterPackableABC
from structlib.abc_.typedef import TypeDefAlignableABC
from structlib.errors import PrettyNotImplementedError
from structlib.io import bufferio, streamio
from structlib.protocols.packing import TPrim, PrimitivePackable
from structlib.protocols.typedef import align_of
from structlib.typedefs.integer import IntegerDefinition
from structlib.typing_ import ReadableStream, ReadableBuffer, WritableBuffer, WritableStream
from structlib.utils import default_if_none


class LengthPrefixedPrimitiveABC(PrimitivePackable, IterPackableABC, TypeDefAlignableABC):
    """
    Represents a `Block` based `Length Prefixed` Primitive; most commonly representing collections like Arrays/strings/bytestrings.
    Internally, the `Block Size` only affects the value used when writing the length prefix, which can be used to prefix the # of elements instead of the # of bytes.
    """

    @abstractmethod
    def _internal_pack(self, arg: TPrim) -> bytes:
        """
        Should return the arg as a byte packed value (excluding the prefixed size).
        :param arg:
        :return:
        """
        raise PrettyNotImplementedError(self, self._internal_pack)

    @abstractmethod
    def _internal_unpack(self, buffer: bytes) -> TPrim:
        """
        Buffer is guaranteed to be the N bytes specified by the prefixed size, padding and the prefixed size are not included
        :param buffer:
        :return:
        """
        raise PrettyNotImplementedError(self, self._internal_unpack)

    def __size2block_count(self, size: int) -> int:
        block_size = self._block_size
        if size % block_size != 0:
            raise ValueError("Size must be a multiple of Block Size!")
        return size // block_size

    def __block_count2size(self, block_count: int) -> int:
        return block_count * self._block_size

    def __init__(self, size_type: IntegerDefinition, alignment: int = None, block_size: int = None):
        alignment = default_if_none(alignment, 1)
        TypeDefAlignableABC.__init__(self, alignment)
        self._size_type = size_type
        self._block_size = default_if_none(block_size,1)

    def prim_pack(self, arg: TPrim) -> bytes:
        packed = self._internal_pack(arg)
        block_count = self.__size2block_count(len(packed))
        size_packed = self._size_type.prim_pack(block_count)
        aligned_packed = bufferio.pad_data_to_boundary(packed, self.__typedef_alignment__)
        return b"".join([size_packed, aligned_packed])

    def prim_pack_buffer(self, buffer: WritableBuffer, arg: TPrim, *, offset: int = 0, origin: int = 0) -> int:
        packed = self.prim_pack(arg)
        alignment = align_of(self)
        return bufferio.write(buffer, packed, alignment, offset=offset, origin=origin)

    def prim_pack_stream(self, stream: WritableStream, arg: TPrim, *, origin: int = 0) -> int:
        packed = self.prim_pack(arg)
        alignment = align_of(self)
        return streamio.write(stream, packed, alignment, origin=origin)

    def unpack_prim(self, buffer: bytes) -> TPrim:
        return self.unpack_prim_buffer(buffer)[1]

    def unpack_prim_buffer(self, buffer: ReadableBuffer, *, offset: int = 0, origin: int = 0) -> Tuple[int, TPrim]:
        read, block_count = self._size_type.unpack_prim_buffer(buffer, offset=offset, origin=origin)
        var_size = self.__block_count2size(block_count)
        alignment = align_of(self)
        var_read, var_buffer = bufferio.read(buffer, var_size, alignment, offset=offset + read, origin=origin)  # var_read includes extra bytes read for alignment padding!
        return read + var_read, self._internal_unpack(var_buffer)

    def unpack_prim_stream(self, stream: ReadableStream, *, origin: int = 0) -> Tuple[int, TPrim]:
        read, block_count = self._size_type.unpack_prim_stream(stream, origin=origin)
        var_size = self.__block_count2size(block_count)
        alignment = align_of(self)
        var_read, var_buffer = streamio.read(stream, var_size, alignment, origin=origin)  # var_read includes extra bytes read for alignment padding!
        return read + var_read, self._internal_unpack(var_buffer)

    def iter_pack(self, *args: TPrim) -> bytes:
        with BytesIO() as stream:
            self.iter_pack_stream(stream, *args, origin=0)
            stream.seek(0)
            return stream.read()

    def iter_pack_buffer(self, buffer: WritableBuffer, *args: Any, offset: int, origin: int) -> int:
        total_written = 0
        for arg in args:
            total_written += self.prim_pack_buffer(buffer, arg, offset=total_written + offset, origin=origin)
        return total_written

    def iter_pack_stream(self, stream: WritableStream, *args: Any, origin: int) -> int:
        total_written = 0
        for arg in args:
            total_written += self.prim_pack_stream(stream, arg, origin=origin)
        return total_written

    def iter_unpack(self, buffer: bytes, iter_count: int) -> Tuple[TPrim, ...]:
        results = []
        total_read = 0
        for _ in range(iter_count):
            read, result = self.unpack_prim_buffer(buffer, offset=total_read)
            total_read += read
            results.append(result)
        return tuple(results)

    def iter_unpack_buffer(self, buffer: ReadableBuffer, iter_count: int, *, offset: int = 0, origin: int = 0) -> Tuple[int, Tuple[TPrim, ...]]:
        results = []
        total_read = 0
        for _ in range(iter_count):
            read, result = self.unpack_prim_buffer(buffer, offset=total_read + offset, origin=origin)
            total_read += read
            results.append(result)
        return total_read, tuple(results)

    def iter_unpack_stream(self, stream: ReadableStream, iter_count: int, *, origin: int) -> Tuple[int, Tuple[TPrim, ...]]:
        results = []
        total_read = 0
        for _ in range(iter_count):
            read, result = self.unpack_prim_stream(stream, origin=origin)
            total_read += read
            results.append(result)
        return total_read, tuple(results)


class LengthPrefixedBytes(LengthPrefixedPrimitiveABC):
    def _internal_pack(self, arg: bytes) -> bytes:
        return arg

    def _internal_unpack(self, buffer: bytes) -> bytes:
        return buffer
