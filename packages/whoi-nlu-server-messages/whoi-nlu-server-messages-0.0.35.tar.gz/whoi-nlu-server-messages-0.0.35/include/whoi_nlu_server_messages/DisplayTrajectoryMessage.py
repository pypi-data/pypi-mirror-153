import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.JointTrajectoryMessage import JointTrajectoryMessage
from whoi_nlu_server_messages.RobotStateMessage import RobotStateMessage


@dataclasses.dataclass
class DisplayTrajectoryMessage(CBorMessage):
    model_id: str
    trajectory: JointTrajectoryMessage
    trajectory_start: RobotStateMessage
