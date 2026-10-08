# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import sys
from unittest import mock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest


@pytest.mark.filterwarnings(
    "ignore:.*imp module is deprecated.*"
)  # ansiwrap spits out an unrelated warning
def test_initialize_autocomplete_runs_without_readline():
    from jrnl import install

    with mock.patch.dict(sys.modules, {"readline": None}):
        install._initialize_autocomplete()  # should not throw exception


def test_install_uses_defaults_when_stdin_is_eof(tmp_path):
    """install() must not raise EOFError when stdin is at EOF (e.g. jrnl < /dev/null).
    Instead every interactive prompt should fall back to its built-in default."""
    from jrnl import install

    config_path = str(tmp_path / "jrnl.yaml")
    journal_path = str(tmp_path / "journal.txt")

    mock_console = MagicMock()
    mock_console.input.side_effect = EOFError

    with (
        patch("jrnl.output._get_console", return_value=mock_console),
        patch("jrnl.install.get_config_path", return_value=config_path),
        patch("jrnl.config.get_config_path", return_value=config_path),
        patch("jrnl.install.get_default_journal_path", return_value=journal_path),
        patch("jrnl.config.get_default_journal_path", return_value=journal_path),
    ):
        config = install.install()

    assert config["journals"]["default"]["journal"] == journal_path
    assert config["encrypt"] is False
