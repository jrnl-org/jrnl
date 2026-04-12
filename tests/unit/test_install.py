# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import sys
from unittest import mock

import pytest


@pytest.mark.filterwarnings(
    "ignore:.*imp module is deprecated.*"
)  # ansiwrap spits out an unrelated warning
def test_initialize_autocomplete_runs_without_readline():
    from jrnl import install

    with mock.patch.dict(sys.modules, {"readline": None}):
        install._initialize_autocomplete()  # should not throw exception


def test_upgrade_config_fills_missing_color_subkeys(tmp_path):
    """Regression test for https://github.com/jrnl-org/jrnl/issues/2021.

    If a user's config has a 'colors' dict but is missing sub-keys
    (e.g. 'tags'), upgrade_config should fill them in from defaults.
    """
    from jrnl.config import get_default_config
    from jrnl.install import upgrade_config

    config = get_default_config()
    # Simulate a config that has colors but is missing the 'tags' key
    del config["colors"]["tags"]
    assert "tags" not in config["colors"]

    config_path = tmp_path / "jrnl.yaml"
    config_path.write_text("")

    upgrade_config(config, alt_config_path=str(config_path))

    assert "tags" in config["colors"]
    assert config["colors"]["tags"] == "none"
