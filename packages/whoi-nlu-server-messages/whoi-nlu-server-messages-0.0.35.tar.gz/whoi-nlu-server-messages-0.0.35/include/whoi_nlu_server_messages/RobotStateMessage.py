import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.JointStateMessage import JointStateMessage


@dataclasses.dataclass
class RobotStateMessage(CBorMessage):
    joint_state: JointStateMessage
    # MultiDOFJointState
    # attached_collision_objects
    # is_diff
