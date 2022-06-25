# Copyright (C) 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from typing import Mapping
from typing import NamedTuple

from .MsgStyle import MsgStyle
from .MsgText import MsgText


class Message(NamedTuple):
    text: MsgText
    style: MsgStyle = MsgStyle.NORMAL
    params: Mapping = {}
