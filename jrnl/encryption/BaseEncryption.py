# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
from abc import ABC
from abc import abstractmethod

from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText


class BaseEncryption(ABC):
    _encoding: str
    _journal_name: str

    def __init__(self, journal_name, config):
        self._encoding = "utf-8"
        self._journal_name = journal_name
        self._config = config

    def encrypt(self, text: str) -> str:
        return self._encrypt(text)

    def decrypt(self, text: bytes) -> str:
        if (result := self._decrypt(text)) is None:
            raise JrnlException(
                Message(MsgText.DecryptionFailedGeneric, MsgStyle.ERROR)
            )

        return result

    @abstractmethod
    def _encrypt(self, text: str) -> str:
        """
        This is needed because self.decrypt might need
        to perform actions (e.g. prompt for password)
        before actually encrypting.
        """
        pass

    @abstractmethod
    def _decrypt(self, text: bytes) -> str | None:
        """
        This is needed because self.decrypt might need
        to perform actions (e.g. prompt for password)
        before actually decrypting.
        """
        pass