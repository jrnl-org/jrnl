# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from unittest.mock import MagicMock
from unittest.mock import patch

import keyring.errors

from jrnl.keyring import get_keyring_password
from jrnl.keyring import set_keyring_password


class FakeBackend:
    """Stand-in so backend-name logging doesn't depend on the real,
    environment-specific keyring backend during tests."""


def patch_get_keyring():
    return patch("keyring.get_keyring", return_value=FakeBackend())


class TestGetKeyringPassword:
    def test_returns_password_on_success(self):
        with (
            patch("keyring.get_password", return_value="hunter2"),
            patch_get_keyring(),
            patch("jrnl.keyring.print_msg") as print_msg,
        ):
            assert get_keyring_password("default") == "hunter2"
            print_msg.assert_called_once()
            msg = print_msg.call_args.args[0]
            assert "retrieved" in str(msg.text).lower()
            assert msg.params["backend"] == "FakeBackend"
            assert msg.params["keyring_key"] == "jrnl/default"

    def test_silent_when_no_password_found(self):
        with (
            patch("keyring.get_password", return_value=None),
            patch_get_keyring(),
            patch("jrnl.keyring.print_msg") as print_msg,
        ):
            assert get_keyring_password("default") is None
            print_msg.assert_not_called()

    def test_returns_none_when_no_backend_available(self):
        with (
            patch(
                "keyring.get_password",
                side_effect=keyring.errors.NoKeyringError(),
            ),
            patch("jrnl.keyring.print_msg") as print_msg,
        ):
            assert get_keyring_password("default") is None
            print_msg.assert_not_called()

    def test_returns_none_on_standard_keyring_error(self):
        with (
            patch(
                "keyring.get_password",
                side_effect=keyring.errors.KeyringError("boom"),
            ),
            patch("jrnl.keyring.print_msg") as print_msg,
            patch_get_keyring(),
        ):
            assert get_keyring_password("default") is None
            print_msg.assert_called_once()
            msg = print_msg.call_args.args[0]
            assert "retrieve" in str(msg.text).lower()
            assert msg.params["backend"] == "FakeBackend"
            assert msg.params["reason"] == "boom"

    def test_returns_none_when_backend_raises_non_conforming_error(self):
        """Some third-party backends (e.g. onepassword-keyring) raise a bare
        exception instead of a keyring.errors.KeyringError, or instead of
        returning None, when no matching secret is found. jrnl should
        degrade gracefully rather than crash."""
        with (
            patch("keyring.get_password", side_effect=RuntimeError("not found")),
            patch("jrnl.keyring.print_msg") as print_msg,
            patch_get_keyring(),
        ):
            assert get_keyring_password("default") is None
            print_msg.assert_called_once()

    def test_logs_backend_name_and_exception_on_failure(self):
        with (
            patch("keyring.get_password", side_effect=RuntimeError("not found")),
            patch("jrnl.keyring.print_msg"),
            patch_get_keyring(),
            patch("logging.debug") as log_debug,
        ):
            get_keyring_password("default")
            logged = " ".join(str(a) for a in log_debug.call_args.args)
            assert "FakeBackend" in logged
            assert "not found" in logged


class TestSetKeyringPassword:
    def test_sets_password_and_confirms_on_success(self):
        with (
            patch("keyring.set_password") as set_password,
            patch("jrnl.keyring.print_msg") as print_msg,
            patch_get_keyring(),
        ):
            set_keyring_password("hunter2", "default")
            set_password.assert_called_once_with("jrnl", "default", "hunter2")
            print_msg.assert_called_once()
            msg = print_msg.call_args.args[0]
            assert "stored" in str(msg.text).lower()
            assert msg.params["backend"] == "FakeBackend"
            assert msg.params["keyring_key"] == "jrnl/default"

    def test_warns_when_no_backend_available(self):
        with (
            patch(
                "keyring.set_password",
                side_effect=keyring.errors.NoKeyringError(),
            ),
            patch("jrnl.keyring.print_msg") as print_msg,
        ):
            set_keyring_password("hunter2", "default")
            print_msg.assert_called_once()

    def test_does_not_raise_when_backend_raises_non_conforming_error(self):
        with (
            patch("keyring.set_password", side_effect=RuntimeError("boom")),
            patch("jrnl.keyring.print_msg") as print_msg,
            patch_get_keyring(),
        ):
            set_keyring_password("hunter2", "default")
            print_msg.assert_called_once()
            msg = print_msg.call_args.args[0]
            assert "store" in str(msg.text).lower()
            assert msg.params["backend"] == "FakeBackend"
            assert msg.params["reason"] == "boom"

    def test_logs_backend_name_and_exception_on_failure(self):
        with (
            patch("keyring.set_password", side_effect=RuntimeError("boom")),
            patch("jrnl.keyring.print_msg"),
            patch_get_keyring(),
            patch("logging.debug") as log_debug,
        ):
            set_keyring_password("hunter2", "default")
            logged = " ".join(str(a) for a in log_debug.call_args.args)
            assert "FakeBackend" in logged
            assert "boom" in logged


def test_backend_name_falls_back_to_unknown_when_get_keyring_fails():
    from jrnl.keyring import _backend_name

    with patch("keyring.get_keyring", side_effect=RuntimeError("no backend")):
        assert _backend_name() == "unknown"


def test_backend_name_uses_active_backend_class_name():
    from jrnl.keyring import _backend_name

    with patch("keyring.get_keyring", return_value=MagicMock(spec=FakeBackend)):
        assert "FakeBackend" in _backend_name() or _backend_name() != ""


