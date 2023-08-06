from typing import Any, Optional, OrderedDict, Dict, Union

from structlib.byteorder import ByteOrder
from structlib.typing_ import ReadableBuffer


def generate_chunks_from_buffer(buffer: ReadableBuffer, count: int, chunk_size: int, offset: int = 0):
    """
    Useful for splitting a buffer into fixed-sized chunks.
    :param buffer: The buffer to read from
    :param count: The amount of chunks to read
    :param chunk_size: The size (in bytes) of an individual chunk
    :param offset: The offset in the buffer to read from
    :return: A generator returning each chunk as bytes
    """
    for _ in range(count):
        yield buffer[offset + _ * chunk_size:offset + (_ + 1) * chunk_size]


def pretty_repr(_repr, msg) -> str:
    """
    Inserts the msg into the 'repr' string between the first two words

    E.G.
    <MyClass (my message) object at 0x00112233>

    :param _repr: The 'repr' string to parse and modify
    :param msg: The message to insert at the first 'space' character
    :return: Repr string with `msg` inserted at the first space.
    """
    pre, post = _repr.split(" ", maxsplit=1)  # split before object
    return pre + f" ({msg}) " + post


def auto_pretty_repr(self) -> str:
    repr = super(self.__class__, self).__repr__()
    msg = str(self)
    return pretty_repr(repr, msg)


def pretty_str(name: str, endian: ByteOrder, alignment: Optional[int]):
    str_endian = f'{endian[0]}e'  # HACK, _byteorder should be one of the literals 'l'ittle or 'b'ig
    str_align = f'-@{alignment}' if alignment is None else ''
    return f"{name}-{str_endian}{str_align}"


def default_if_none(value: Any, default: Any) -> Any:
    """
    Returns default if value is None
    """
    return default if value is None else value


# Stolen from
# https://stackoverflow.com/qstions/128573/using-property-on-classmethods/64738850#64738850
# We don't use @classmethod + @property to allow <= 3.9 support
class ClassProperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


classproperty = ClassProperty  # Alias for decorator


def dataclass_str_format(cls_name: str, attrs: Union[OrderedDict[str, Any],Dict[str,Any]]):
    pairs = [f"{name}={value}" for name, value in attrs.items()]
    return f"{cls_name}({', '.join(pairs)})"
