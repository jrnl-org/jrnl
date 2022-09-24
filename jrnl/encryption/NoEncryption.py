# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html


class NoEncryption:
    def __init__(self, *args, **kwargs):
        pass

    def encrypt(self, text: str) -> str:
        return text

    def decrypt(self, text: str) -> str:
        return text
