import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.HeaderMessage import HeaderMessage


@dataclasses.dataclass
class JointStateMessage(CBorMessage):
    header: HeaderMessage
    name: list
    position: list
    velocity: list
    effort: list
