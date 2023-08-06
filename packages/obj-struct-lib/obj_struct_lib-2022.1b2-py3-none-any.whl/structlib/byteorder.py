import sys
from typing import Literal, Optional

ByteOrder = Literal["little", "big"]

LittleEndian: Literal["little"] = "little"
BigEndian: Literal["big"] = "big"
NetworkEndian: ByteOrder = BigEndian
NativeEndian: ByteOrder = sys.byteorder


def resolve_byteorder(*byteorder: Optional[ByteOrder], default: ByteOrder = NativeEndian):
    """
    Will resolve to the first non-None byteorder, if all byteorder objects are None, default will be used.
    :param byteorder:
    :param default:
    :return:
    """
    for bom in byteorder:
        if bom is None:
            continue
        return bom
    return default
