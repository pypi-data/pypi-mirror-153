import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.HeaderMessage import HeaderMessage


@dataclasses.dataclass
class PointCloud2Message(CBorMessage):
    header: HeaderMessage
    height: int
    width: int
    is_bigendian: bool
    point_step: int
    row_step: int
    data: bytearray
    is_dense: bool
