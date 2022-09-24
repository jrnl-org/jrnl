# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
from jrnl.encryption.NoEncryption import NoEncryption


def determine_encryption_type(config):
    encryption_method = NoEncryption
    if config is True:
        # Default encryption method
        from jrnl.encryption.Jrnlv2Encryption import Jrnlv2Encryption

        encryption_method = Jrnlv2Encryption
    elif config == "jrnlv1":
        from jrnl.encryption.Jrnlv1Encryption import Jrnlv1Encryption

        encryption_method = Jrnlv1Encryption

    return encryption_method
