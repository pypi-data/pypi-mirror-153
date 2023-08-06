import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class GroundedActionParamMessage(CBorMessage):
    name: str
    value: str
