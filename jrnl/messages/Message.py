from typing import NamedTuple
from typing import Mapping

from .MsgText import MsgText
from .MsgStyle import MsgStyle


class Message(NamedTuple):
    text: MsgText
    style: MsgStyle = MsgStyle.NORMAL
    params: Mapping = {}
