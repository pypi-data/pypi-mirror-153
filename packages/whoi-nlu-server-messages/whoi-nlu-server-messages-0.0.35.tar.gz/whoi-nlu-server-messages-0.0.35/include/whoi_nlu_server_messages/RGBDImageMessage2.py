import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.HeaderMessage import HeaderMessage


@dataclasses.dataclass
class RGBDImageMessage2(CBorMessage):
    header: HeaderMessage
    format: str
    data: bytearray
    # Depth data uses raw image instead of compressed
    d_height: int
    d_width: int
    d_format: str
    d_is_bigendian: int
    d_step: int
    d_data: bytearray

    # Projection/camera matrix
    #     [fx'  0  cx' Tx]
    # P = [ 0  fy' cy' Ty]
    #     [ 0   0   1   0]
    P: list