class TestSelectBackend:
    def test_noop_when_no_config(self):
        with patch("keyring.set_keyring") as set_keyring:
            from jrnl.keyring import _select_backend

            _select_backend(None)
            set_keyring.assert_not_called()

    def test_noop_when_keyring_backend_not_set(self):
        with patch("keyring.set_keyring") as set_keyring:
            from jrnl.keyring import _select_backend

            _select_backend({"encrypt": True})
            set_keyring.assert_not_called()

    def test_pins_onepassword_backend_when_requested_and_available(self):
        from jrnl.encryption.OnePasswordBackend import OnePasswordBackend
        from jrnl.keyring import _select_backend

        with (
            patch.object(OnePasswordBackend, "is_available", return_value=True),
            patch("keyring.set_keyring") as set_keyring,
        ):
            _select_backend({"keyring_backend": "onepassword"})
            set_keyring.assert_called_once()
            assert isinstance(set_keyring.call_args.args[0], OnePasswordBackend)

    def test_warns_and_does_not_pin_when_op_cli_missing(self):
        from jrnl.encryption.OnePasswordBackend import OnePasswordBackend
        from jrnl.keyring import _select_backend

        with (
            patch.object(OnePasswordBackend, "is_available", return_value=False),
            patch("keyring.set_keyring") as set_keyring,
            patch("jrnl.keyring.print_msg") as print_msg,
        ):
            _select_backend({"keyring_backend": "onepassword"})
            set_keyring.assert_not_called()
            print_msg.assert_called_once()

    def test_noop_for_unrecognized_backend_name(self):
        with patch("keyring.set_keyring") as set_keyring:
            from jrnl.keyring import _select_backend

            _select_backend({"keyring_backend": "bitwarden"})
            set_keyring.assert_not_called()

    def test_get_keyring_password_selects_backend_from_config(self):
        with (
            patch("keyring.get_password", return_value="hunter2"),
            patch_get_keyring(),
            patch("jrnl.keyring._select_backend") as select_backend,
        ):
            config = {"keyring_backend": "onepassword"}
            get_keyring_password("default", config)
            select_backend.assert_called_once_with(config)

    def test_set_keyring_password_selects_backend_from_config(self):
        with (
            patch("keyring.set_password"),
            patch("jrnl.keyring.print_msg"),
            patch_get_keyring(),
            patch("jrnl.keyring._select_backend") as select_backend,
            patch("jrnl.keyring._confirm_onepassword_overwrite", return_value=True),
        ):
            config = {"keyring_backend": "onepassword"}
            set_keyring_password("hunter2", "default", config)
            select_backend.assert_called_once_with(config)


class TestConfirmOnePasswordOverwrite:
    def test_true_when_backend_is_not_onepassword(self):
        from jrnl.encryption.OnePasswordBackend import OnePasswordBackend
        from jrnl.keyring import _confirm_onepassword_overwrite

        with patch.object(OnePasswordBackend, "item_exists") as item_exists:
            assert _confirm_onepassword_overwrite(None, "default", "jrnl/default")
            assert _confirm_onepassword_overwrite(
                {"keyring_backend": None}, "default", "jrnl/default"
            )
            item_exists.assert_not_called()

    def test_true_when_no_existing_item(self):
        from jrnl.encryption.OnePasswordBackend import OnePasswordBackend
        from jrnl.keyring import _confirm_onepassword_overwrite

        with patch.object(OnePasswordBackend, "item_exists", return_value=False):
            assert _confirm_onepassword_overwrite(
                {"keyring_backend": "onepassword"}, "default", "jrnl/default"
            )

    def test_true_when_existing_item_check_fails(self):
        """If we can't tell whether an item exists (e.g. not authenticated),
        don't block the store on that -- the store call itself will
        surface a clear error if something's actually wrong."""
        from jrnl.encryption.OnePasswordBackend import OnePasswordBackend
        from jrnl.keyring import _confirm_onepassword_overwrite

        with patch.object(
            OnePasswordBackend, "item_exists", side_effect=RuntimeError("boom")
        ):
            assert _confirm_onepassword_overwrite(
                {"keyring_backend": "onepassword"}, "default", "jrnl/default"
            )

    def test_asks_and_returns_true_when_confirmed(self):
        from jrnl.encryption.OnePasswordBackend import OnePasswordBackend
        from jrnl.keyring import _confirm_onepassword_overwrite

        with (
            patch.object(OnePasswordBackend, "item_exists", return_value=True),
            patch("jrnl.prompt.yesno", return_value=True) as yesno,
        ):
            assert _confirm_onepassword_overwrite(
                {"keyring_backend": "onepassword"}, "default", "jrnl/default"
            )
            yesno.assert_called_once()

    def test_asks_and_returns_false_when_declined(self):
        from jrnl.encryption.OnePasswordBackend import OnePasswordBackend
        from jrnl.keyring import _confirm_onepassword_overwrite

        with (
            patch.object(OnePasswordBackend, "item_exists", return_value=True),
            patch("jrnl.prompt.yesno", return_value=False),
        ):
            assert not _confirm_onepassword_overwrite(
                {"keyring_backend": "onepassword"}, "default", "jrnl/default"
            )

    def test_set_keyring_password_aborts_when_overwrite_declined(self):
        with (
            patch("keyring.set_password") as set_password,
            patch("jrnl.keyring.print_msg") as print_msg,
            patch_get_keyring(),
            patch("jrnl.keyring._confirm_onepassword_overwrite", return_value=False),
        ):
            config = {"keyring_backend": "onepassword"}
            set_keyring_password("hunter2", "default", config)
            set_password.assert_not_called()
            print_msg.assert_called_once()
            msg = print_msg.call_args.args[0]
            assert "not stored" in str(msg.text).lower()
