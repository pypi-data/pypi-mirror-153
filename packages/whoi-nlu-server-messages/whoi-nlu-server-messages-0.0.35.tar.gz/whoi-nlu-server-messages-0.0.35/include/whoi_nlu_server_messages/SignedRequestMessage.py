import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class SignedRequestMessage(CBorMessage):
    key: str
    payload: bytes
