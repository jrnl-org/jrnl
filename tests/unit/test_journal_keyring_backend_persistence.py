# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from unittest.mock import MagicMock

from jrnl.journals.Journal import Journal


def _journal_with_stub_encryption_method(mutate_config=None):
    journal = Journal("test", encrypt=False)

    def encrypt(text):
        if mutate_config:
            mutate_config(journal.config)
        return text.encode()

    journal.encryption_method = MagicMock()
    journal.encryption_method.encrypt.side_effect = encrypt
    return journal


class TestKeyringBackendPendingConfigUpdate:
    def test_queues_update_when_encrypt_sets_keyring_backend(self):
        journal = _journal_with_stub_encryption_method(
            mutate_config=lambda config: config.__setitem__(
                "keyring_backend", "onepassword"
            )
        )

        journal._encrypt("some text")

        assert journal.config["keyring_backend"] == "onepassword"
        assert journal._pending_config_updates == {"keyring_backend": "onepassword"}

    def test_does_not_queue_update_when_keyring_backend_unchanged(self):
        journal = _journal_with_stub_encryption_method()

        journal._encrypt("some text")

        assert "keyring_backend" not in journal._pending_config_updates

    def test_does_not_queue_update_when_keyring_backend_already_set(self):
        journal = _journal_with_stub_encryption_method()
        journal.config["keyring_backend"] = "onepassword"

        journal._encrypt("some text")

        assert "keyring_backend" not in journal._pending_config_updates
