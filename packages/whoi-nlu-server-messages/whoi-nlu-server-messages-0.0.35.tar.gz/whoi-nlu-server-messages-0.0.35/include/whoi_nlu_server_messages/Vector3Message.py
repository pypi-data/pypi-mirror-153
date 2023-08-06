import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class Vector3Message(CBorMessage):
    x: float
    y: float
    z: float

    @staticmethod
    def from_ros_vector3_msg(msg):
        return Vector3Message(
            x=msg.x,
            y=msg.y,
            z=msg.z,
        )
