import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.HeaderMessage import HeaderMessage


@dataclasses.dataclass
class RGBDImageMessage(CBorMessage):
    header: HeaderMessage
    height: int        # image height, that is, number of rows
    width: int         # image width, that is, number of columns
    encoding: str      # Encoding of pixels -- channel meaning, ordering, size
    # taken from the list of strings in include/sensor_msgs/image_encodings.h
    is_bigendian: int  # is this data bigendian?
    step: int          # Full row length in bytes
    data: bytearray    # actual matrix data, size is (step * rows)
    # same params as above but for depth data
    d_encoding: str
    d_is_bigendian: int
    d_step: int
    d_data: bytearray
    # Projection/camera matrix
    #     [fx'  0  cx' Tx]
    # P = [ 0  fy' cy' Ty]
    #     [ 0   0   1   0]
    P: list
