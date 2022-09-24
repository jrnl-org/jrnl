# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
from abc import ABC
from abc import abstractmethod


class BaseEncryption(ABC):
    def __init__(self, config):
        self._config = config

    @abstractmethod
    def encrypt(self, text: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, text: str) -> str | None:
        pass

    @abstractmethod
    def _decrypt(self, text: str) -> str:
        """
        This is needed because self.decrypt needs
        to get a password on decryption failures
        """
        pass
