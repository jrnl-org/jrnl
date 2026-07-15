# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import hashlib
import os
from unittest.mock import patch

import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes

from jrnl.encryption import detect_decryption_method
from jrnl.encryption.Jrnlv1Encryption import Jrnlv1Encryption
from jrnl.encryption.Jrnlv3Encryption import Jrnlv3Encryption
from jrnl.encryption.Jrnlv3Encryption import is_v3_encrypted
from jrnl.journals.Journal import Journal


# The helpers below replicate the v1 encryption format originally implemented in
# LegacyEncryptedJournal._load (jrnl/EncryptedJournal.py) at:
# https://github.com/jrnl-org/jrnl/commit/fcc8d8e3fae1c50ada9584ded2a4f4da81a8a413
def _make_v1_ciphertext(plaintext: str, password: str) -> bytes:
    """Produce a v1-format ciphertext: IV || AES-CBC(PKCS7(plaintext))."""
    key = hashlib.sha256(password.encode("utf-8")).digest()
    iv = os.urandom(16)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded = padder.update(plaintext.encode("utf-8")) + padder.finalize()
    encryptor = Cipher(
        algorithms.AES(key), modes.CBC(iv), default_backend()
    ).encryptor()
    return iv + encryptor.update(padded) + encryptor.finalize()


def _make_v1_ciphertext_space_padded(plaintext: str, password: str) -> bytes:
    """Produce a v1-format ciphertext using the ancient space-padding scheme."""
    key = hashlib.sha256(password.encode("utf-8")).digest()
    iv = os.urandom(16)
    block_size = algorithms.AES.block_size // 8  # bits → bytes
    padded = plaintext.encode("utf-8")
    remainder = len(padded) % block_size
    if remainder:
        padded += b" " * (block_size - remainder)
    encryptor = Cipher(
        algorithms.AES(key), modes.CBC(iv), default_backend()
    ).encryptor()
    return iv + encryptor.update(padded) + encryptor.finalize()


class TestJrnlv1Encryption:
    def test_decrypt_correct_password(self):
        plaintext = "v1 journal entry"
        password = "test password"
        ciphertext = _make_v1_ciphertext(plaintext, password)

        v1 = Jrnlv1Encryption("test_journal", {})
        v1.password = password
        assert v1._decrypt(ciphertext) == plaintext

    def test_decrypt_wrong_password_returns_none(self):
        ciphertext = _make_v1_ciphertext("secret entry", "correct password")

        v1 = Jrnlv1Encryption("test_journal", {})
        v1.password = "wrong password"
        assert v1._decrypt(ciphertext) is None

    def test_decrypt_ancient_space_padded(self):
        """Oldest jrnl versions padded with spaces instead of PKCS7."""
        plaintext = "ancient entry"
        password = "old password"
        ciphertext = _make_v1_ciphertext_space_padded(plaintext, password)

        v1 = Jrnlv1Encryption("test_journal", {})
        v1.password = password
        assert v1._decrypt(ciphertext) == plaintext

    def test_decrypt_unicode(self):
        plaintext = "日本語テスト 🎉"
        password = "unicode password"
        ciphertext = _make_v1_ciphertext(plaintext, password)

        v1 = Jrnlv1Encryption("test_journal", {})
        v1.password = password
        assert v1._decrypt(ciphertext) == plaintext

    def test_encrypt_not_implemented(self):
        v1 = Jrnlv1Encryption("test_journal", {})
        v1.password = "any"
        with pytest.raises(NotImplementedError):
            v1._encrypt("anything")

    def test_detect_decryption_method_returns_v1_for_v1_data(self):
        """Byte-level fallback: unrecognised binary routes to Jrnlv1Encryption."""
        ciphertext = _make_v1_ciphertext("entry", "password")
        assert detect_decryption_method(ciphertext) is Jrnlv1Encryption

    def test_detect_decryption_method_returns_v1_for_jrnlv1_config(self):
        """Config hint: 'jrnlv1' routes to v1 even for data that looks like v2."""
        assert (
            detect_decryption_method(b"gAAAAA_looks_like_v2", encrypt_setting="jrnlv1")
            is Jrnlv1Encryption
        )

    def test_detect_decryption_method_v3_prefix_beats_jrnlv1_config(self):
        """v3 magic prefix always wins, even if config still says
        'jrnlv1' (post-upgrade safe)."""
        v3 = Jrnlv3Encryption("test_journal", {})
        v3.password = "pw"
        ciphertext = v3._encrypt("entry")
        assert (
            detect_decryption_method(ciphertext, encrypt_setting="jrnlv1")
            is Jrnlv3Encryption
        )


class TestJrnlv1JournalUpgrade:
    """Test that a journal with encrypt: 'jrnlv1' decrypts with v1 and
    re-encrypts as v3."""

    def test_decrypt_uses_v1_and_flags_upgrade(self):
        password = "test password"
        plaintext = "v1 journal entry"
        ciphertext = _make_v1_ciphertext(plaintext, password)

        journal = Journal("test", encrypt="jrnlv1")
        journal._reconfigure_encryption_method()

        with (
            patch("jrnl.output.print_msg"),
            patch(
                "jrnl.encryption.BasePasswordEncryption.prompt_password",
                return_value=password,
            ),
            patch(
                "jrnl.encryption.BasePasswordEncryption.DEFAULT_PROMPT_TO_ADD_TO_KEYRING_ON_SUCCESSFUL_DECRYPT",
                False,
            ),
        ):
            result = journal._decrypt(ciphertext)

        assert result == plaintext
        assert journal._upgrade_encryption_from_version == "v1"
        assert journal.encryption_method.password == password

    def test_encrypt_after_v1_decrypt_produces_v3(self):
        password = "test password"
        plaintext = "v1 journal entry"
        ciphertext = _make_v1_ciphertext(plaintext, password)

        journal = Journal("test", encrypt="jrnlv1")
        journal._reconfigure_encryption_method()

        with (
            patch("jrnl.output.print_msg"),
            patch(
                "jrnl.encryption.BasePasswordEncryption.prompt_password",
                return_value=password,
            ),
            patch(
                "jrnl.encryption.BasePasswordEncryption.DEFAULT_PROMPT_TO_ADD_TO_KEYRING_ON_SUCCESSFUL_DECRYPT",
                False,
            ),
        ):
            journal._decrypt(ciphertext)
            v3_ciphertext = journal._encrypt(plaintext)

        assert is_v3_encrypted(v3_ciphertext)
        assert journal._upgrade_encryption_from_version is None

    def test_config_updated_to_true_after_v1_upgrade(self):
        password = "test password"
        plaintext = "v1 journal entry"
        ciphertext = _make_v1_ciphertext(plaintext, password)

        journal = Journal("test", encrypt="jrnlv1")
        journal._reconfigure_encryption_method()

        with (
            patch("jrnl.output.print_msg"),
            patch(
                "jrnl.encryption.BasePasswordEncryption.prompt_password",
                return_value=password,
            ),
            patch(
                "jrnl.encryption.BasePasswordEncryption.DEFAULT_PROMPT_TO_ADD_TO_KEYRING_ON_SUCCESSFUL_DECRYPT",
                False,
            ),
        ):
            journal._decrypt(ciphertext)
            journal._encrypt(plaintext)

        assert journal.config["encrypt"] is True
        assert journal._pending_config_updates == {"encrypt": True}
