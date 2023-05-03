# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from typing import TYPE_CHECKING

from jrnl.output import print_msg

if TYPE_CHECKING:
    from jrnl.messages import Message
    from jrnl.messages import MsgText


class JrnlException(Exception):
    """Common exceptions raised by jrnl."""

    def __init__(self, *messages: "Message"):
        self.messages = messages

    def print(self) -> None:
        for msg in self.messages:
            print_msg(msg)

    def has_message_text(self, message_text: "MsgText"):
        return any([m.text == message_text for m in self.messages])
