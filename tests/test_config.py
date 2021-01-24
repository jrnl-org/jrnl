import pytest

import mock

import yaml
from jrnl.args import parse_args
from jrnl.jrnl import run
from jrnl import install


@pytest.fixture()
def minimal_config():
    with open("features/data/configs/editor.yaml", "r") as cfg_file:
        cfg = yaml.load(cfg_file.read(), Loader=yaml.FullLoader)
    yield cfg


@pytest.fixture()
def expected_override(minimal_config):
    exp_out_cfg = minimal_config.copy()
    exp_out_cfg["editor"] = "nano"
    exp_out_cfg["journal"] = "features/journals/simple.journal"
    yield exp_out_cfg


from jrnl import jrnl


@mock.patch("sys.stdin.isatty")
@mock.patch.object(install, "load_or_install_jrnl")
@mock.patch("subprocess.call")
def test_override_configured_editor(
    mock_subprocess_call,
    mock_load_or_install,
    mock_isatty,
    minimal_config,
    expected_override,
    capsys,
):
    mock_load_or_install.return_value = minimal_config
    mock_isatty.return_value = True

    cli_args = ["--config-override", '{"editor": "nano"}']
    parser = parse_args(cli_args)
    assert parser.config_override.__len__() == 1
    assert "editor" in parser.config_override.keys() 
    def mock_editor_launch(editor):
        print("%s launched! Success!" % editor)

    with mock.patch.object(
        jrnl,
        "_write_in_editor",
        side_effect=mock_editor_launch(parser.config_override["editor"]),
        return_value="note_contents",
    ) as mock_write_in_editor:
        run(parser)
    mock_write_in_editor.assert_called_once_with(expected_override)

@pytest.fixture()
def expected_color_override(minimal_config): 
    exp_out_cfg = minimal_config.copy() 
    exp_out_cfg["colors"] = {"body": "blue"}
    exp_out_cfg["journal"] = "features/journals/simple.journal"
    yield exp_out_cfg

# @mock.patch.object(install,'load_or_install_jrnl')
# @mock.patch('subprocess.call')
# def test_override_configured_colors(mock_load_or_install, mock_subprocess_call, minimal_config, expected_color_override, capsys): 
#     mock_load_or_install.return_value = minimal_config
    
#     cli_args=["--config-override",'{"colors.body": "blue"}']
#     parser = parse_args(cli_args)
#     assert "colors.body" in parser.config_override.keys() 
#     run(parser)

    
