import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.HeaderMessage import HeaderMessage
from whoi_nlu_server_messages.TransformMessage import TransformMessage


@dataclasses.dataclass
class TransformStampedMessage(CBorMessage):
    header: HeaderMessage
    child_frame_id: str
    transform: TransformMessage
