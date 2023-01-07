# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
from abc import ABC
from abc import abstractmethod

from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText


class BaseEncryption(ABC):
    def __init__(self, journal_name: str, config: dict):
        logging.debug("start")
        self._encoding: str = "utf-8"
        self._journal_name: str = journal_name
        self._config: dict = config

    def clear(self) -> None:
        pass

    def encrypt(self, text: str) -> bytes:
        logging.debug("encrypting")
        return self._encrypt(text)

    def decrypt(self, text: bytes) -> str:
        logging.debug("decrypting")
        if (result := self._decrypt(text)) is None:
            raise JrnlException(
                Message(MsgText.DecryptionFailedGeneric, MsgStyle.ERROR)
            )

        return result

    @abstractmethod
    def _encrypt(self, text: str) -> bytes:
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
