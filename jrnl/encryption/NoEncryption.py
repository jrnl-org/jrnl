# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
import logging

from jrnl.encryption.BaseEncryption import BaseEncryption


class NoEncryption(BaseEncryption):
    def __init__(self, *args, **kwargs):
        logging.debug("NoEncryption.__init__ start")
        super().__init__(*args, **kwargs)

    def _encrypt(self, text: str) -> bytes:
        return text.encode(self._encoding)

    def _decrypt(self, text: bytes) -> str:
        return text.decode(self._encoding)
