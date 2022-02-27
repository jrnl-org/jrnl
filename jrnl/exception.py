# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
from jrnl.messages import Message
from jrnl.output import print_msg


class UserAbort(Exception):
    pass


class UpgradeValidationException(Exception):
    """Raised when the contents of an upgraded journal do not match the old journal"""

    pass


class JrnlException(Exception):
    """Common exceptions raised by jrnl."""

    def __init__(self, *messages: Message):
        self.messages = messages

    def print(self) -> None:
        for msg in self.messages:
            print_msg(msg)
