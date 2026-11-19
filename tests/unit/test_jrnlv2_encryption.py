# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from cryptography.fernet import Fernet

from jrnl.encryption import detect_decryption_method
from jrnl.encryption.Jrnlv2Encryption import Jrnlv2Encryption
from jrnl.encryption.Jrnlv3Encryption import is_v3_encrypted


class TestJrnlv2Encryption:
    def test_v2_fallback(self):
        """detect_decryption_method routes v2-format data to Jrnlv2Encryption."""
        v2 = Jrnlv2Encryption("test_journal", {})
        v2.password = "test password"
        v2_ciphertext = Fernet(v2._key).encrypt("v2 entry".encode())

        assert not is_v3_encrypted(v2_ciphertext)

        # detect_decryption_method should route to Jrnlv2Encryption
        decryption_cls = detect_decryption_method(v2_ciphertext)
        assert decryption_cls is Jrnlv2Encryption

        # v2 class should decrypt it successfully
        decryptor = decryption_cls("test_journal", {})
        decryptor.password = "test password"
        assert decryptor._decrypt(v2_ciphertext) == "v2 entry"

    def test_v2_fallback_wrong_password(self):
        v2 = Jrnlv2Encryption("test_journal", {})
        v2.password = "test password"
        v2_ciphertext = Fernet(v2._key).encrypt("v2 entry".encode())

        decryption_cls = detect_decryption_method(v2_ciphertext)
        decryptor = decryption_cls("test_journal", {})
        decryptor.password = "wrong password"
        assert decryptor._decrypt(v2_ciphertext) is None
