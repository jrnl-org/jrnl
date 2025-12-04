# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import pytest
from colorama import Fore
from colorama import Style

from jrnl.color import colorize
from jrnl.color import get_tag_color


@pytest.fixture()
def data_fixture():
    string = "Zwei peanuts walked into a bar"
    yield string


def test_colorize(data_fixture):
    string = data_fixture
    colorized_string = colorize(string, "BLUE", True)

    assert colorized_string == Style.BRIGHT + Fore.BLUE + string + Style.RESET_ALL


@pytest.fixture()
def config_with_tag_colors():
    return {
        "tag_colors": {
            "@high": "red",
            "@low": "green",
            "#urgent": "magenta",
        },
        "colors": {"tags": "yellow"},
    }


def test_get_tag_color_with_specific_color(config_with_tag_colors):
    """Test that specific tag colors are returned when configured"""
    config = config_with_tag_colors

    assert get_tag_color("@high", config) == "red"
    assert get_tag_color("#urgent", config) == "magenta"
    assert get_tag_color("@low", config) == "green"


def test_get_tag_color_case_insensitive(config_with_tag_colors):
    """Test that tag color lookup is case insensitive"""
    config = config_with_tag_colors

    assert get_tag_color("@HIGH", config) == "red"
    assert get_tag_color("#URGENT", config) == "magenta"


def test_get_tag_color_fallback_to_default(config_with_tag_colors):
    """Test that unspecified tags fall back to the default tags color"""
    config = config_with_tag_colors

    assert get_tag_color("@unknown", config) == "yellow"
    assert get_tag_color("#work", config) == "yellow"


def test_get_tag_color_no_tag_colors_config():
    """Test that it falls back to default when no tag_colors section exists"""
    config = {"colors": {"tags": "blue"}}

    assert get_tag_color("@any", config) == "blue"
    assert get_tag_color("#any", config) == "blue"


def test_get_tag_color_missing_colors_config():
    """Test that it falls back to 'none' when no colors section exists"""
    config = {}

    assert get_tag_color("@any", config) == "none"
    assert get_tag_color("#any", config) == "none"


def test_get_tag_color_empty_tag_colors():
    """Test with empty tag_colors section"""
    config = {"tag_colors": {}, "colors": {"tags": "cyan"}}

    assert get_tag_color("@any", config) == "cyan"
