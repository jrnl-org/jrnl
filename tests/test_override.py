import pytest

from jrnl.override import apply_overrides, recursively_apply
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

def test_override_dot_notation(minimal_config): 
    cfg = minimal_config.copy() 
    overrides = { 
        "colors.body": "blue"
    }
    cfg = apply_overrides(overrides=overrides, base_config=cfg)
    assert cfg["colors"] == {"body": "blue", "date":"green"}

def test_recursive_override(minimal_config): 
    
    cfg = { 
        "colors": { 
            "body": "red",
            "title": "green"
        }
    }
    cfg = recursively_apply(cfg,["colors",'body'],"blue")
    assert cfg["colors"]["body"] == "blue"