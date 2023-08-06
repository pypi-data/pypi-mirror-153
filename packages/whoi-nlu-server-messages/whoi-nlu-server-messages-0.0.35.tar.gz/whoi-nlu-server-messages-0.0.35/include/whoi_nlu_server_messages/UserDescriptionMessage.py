import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class UserDescriptionMessage(CBorMessage):
    name: str
    role: str
