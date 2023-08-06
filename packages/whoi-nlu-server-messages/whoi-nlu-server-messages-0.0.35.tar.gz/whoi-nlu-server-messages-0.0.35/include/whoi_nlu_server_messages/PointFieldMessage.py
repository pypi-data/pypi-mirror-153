import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class PointFieldMessage(CBorMessage):
    name: str      # Name of field
    offset: int    # Offset from start of point struct
    datatype: int  # Datatype enumeration, see above
    count: int     # How many elements in the field
