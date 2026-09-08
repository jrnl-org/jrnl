# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import sys
from unittest import mock

import pytest

from jrnl import config
from jrnl import install


@pytest.mark.parametrize(
    "eof_at", [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
)
def test_install_uses_defaults_on_eof(tmp_path, monkeypatch, eof_at):
    config_path = tmp_path / "jrnl.yaml"
    default_journal_path = tmp_path / "default" / "journal.txt"
    monkeypatch.chdir(tmp_path)
    for module in (config, install):
        monkeypatch.setattr(module, "get_config_path", lambda: str(config_path))
        monkeypatch.setattr(
            module, "get_default_journal_path", lambda: str(default_journal_path)
        )

    responses = ["custom/journal.txt", "y", "n"]
    for index in eof_at:
        responses[index] = EOFError()
    with mock.patch("builtins.input", side_effect=responses):
        installed_config = install.install()

    expected_journal_path = (
        default_journal_path if 0 in eof_at else tmp_path / "custom" / "journal.txt"
    )
    assert installed_config["journals"]["default"]["journal"] == str(
        expected_journal_path
    )
    assert expected_journal_path.parent.is_dir()
    assert installed_config["encrypt"] is (1 not in eof_at)
    assert installed_config["colors"] == (
        config.get_default_colors()
        if 2 in eof_at
        else config.get_default_config()["colors"]
    )
    assert config.load_config(str(config_path)) == installed_config


@pytest.mark.filterwarnings(
    "ignore:.*imp module is deprecated.*"
)  # ansiwrap spits out an unrelated warning
def test_initialize_autocomplete_runs_without_readline():
    with mock.patch.dict(sys.modules, {"readline": None}):
        install._initialize_autocomplete()  # should not throw exception
