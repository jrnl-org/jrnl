import pytest

import mock

from jrnl.args import parse_args
from jrnl.jrnl import run, search_mode
from jrnl import install
from jrnl.override import apply_overrides
@pytest.fixture()
def minimal_config(): 
    cfg = { 
        "colors":{ 
            "body":"red",
            "date":"green"
        },
        "default":"/tmp/journal.jrnl",
        "editor":"vim"
    }
    yield cfg 

def test_apply_override(minimal_config): 
    config = minimal_config.copy()
    overrides = {
        'editor':'nano'
    }
    config = apply_overrides(overrides, config)
    assert config['editor']=='nano'