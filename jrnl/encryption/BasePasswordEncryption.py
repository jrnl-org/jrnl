# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
from jrnl.encryption.BaseEncryption import BaseEncryption
from jrnl.keyring import get_keyring_password
from jrnl.prompt import create_password
from jrnl.prompt import prompt_password


class BasePasswordEncryption(BaseEncryption):
    _attempts: int
    _max_attempts: int
    _password: str | None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._attempts = 0
        self._max_attempts = 3
        self._password = None

        # Check keyring first for password.
        # That way we'll have it.
        if keyring_pw := get_keyring_password(self._journal_name):
            self.password = keyring_pw

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    def encrypt(self, text):
        if self.password is None:
            self.password = create_password(self._journal_name)
        return self._encrypt(text)

    def decrypt(self, text: bytes) -> str:
        if self.password is None:
            self._prompt_password()
        while (result := self._decrypt(text)) is None:
            self._prompt_password()

        return result

    def _prompt_password(self):
        self._attempts, self.password = prompt_password(
            self._attempts, self._max_attempts
        )
