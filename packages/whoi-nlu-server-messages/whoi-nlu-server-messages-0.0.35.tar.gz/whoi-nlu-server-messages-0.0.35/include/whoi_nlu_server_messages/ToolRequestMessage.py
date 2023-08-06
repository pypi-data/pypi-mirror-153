import dataclasses
from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.TransformMessage import TransformMessage


@dataclasses.dataclass
class ToolRequestMessage(CBorMessage):
    tool_name: str
    request: str
    tool_transform: TransformMessage
    quiver_transform: TransformMessage
