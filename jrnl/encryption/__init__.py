# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from enum import Enum
from importlib import import_module
from typing import TYPE_CHECKING
from typing import Type

if TYPE_CHECKING:
    from .BaseEncryption import BaseEncryption


class EncryptionMethods(str, Enum):
    def __str__(self) -> str:
        return self.value

    NONE = "NoEncryption"
    JRNLV1 = "Jrnlv1Encryption"
    JRNLV2 = "Jrnlv2Encryption"


def determine_encryption_method(config: str | bool) -> Type["BaseEncryption"]:
    ENCRYPTION_METHODS = {
        True: EncryptionMethods.JRNLV2,  # the default
        False: EncryptionMethods.NONE,
        "jrnlv1": EncryptionMethods.JRNLV1,
        "jrnlv2": EncryptionMethods.JRNLV2,
    }

    key = config
    if isinstance(config, str):
        key = config.lower()

    my_class = ENCRYPTION_METHODS[key]

    return getattr(import_module(f"jrnl.encryption.{my_class}"), my_class)
