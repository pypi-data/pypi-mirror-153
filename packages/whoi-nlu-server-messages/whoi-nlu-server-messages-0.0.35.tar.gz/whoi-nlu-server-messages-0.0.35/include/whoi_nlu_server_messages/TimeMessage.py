import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class TimeMessage(CBorMessage):
    secs: int
    nsecs: int
