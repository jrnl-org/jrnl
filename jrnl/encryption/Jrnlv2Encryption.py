# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
import base64

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .BasePasswordEncryption import BasePasswordEncryption


class Jrnlv2Encryption(BasePasswordEncryption):
    def __init__(self, *args, **kwargs) -> None:
        # Salt is hard-coded
        self._salt: bytes = b"\xf2\xd5q\x0e\xc1\x8d.\xde\xdc\x8e6t\x89\x04\xce\xf8"
        self._key: bytes = b""

        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
        self._make_key()

    def _make_key(self) -> None:
        password = self.password.encode(self._encoding)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt,
            iterations=100_000,
            backend=default_backend(),
        )
        key = kdf.derive(password)
        self._key = base64.urlsafe_b64encode(key)

    def _encrypt(self, text: str) -> str:
        return (
            Fernet(self._key)
            .encrypt(text.encode(self._encoding))
            .decode(self._encoding)
        )

    def _decrypt(self, text: str) -> str | None:
        try:
            return (
                Fernet(self._key)
                .decrypt(text.encode(self._encoding))
                .decode(self._encoding)
            )
        except (InvalidToken, IndexError):
            return None
