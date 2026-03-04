# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from jrnl.config import get_default_config
from jrnl.config import save_config


def test_save_config_writes_git_comment(tmp_path):
    config_path = tmp_path / "jrnl.yaml"
    save_config(get_default_config(), str(config_path))
    content = config_path.read_text()
    assert "# git: false" in content
