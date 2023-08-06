import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class NetworkErrorMessage(CBorMessage):
    reason: str
