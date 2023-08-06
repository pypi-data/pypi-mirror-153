import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.HeaderMessage import HeaderMessage


@dataclasses.dataclass
class CompressedImageMessage(CBorMessage):
    header: HeaderMessage
    format: str
    data: bytearray
