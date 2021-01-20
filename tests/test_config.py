import pytest 
import pytest_mock 
import mock

import yaml
from jrnl.args import parse_args
from jrnl.jrnl import run 
from jrnl import install 

@pytest.fixture()
def minimal_config():
    with open('features/data/configs/editor.yaml','r') as cfg_file:
        yield yaml.load(cfg_file.read())

from jrnl import jrnl
@mock.patch.object(jrnl,'write_mode')
@mock.patch.object(install,'load_or_install_jrnl')
def test_override_configured_editor(mock_load_or_install, mock_write_mode, minimal_config): 
    mock_load_or_install.return_value = minimal_config
    cli_args = ['--override','{\"editor\": \"nano\"}' ]
    parser = parse_args(cli_args)
    assert parser.config_override.__len__() == 1
    with mock.patch('subprocess.call'):
        res = run(parser)
    assert res==None 