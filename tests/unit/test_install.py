# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import errno
import sys
from unittest import mock

import pytest

from jrnl import __version__
from jrnl import install


@pytest.mark.parametrize("error_code", [errno.EACCES, errno.EROFS])
def test_load_config_with_read_only_defaults(tmp_path, monkeypatch, capsys, error_code):
    path = tmp_path / "jrnl.yaml"
    original = f"version: {__version__}\njournals:\n  default: journal.txt\n"
    path.write_text(original, encoding="utf-8")

    def fail_to_save(_config, config_path):
        assert config_path == str(path)
        raise OSError(error_code, "Cannot write configuration", config_path)

    monkeypatch.setattr(install, "save_config", fail_to_save)

    config = install.load_or_install_jrnl(str(path))

    assert config["default_hour"] == 9
    assert path.read_text(encoding="utf-8") == original
    assert "Using updated configuration for this run" in capsys.readouterr().err


@pytest.mark.filterwarnings(
    "ignore:.*imp module is deprecated.*"
)  # ansiwrap spits out an unrelated warning
def test_initialize_autocomplete_runs_without_readline():
    with mock.patch.dict(sys.modules, {"readline": None}):
        install._initialize_autocomplete()  # should not throw exception
