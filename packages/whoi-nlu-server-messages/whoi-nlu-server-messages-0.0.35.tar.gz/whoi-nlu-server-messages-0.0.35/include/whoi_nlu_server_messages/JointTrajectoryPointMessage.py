import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.TimeMessage import TimeMessage


@dataclasses.dataclass
class JointTrajectoryPointMessage(CBorMessage):
    positions: list
    velocities: list
    accelerations: list
    effort: list
    time_from_start: TimeMessage
