# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from jrnl.messages import Message
from jrnl.output import print_msg


class JrnlException(Exception):
    """Common exceptions raised by jrnl."""

    def __init__(self, *messages: Message):
        self.messages = messages

    def print(self) -> None:
        for msg in self.messages:
            print_msg(msg)
