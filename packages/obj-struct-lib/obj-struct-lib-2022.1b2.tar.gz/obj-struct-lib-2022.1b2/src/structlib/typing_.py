from io import BytesIO
from typing import Union, BinaryIO

ReadableBuffer = Union[bytes, bytearray]
WritableBuffer = Union[bytearray]
ReadableStream = Union[BinaryIO, BytesIO]
WritableStream = ReadableStream  # No difference in typing; class var 'readable()' signifies the difference
