# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging

from jrnl.encryption.BaseEncryption import BaseEncryption


class NoEncryption(BaseEncryption):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.debug("start")

    def _encrypt(self, text: str) -> bytes:
        logging.debug("encrypting")
        return text.encode(self._encoding)

    def _decrypt(self, text: bytes) -> str:
        logging.debug("decrypting")
        return text.decode(self._encoding)
