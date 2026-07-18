# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from unittest.mock import patch

from jrnl.encryption.Jrnlv3Encryption import Jrnlv3Encryption


def _encrypted_blob(password: str, plaintext: str = "hello") -> bytes:
    enc = Jrnlv3Encryption("test", {})
    enc.password = password
    return enc._encrypt(plaintext)


class TestDecryptKeyringOffer:
    def test_offers_by_default_when_password_not_in_keyring(self):
        config = {}
        blob = _encrypted_blob("hunter2")
        enc = Jrnlv3Encryption("test", config)

        with (
            patch(
                "jrnl.encryption.BasePasswordEncryption.get_keyring_password",
                return_value=None,
            ),
            patch(
                "jrnl.encryption.BasePasswordEncryption.prompt_password",
                return_value="hunter2",
            ),
            patch(
                "jrnl.encryption.BasePasswordEncryption"
                ".offer_to_store_password_in_keyring"
            ) as offer,
        ):
            result = enc.decrypt(blob)

        assert result == "hello"
        offer.assert_called_once_with("hunter2", "test", config)

    def test_does_not_offer_when_password_came_from_keyring(self):
        config = {}
        blob = _encrypted_blob("hunter2")
        enc = Jrnlv3Encryption("test", config)

        with (
            patch(
                "jrnl.encryption.BasePasswordEncryption.get_keyring_password",
                return_value="hunter2",
            ),
            patch(
                "jrnl.encryption.BasePasswordEncryption"
                ".offer_to_store_password_in_keyring"
            ) as offer,
        ):
            result = enc.decrypt(blob)

        assert result == "hello"
        offer.assert_not_called()

    def test_does_not_offer_when_disabled_via_config(self):
        config = {"prompt_to_add_to_keyring_on_successful_decrypt": False}
        blob = _encrypted_blob("hunter2")
        enc = Jrnlv3Encryption("test", config)

        with (
            patch(
                "jrnl.encryption.BasePasswordEncryption.get_keyring_password",
                return_value=None,
            ),
            patch(
                "jrnl.encryption.BasePasswordEncryption.prompt_password",
                return_value="hunter2",
            ),
            patch(
                "jrnl.encryption.BasePasswordEncryption"
                ".offer_to_store_password_in_keyring"
            ) as offer,
        ):
            result = enc.decrypt(blob)

        assert result == "hello"
        offer.assert_not_called()

    def test_does_not_offer_when_check_keyring_is_false(self):
        config = {}
        blob = _encrypted_blob("hunter2")
        enc = Jrnlv3Encryption("test", config)
        enc.check_keyring = False

        with (
            patch(
                "jrnl.encryption.BasePasswordEncryption.prompt_password",
                return_value="hunter2",
            ),
            patch(
                "jrnl.encryption.BasePasswordEncryption"
                ".offer_to_store_password_in_keyring"
            ) as offer,
        ):
            result = enc.decrypt(blob)

        assert result == "hello"
        offer.assert_not_called()
