# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
import logging

from jrnl.encryption.BaseEncryption import BaseEncryption
from jrnl.exception import JrnlException
from jrnl.keyring import get_keyring_password
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.prompt import create_password
from jrnl.prompt import prompt_password


class BasePasswordEncryption(BaseEncryption):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        logging.debug("BasePasswordEncryption.__init__ start")
        self._attempts: int = 0
        self._max_attempts: int = 3
        self._password: str = ""

        # Check keyring first for password.
        # That way we'll have it.
        if keyring_pw := get_keyring_password(self._journal_name):
            self.password = keyring_pw

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        self._password = value

    def encrypt(self, text: str) -> bytes:
        if not self.password:
            self.password = create_password(self._journal_name)
        return self._encrypt(text)

    def decrypt(self, text: bytes) -> str:
        logging.debug("BasePasswordEncryption decrypt start")
        if not self.password:
            self._prompt_password()

        while (result := self._decrypt(text)) is None:
            self._prompt_password()

        return result

    def _prompt_password(self) -> None:
        if self._attempts >= self._max_attempts:
            raise JrnlException(
                Message(MsgText.PasswordMaxTriesExceeded, MsgStyle.ERROR)
            )

        first_try = self._attempts == 0
        self.password = prompt_password(first_try=first_try)
        self._attempts += 1
