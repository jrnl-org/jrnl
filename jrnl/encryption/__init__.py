# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
from importlib import import_module

ENCRYPTION_METHODS = {
    # config: classname (as string)
    "default": "NoEncryption",
    False: "NoEncryption",
    True: "Jrnlv2Encryption",
    "jrnlv1": "Jrnlv1Encryption",
    "jrnlv2": "Jrnlv2Encryption",
}


def determine_encryption_method(config):
    key = config
    if isinstance(config, str):
        key = config.lower()

    my_class = ENCRYPTION_METHODS.get(key, "default")

    return getattr(import_module(f"jrnl.encryption.{my_class}"), my_class)
