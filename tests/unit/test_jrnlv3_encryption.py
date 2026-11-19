# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import base64
import json
import struct

import pytest

from jrnl.encryption import detect_decryption_method
from jrnl.encryption.Jrnlv3Encryption import _HEADER_LEN_STRUCT_FORMAT
from jrnl.encryption.Jrnlv3Encryption import JRNL_V3_FILE_FORMAT_PREFIX
from jrnl.encryption.Jrnlv3Encryption import Jrnlv3Encryption
from jrnl.encryption.Jrnlv3Encryption import is_v3_encrypted


@pytest.fixture
def encryption():
    enc = Jrnlv3Encryption("test_journal", {})
    enc.password = "test password"
    return enc


class TestJrnlv3Encryption:
    def test_roundtrip(self, encryption):
        plaintext = "This is a test journal entry."
        ciphertext = encryption._encrypt(plaintext)
        assert is_v3_encrypted(ciphertext)
        assert encryption._decrypt(ciphertext) == plaintext

    def test_unique_salts_per_encrypt(self, encryption):
        ct1 = encryption._encrypt("same text")
        ct2 = encryption._encrypt("same text")
        salt1 = encryption._parse_header(ct1)[0]["salt"]
        salt2 = encryption._parse_header(ct2)[0]["salt"]
        assert salt1 != salt2

    def test_header_salt_is_correct_length(self, encryption):
        ciphertext = encryption._encrypt("entry")
        header, _ = encryption._parse_header(ciphertext)
        salt = base64.urlsafe_b64decode(header["salt"])
        assert len(salt) == 16

    def test_wrong_password_returns_none(self, encryption):
        ciphertext = encryption._encrypt("secret")
        encryption.password = "wrong password"
        result = encryption._decrypt(ciphertext)
        assert result is None

    def test_detect_decryption_method_returns_v3_for_v3_data(self, encryption):
        """v3-format data should route to Jrnlv3Encryption."""
        ciphertext = encryption._encrypt("v3 entry")
        assert detect_decryption_method(ciphertext) is Jrnlv3Encryption

    def test_multiline_roundtrip(self, encryption):
        text = "Line 1\nLine 2\nLine 3\n"
        ciphertext = encryption._encrypt(text)
        assert encryption._decrypt(ciphertext) == text

    def test_unicode_roundtrip(self, encryption):
        text = "日本語テスト 🎉 émojis"
        ciphertext = encryption._encrypt(text)
        assert encryption._decrypt(ciphertext) == text

    def test_oversized_header_raises(self, encryption, monkeypatch):
        import importlib

        _v3_mod = importlib.import_module("jrnl.encryption.Jrnlv3Encryption")
        monkeypatch.setattr(_v3_mod.json, "dumps", lambda *a, **kw: "x" * 0x10000)
        with pytest.raises(ValueError, match="Encryption header too large"):
            encryption._encrypt("entry")

    def test_header_is_base64_encoded_on_disk(self, encryption):
        """The header field written by _encrypt should be base64, not raw JSON."""
        ciphertext = encryption._encrypt("entry")

        offset = len(JRNL_V3_FILE_FORMAT_PREFIX)
        header_len_size = struct.calcsize(_HEADER_LEN_STRUCT_FORMAT)
        (header_len,) = struct.unpack_from(
            _HEADER_LEN_STRUCT_FORMAT, ciphertext, offset
        )
        offset += header_len_size
        header_field = ciphertext[offset : offset + header_len]

        # Raises if header_field isn't valid base64; a raw JSON header
        # (starting with b'{') would fail this with validate=True.
        decoded = base64.b64decode(header_field, validate=True)
        header = json.loads(decoded)
        assert "salt" in header

    def test_decrypt_supports_legacy_raw_json_header(self, encryption):
        """Journals written before the base64 header change should still decrypt."""
        from cryptography.fernet import Fernet

        plaintext = "an entry from before the base64 header change"
        salt = b"0123456789abcdef"
        header_json = json.dumps(
            {"salt": base64.urlsafe_b64encode(salt).decode("ascii")},
            separators=(",", ":"),
        ).encode("utf-8")

        key = encryption._make_key(salt)
        token = Fernet(key).encrypt(plaintext.encode("utf-8"))

        v3_ciphertext_without_base64 = (
            JRNL_V3_FILE_FORMAT_PREFIX
            + struct.pack(_HEADER_LEN_STRUCT_FORMAT, len(header_json))
            + header_json
            + token
        )

        assert encryption._decrypt(v3_ciphertext_without_base64) == plaintext
