# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import base64
import json
import logging
import secrets
import struct

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .BasePasswordEncryption import BasePasswordEncryption

# v3 file format:
#   b'JRNLv3'       6 bytes, magic prefix
#   header_len      2 bytes, big-endian uint16
#   header          JSON, `header_len` bytes
#   token           Fernet token, remaining bytes
#
# JSON header fields:
#   "salt"  — base64url-encoded 16-byte salt (required)
#
# Additional fields can be added to the header in future without a format
# version bump.
JRNL_V3_FILE_FORMAT_PREFIX = b"JRNLv3"
SALT_LENGTH = 16
_HEADER_LEN_STRUCT_FORMAT = ">H"  # uint16_be, max header size 65,535 bytes
_HEADER_LEN_SIZE = struct.calcsize(_HEADER_LEN_STRUCT_FORMAT)


def is_v3_encrypted(data: bytes) -> bool:
    """Return True if data is in the v3 encrypted journal format."""
    return data.startswith(JRNL_V3_FILE_FORMAT_PREFIX)


class Jrnlv3Encryption(BasePasswordEncryption):
    @property
    def version(self) -> str:
        return "v3"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        logging.debug("start")

    @staticmethod
    def _parse_header(data: bytes) -> tuple[dict, bytes]:
        """Parse the JSON header from a v3 ciphertext blob.

        Returns (header, ciphertext) where ciphertext is the Fernet token
        following the header.
        """
        offset = len(JRNL_V3_FILE_FORMAT_PREFIX)
        (header_len,) = struct.unpack_from(_HEADER_LEN_STRUCT_FORMAT, data, offset)
        offset += _HEADER_LEN_SIZE
        header = json.loads(data[offset : offset + header_len])
        return header, data[offset + header_len :]

    def _make_key(self, salt: bytes) -> bytes:
        password = self.password.encode(self._encoding)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def _encrypt(self, text: str) -> bytes:
        logging.debug("encrypting")
        salt = secrets.token_bytes(SALT_LENGTH)

        header = {"salt": base64.urlsafe_b64encode(salt).decode("ascii")}
        header_bytes = json.dumps(header, separators=(",", ":")).encode("utf-8")

        if len(header_bytes) > 0xFFFF:
            message = (
                f"Encryption header too large ({len(header_bytes)} bytes, max 65535)"
            )
            logging.error(message)
            raise ValueError(message)

        key = self._make_key(salt)
        ciphertext = Fernet(key).encrypt(text.encode(self._encoding))

        return (
            JRNL_V3_FILE_FORMAT_PREFIX
            + struct.pack(_HEADER_LEN_STRUCT_FORMAT, len(header_bytes))
            + header_bytes
            + ciphertext
        )

    def _decrypt(self, text: bytes) -> str | None:
        logging.debug("decrypting")
        if not is_v3_encrypted(text):
            return None
        try:
            header, ciphertext = self._parse_header(text)
            salt = base64.urlsafe_b64decode(header["salt"])
            key = self._make_key(salt)
            return Fernet(key).decrypt(ciphertext).decode(self._encoding)
        except (InvalidToken, KeyError, ValueError, struct.error):
            return None
