import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.QuaternionMessage import QuaternionMessage
from whoi_nlu_server_messages.Vector3Message import Vector3Message


@dataclasses.dataclass
class TransformMessage(CBorMessage):
    translation: Vector3Message
    rotation: QuaternionMessage
