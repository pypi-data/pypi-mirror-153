from __future__ import annotations

from typing import BinaryIO, Tuple

from structlib.io.bufferio import create_padding_buffer
from structlib.protocols.typedef import calculate_padding


def write(stream: BinaryIO, data: bytes, alignment: int, origin: int = 0) -> int:
    """
    Writes data to the stream
    Adds prefix/postfix padding to align to `alignment boundaries`
    :param stream:
    :param data:
    :param alignment:
    :param origin:
    :return:
    """
    offset = stream_offset_from_origin(stream, origin)
    data_size = len(data)

    prefix_padding = calculate_padding(alignment, offset)
    prefix_padding_buf = create_padding_buffer(prefix_padding)

    postfix_padding = calculate_padding(alignment, offset + prefix_padding + data_size)
    postfix_padding_buf = create_padding_buffer(postfix_padding)

    stream.write(prefix_padding_buf)
    stream.write(data)
    stream.write(postfix_padding_buf)

    return prefix_padding + data_size + postfix_padding


def read(stream: BinaryIO, data_size: int, alignment: int, origin: int = 0) -> Tuple[int, bytes]:
    offset = stream_offset_from_origin(stream, origin)

    prefix_padding = calculate_padding(alignment, offset)
    postfix_padding = calculate_padding(alignment, offset + prefix_padding + data_size)

    _prefix_padding_buf = stream.read(prefix_padding)
    data = stream.read(data_size)
    _postfix_padding_buf = stream.read(postfix_padding)

    return prefix_padding + data_size + postfix_padding, data


def stream_offset_from_origin(stream: BinaryIO, origin: int):
    return stream.tell() - origin