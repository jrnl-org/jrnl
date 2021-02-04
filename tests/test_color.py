import pytest

from jrnl.color import colorize
from colorama import Fore, Style


@pytest.fixture()
def data_fixture():
    string = "Zwei peanuts walked into a bar"
    yield string


def test_colorize(data_fixture):
    string = data_fixture
    colorized_string = colorize(string, "BLUE", True)

    assert colorized_string == Style.BRIGHT + Fore.BLUE + string + Style.RESET_ALL


def test_colorize_none(data_fixture):
    string = data_fixture
    colorized_string = colorize(string, None, False)
    assert colorized_string == string
