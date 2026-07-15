# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from unittest.mock import patch

from jrnl.prompt import create_password

PASSWORD_ENTRY = ["hunter2", "hunter2"]


class TestCreatePasswordOnePasswordOffer:
    def test_offers_onepassword_when_available_and_unconfigured(self):
        config = {}
        with (
            patch("jrnl.prompt.print_msg", side_effect=PASSWORD_ENTRY),
            patch("jrnl.prompt.yesno", side_effect=[True, True]),
            patch(
                "jrnl.encryption.OnePasswordBackend.OnePasswordBackend.is_available",
                return_value=True,
            ),
            patch("jrnl.keyring.set_keyring_password") as set_keyring_password,
        ):
            create_password("default", config)

        assert config["keyring_backend"] == "onepassword"
        set_keyring_password.assert_called_once_with("hunter2", "default", config)

    def test_keeps_os_keychain_when_user_declines_onepassword(self):
        config = {}
        with (
            patch("jrnl.prompt.print_msg", side_effect=PASSWORD_ENTRY),
            patch("jrnl.prompt.yesno", side_effect=[True, False]),
            patch(
                "jrnl.encryption.OnePasswordBackend.OnePasswordBackend.is_available",
                return_value=True,
            ),
            patch("jrnl.keyring.set_keyring_password") as set_keyring_password,
        ):
            create_password("default", config)

        assert "keyring_backend" not in config
        set_keyring_password.assert_called_once_with("hunter2", "default", config)

    def test_does_not_offer_when_op_cli_unavailable(self):
        config = {}
        with (
            patch("jrnl.prompt.print_msg", side_effect=PASSWORD_ENTRY),
            patch("jrnl.prompt.yesno", side_effect=[True]) as yesno,
            patch(
                "jrnl.encryption.OnePasswordBackend.OnePasswordBackend.is_available",
                return_value=False,
            ),
            patch("jrnl.keyring.set_keyring_password") as set_keyring_password,
        ):
            create_password("default", config)

        assert "keyring_backend" not in config
        assert yesno.call_count == 1
        set_keyring_password.assert_called_once_with("hunter2", "default", config)

    def test_does_not_offer_when_keyring_backend_already_configured(self):
        config = {"keyring_backend": "onepassword"}
        with (
            patch("jrnl.prompt.print_msg", side_effect=PASSWORD_ENTRY),
            patch("jrnl.prompt.yesno", side_effect=[True]) as yesno,
            patch(
                "jrnl.encryption.OnePasswordBackend.OnePasswordBackend.is_available",
                return_value=True,
            ),
            patch("jrnl.keyring.set_keyring_password") as set_keyring_password,
        ):
            create_password("default", config)

        assert yesno.call_count == 1
        set_keyring_password.assert_called_once_with("hunter2", "default", config)

    def test_does_not_offer_when_user_declines_keychain_storage(self):
        config = {}
        with (
            patch("jrnl.prompt.print_msg", side_effect=PASSWORD_ENTRY),
            patch("jrnl.prompt.yesno", side_effect=[False]) as yesno,
            patch(
                "jrnl.encryption.OnePasswordBackend.OnePasswordBackend.is_available",
                return_value=True,
            ),
            patch("jrnl.keyring.set_keyring_password") as set_keyring_password,
        ):
            create_password("default", config)

        assert "keyring_backend" not in config
        assert yesno.call_count == 1
        set_keyring_password.assert_not_called()
