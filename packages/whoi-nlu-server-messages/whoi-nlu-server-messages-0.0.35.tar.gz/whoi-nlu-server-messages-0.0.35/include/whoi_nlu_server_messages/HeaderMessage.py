import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.TimeMessage import TimeMessage


@dataclasses.dataclass
class HeaderMessage(CBorMessage):
    seq: int
    stamp: TimeMessage
    frame_id: str
