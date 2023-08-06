import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class NetworkDescriptionMessage(CBorMessage):
    control_hostname: str = ""
    control_port: int = 0
    data_hostname: str = ""
    data_port: int = 0
    data_heavy_hostname: str = ""
    data_heavy_port: int = 0
    speech_to_text_hostname: str = ""
    speech_to_text_port: int = 0
    h2sl_1_hostname: str = ""
    h2sl_1_port: int = 0
    h2sl_2_hostname: str = ""
    h2sl_2_port: int = 0
