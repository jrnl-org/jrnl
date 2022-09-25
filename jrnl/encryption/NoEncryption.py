# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
from jrnl.encryption.BaseEncryption import BaseEncryption


class NoEncryption(BaseEncryption):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _encrypt(self, text: str) -> str:
        return text

    def _decrypt(self, text: str) -> str:
        return text
