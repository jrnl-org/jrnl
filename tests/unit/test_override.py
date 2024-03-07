# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from argparse import Namespace

import pytest

from jrnl.override import _convert_dots_to_list
from jrnl.override import _get_config_node
from jrnl.override import _get_key_and_value_from_pair
from jrnl.override import _recursively_apply
from jrnl.override import apply_overrides


@pytest.fixture()
def minimal_config():
    cfg = {
        "colors": {"body": "red", "date": "green"},
        "default": "/tmp/journal.jrnl",
        "editor": "vim",
        "journals": {"default": "/tmp/journals/journal.jrnl"},
    }
    return cfg


def expected_args(overrides):
    default_args = {
        "contains": None,
        "debug": False,
        "delete": False,
        "edit": False,
        "end_date": None,
        "today_in_history": False,
        "month": None,
        "day": None,
        "year": None,
        "excluded": [],
        "export": False,
        "filename": None,
        "limit": None,
        "on_date": None,
        "preconfig_cmd": None,
        "postconfig_cmd": None,
        "short": False,
        "starred": False,
        "start_date": None,
        "strict": False,
        "tags": False,
        "text": [],
        "config_override": [],
    }
    return Namespace(**{**default_args, **overrides})


def test_apply_override(minimal_config):
    overrides = {"config_override": [["editor", "nano"]]}
    apply_overrides(expected_args(overrides), minimal_config)
    assert minimal_config["editor"] == "nano"


def test_override_dot_notation(minimal_config):
    overrides = {"config_override": [["colors.body", "blue"]]}
    apply_overrides(expected_args(overrides), minimal_config)
    assert minimal_config["colors"] == {"body": "blue", "date": "green"}


def test_multiple_overrides(minimal_config):
    overrides = {
        "config_override": [
            ["colors.title", "magenta"],
            ["editor", "nano"],
            ["journals.burner", "/tmp/journals/burner.jrnl"],
        ]
    }

    actual = apply_overrides(expected_args(overrides), minimal_config)
    assert actual["editor"] == "nano"
    assert actual["colors"]["title"] == "magenta"
    assert "burner" in actual["journals"]
    assert actual["journals"]["burner"] == "/tmp/journals/burner.jrnl"


def test_recursively_apply():
    cfg = {"colors": {"body": "red", "title": "green"}}
    cfg = _recursively_apply(cfg, ["colors", "body"], "blue")
    assert cfg["colors"]["body"] == "blue"


def test_get_config_node(minimal_config):
    assert len(minimal_config.keys()) == 4
    assert _get_config_node(minimal_config, "editor") == "vim"
    assert _get_config_node(minimal_config, "display_format") is None


def test_get_kv_from_pair():
    pair = {"ab.cde": "fgh"}
    k, v = _get_key_and_value_from_pair(pair)
    assert k == "ab.cde"
    assert v == "fgh"


class TestDotNotationToList:
    def test_unpack_dots_to_list(self):
        keys = "a.b.c.d.e.f"
        keys_list = _convert_dots_to_list(keys)
        assert len(keys_list) == 6

    def test_sequential_delimiters(self):
        k = "g.r..h.v"
        k_l = _convert_dots_to_list(k)
        assert len(k_l) == 4