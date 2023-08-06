import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class QuaternionMessage(CBorMessage):
    x: float
    y: float
    z: float
    w: float

    @staticmethod
    def from_ros_quaternion_msg(msg):
        return QuaternionMessage(
            x=msg.x,
            y=msg.y,
            z=msg.z,
            w=msg.w,
        )

