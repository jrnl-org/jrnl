from unittest import mock
import pytest
import sys


@pytest.mark.filterwarnings(
    "ignore:.*imp module is deprecated.*"
)  # ansiwrap spits out an unrelated warning
def test_initialize_autocomplete_runs_without_readline():
    from jrnl import install

    with mock.patch.dict(sys.modules, {"readline": None}):
        install._initialize_autocomplete()  # should not throw exception
