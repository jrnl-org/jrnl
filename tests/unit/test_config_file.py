import pytest
import os

from jrnl.install import find_alt_config


def test_find_alt_config(request):
    work_config_path = os.path.join(
        request.fspath.dirname, "..", "data", "configs", "basic_onefile.yaml"
    )
    found_alt_config = find_alt_config(work_config_path)
    assert found_alt_config == work_config_path


def test_find_alt_config_not_exist(request):
    bad_config_path = os.path.join(
        request.fspath.dirname, "..", "data", "configs", "not-existing-config.yaml"
    )
    with pytest.raises(SystemExit) as ex:
        found_alt_config = find_alt_config(bad_config_path)
        assert found_alt_config is not None
    assert isinstance(ex.value, SystemExit)
