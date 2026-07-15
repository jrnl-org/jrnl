# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from typing import TYPE_CHECKING
from typing import Type

if TYPE_CHECKING:
    from jrnl.encryption.BaseEncryption import BaseEncryption

# NOTE: encryption classes are imported lazily, inside each function, rather
# than at module level. Encryption libraries (cryptography, keyring) are
# expensive to import, and this module is on the startup path for every jrnl
# invocation (main -> controller -> journals -> Journal -> here). Importing
# them eagerly here would pay that cost even for commands that never touch
# encrypted data, e.g. `jrnl --help`.


def determine_encryption_method_for_writing(
    config: str | bool,
) -> Type["BaseEncryption"]:
    """Return the encryption class to use for writing, based on config.

    All encrypted journals are written as v3. Decryption format is detected
    separately by detect_decryption_method().
    """
    if not config:
        from jrnl.encryption.NoEncryption import NoEncryption

        return NoEncryption

    from jrnl.encryption.Jrnlv3Encryption import Jrnlv3Encryption

    return Jrnlv3Encryption


def detect_decryption_method(
    data: bytes, encrypt_setting=None
) -> Type["BaseEncryption"]:
    """Detect which encryption class should be used to decrypt data (i.e. what the
    on-disk format is)

    Detection order:
      1. v3 magic prefix — unambiguous, always checked first so a post-upgrade
         journal still decrypts correctly even if encrypt_setting still says 'jrnlv1'.
      2. encrypt_setting == 'jrnlv1' — explicit user declaration. Checked before
         the v2 prefix because v1 data is raw AES-CBC binary; although the
         probability is ~1/2^48, its random IV could theoretically start with
         the 'gAAAAA' Fernet prefix, causing a false v2 match without this hint.
      3. v2 Fernet prefix ('gAAAAA') — reliable for all real-world v2 tokens.
      4. fallback → v1 (untagged raw binary).
    """
    if encrypt_setting is False:
        from jrnl.encryption.NoEncryption import NoEncryption

        return NoEncryption

    from jrnl.encryption.Jrnlv3Encryption import Jrnlv3Encryption
    from jrnl.encryption.Jrnlv3Encryption import is_v3_encrypted

    if is_v3_encrypted(data):
        return Jrnlv3Encryption

    from jrnl.encryption.Jrnlv1Encryption import Jrnlv1Encryption

    if encrypt_setting == "jrnlv1":
        return Jrnlv1Encryption

    from jrnl.encryption.Jrnlv2Encryption import Jrnlv2Encryption
    from jrnl.encryption.Jrnlv2Encryption import is_v2_encrypted

    if is_v2_encrypted(data):
        return Jrnlv2Encryption

    return Jrnlv1Encryption
