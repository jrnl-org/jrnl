# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
from enum import Enum
from importlib import import_module

from .BaseEncryption import BaseEncryption


class EncryptionMethods(str, Enum):
    NONE = "NoEncryption"
    JRNLV1 = "Jrnlv1Encryption"
    JRNLV2 = "Jrnlv2Encryption"


def determine_encryption_method(config: str | bool) -> BaseEncryption:
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
