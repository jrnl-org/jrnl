# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import base64
import logging

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .BasePasswordEncryption import BasePasswordEncryption


def is_v2_encrypted(data: bytes) -> bool:
    """Return True if data is a v2 Fernet-token journal (base64url, starts with 'gAAAAA')."""
    return data.startswith(b"gAAAAA")


class Jrnlv2Encryption(BasePasswordEncryption):
    @property
    def version(self) -> str:
        return "v2"

    def __init__(self, *args, **kwargs) -> None:
        # Salt is hard-coded. See https://github.com/jrnl-org/jrnl/security/advisories/GHSA-rhx6-37mm-5q9r
        self._salt: bytes = b"\xf2\xd5q\x0e\xc1\x8d.\xde\xdc\x8e6t\x89\x04\xce\xf8"
        self._key: bytes = b""

        super().__init__(*args, **kwargs)
        logging.debug("start")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str | None):
        self._password = value
        self._make_key()

    def _make_key(self) -> None:
        if self._password is None:
            # Password was removed after being set
            self._key = None
            return
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

    def _encrypt(self, _: str) -> bytes:
        raise NotImplementedError

    def _decrypt(self, text: bytes) -> str | None:
        logging.debug("decrypting")
        try:
            return Fernet(self._key).decrypt(text).decode(self._encoding)
        except (InvalidToken, IndexError):
            return None
