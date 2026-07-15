# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import argparse
from unittest.mock import MagicMock
from unittest.mock import patch

from jrnl.commands import postconfig_encrypt


def make_journal_stub(pending_updates=None):
    journal = MagicMock()
    journal.config = {"encrypt": False, "journal": "/tmp/journal.txt"}
    journal.can_be_encrypted = True
    journal._pending_config_updates = {}
    journal.name = "default"

    def write(filename, force_new_password=False):
        # Simulate a config change accumulated during the password prompt
        # (e.g. the user opted into a non-default keyring backend).
        journal._pending_config_updates.update(pending_updates or {})

    journal.write.side_effect = write
    return journal


class TestPostconfigEncryptPersistsPendingConfigUpdates:
    def test_persists_keyring_backend_choice_made_during_encrypt(self):
        journal = make_journal_stub(pending_updates={"keyring_backend": "onepassword"})
        args = argparse.Namespace(journal_name="default", filename=None)
        original_config = {"journals": {"default": "/tmp/journal.txt"}}
        config = {"journals": {"default": "/tmp/journal.txt"}}

        with (
            patch("jrnl.journals.open_journal", return_value=journal),
            patch("jrnl.config.update_config") as update_config,
            patch("jrnl.install.save_config") as save_config,
            patch("jrnl.output.print_msg"),
        ):
            postconfig_encrypt(
                args=args, config=config, original_config=original_config
            )

        update_config.assert_called_once_with(
            original_config,
            {"encrypt": True, "keyring_backend": "onepassword"},
            "default",
            force_local=True,
        )
        save_config.assert_called_once_with(original_config)

    def test_persists_just_encrypt_when_no_pending_updates(self):
        journal = make_journal_stub()
        args = argparse.Namespace(journal_name="default", filename=None)
        original_config = {"journals": {"default": "/tmp/journal.txt"}}
        config = {"journals": {"default": "/tmp/journal.txt"}}

        with (
            patch("jrnl.journals.open_journal", return_value=journal),
            patch("jrnl.config.update_config") as update_config,
            patch("jrnl.install.save_config"),
            patch("jrnl.output.print_msg"),
        ):
            postconfig_encrypt(
                args=args, config=config, original_config=original_config
            )

        update_config.assert_called_once_with(
            original_config, {"encrypt": True}, "default", force_local=True
        )

    def test_does_not_persist_when_writing_to_a_separate_file(self):
        journal = make_journal_stub(pending_updates={"keyring_backend": "onepassword"})
        args = argparse.Namespace(journal_name="default", filename="out.txt")
        original_config = {"journals": {"default": "/tmp/journal.txt"}}
        config = {"journals": {"default": "/tmp/journal.txt"}}

        with (
            patch("jrnl.journals.open_journal", return_value=journal),
            patch("jrnl.config.update_config") as update_config,
            patch("jrnl.install.save_config") as save_config,
            patch("jrnl.output.print_msg"),
        ):
            postconfig_encrypt(
                args=args, config=config, original_config=original_config
            )

        update_config.assert_not_called()
        save_config.assert_not_called()
