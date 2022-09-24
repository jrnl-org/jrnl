# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
from jrnl.encryption.BaseEncryption import BaseEncryption
from jrnl.exception import JrnlException
from jrnl.keyring import get_keyring_password
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg
from jrnl.prompt import create_password


class BasePasswordEncryption(BaseEncryption):
    _attempts: int
    _journal_name: str
    _max_attempts: int
    _password: str | None
    _encoding: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._attempts = 0
        self._max_attempts = 3
        self._password = None
        self._encoding = "utf-8"

        # Check keyring first to be ready for decryption
        get_keyring_password(self._config["journal"])

        # Prompt for password if keyring didn't work
        if self.password is None:
            self._prompt_password()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    def encrypt(self, text):
        if self.password is None:
            self.password = create_password(self._config["journal"])
        return self._encrypt(text)

    def decrypt(self, text):
        while (result := self._decrypt(text)) is None:
            self._prompt_password()

        return result

    def _prompt_password(self):
        if self._attempts >= self._max_attempts:
            raise JrnlException(
                Message(MsgText.PasswordMaxTriesExceeded, MsgStyle.ERROR)
            )

        if self._attempts > 0:
            print_msg(Message(MsgText.WrongPasswordTryAgain, MsgStyle.WARNING))

        self._attempts += 1
        self.password = print_msg(
            Message(MsgText.Password, MsgStyle.PROMPT),
            get_input=True,
            hide_input=True,
        )
