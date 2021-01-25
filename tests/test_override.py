import pytest

from jrnl.override import apply_overrides, _recursively_apply, _get_config_node


@pytest.fixture()
def minimal_config():
    cfg = {
        "colors": {"body": "red", "date": "green"},
        "default": "/tmp/journal.jrnl",
        "editor": "vim",
    }
    yield cfg


def test_apply_override(minimal_config):
    config = minimal_config.copy()
    overrides = {"editor": "nano"}
    config = apply_overrides(overrides, config)
    assert config["editor"] == "nano"


def test_override_dot_notation(minimal_config):
    cfg = minimal_config.copy()
    overrides = {"colors.body": "blue"}
    cfg = apply_overrides(overrides=overrides, base_config=cfg)
    assert cfg["colors"] == {"body": "blue", "date": "green"}


def test_recursively_apply():
    cfg = {"colors": {"body": "red", "title": "green"}}
    cfg = _recursively_apply(cfg, ["colors", "body"], "blue")
    assert cfg["colors"]["body"] == "blue"


def test_get_config_node(minimal_config):
    assert len(minimal_config.keys()) == 3
    assert _get_config_node(minimal_config, "editor") == "vim"
    assert _get_config_node(minimal_config, "display_format") == None
