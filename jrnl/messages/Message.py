# Copyright (C) 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from typing import NamedTuple
from typing import Mapping

from .MsgText import MsgText
from .MsgStyle import MsgStyle


class Message(NamedTuple):
    text: MsgText
    style: MsgStyle = MsgStyle.NORMAL
    params: Mapping = {}
