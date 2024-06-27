# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import shlex

import pytest

from jrnl.args import parse_args
from jrnl.config import make_yaml_valid_dict


def cli_as_dict(str):
    cli = shlex.split(str)
    args = parse_args(cli)
    return vars(args)


def expected_args(**kwargs):
    default_args = {
        "contains": None,
        "debug": False,
        "delete": False,
        "change_time": None,
        "edit": False,
        "end_date": None,
        "exclude_starred": False,
        "exclude_tagged": False,
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
        "tagged": False,
        "tags": False,
        "template": None,
        "text": [],
        "config_override": [],
        "config_file_path": "",
    }
    return {**default_args, **kwargs}


def test_empty():
    assert cli_as_dict("") == expected_args()


def test_contains_alone():
    assert cli_as_dict("-contains whatever") == expected_args(contains=["whatever"])


def test_debug_alone():
    assert cli_as_dict("--debug") == expected_args(debug=True)


def test_delete_alone():
    assert cli_as_dict("--delete") == expected_args(delete=True)


def test_change_time_alone():
    assert cli_as_dict("--change-time") == expected_args(change_time="now")
    assert cli_as_dict("--change-time yesterday") == expected_args(
        change_time="yesterday"
    )


def test_diagnostic_alone():
    from jrnl.commands import preconfig_diagnostic

    assert cli_as_dict("--diagnostic") == expected_args(
        preconfig_cmd=preconfig_diagnostic
    )


def test_edit_alone():
    assert cli_as_dict("--edit") == expected_args(edit=True)


def test_encrypt_alone():
    from jrnl.commands import postconfig_encrypt

    assert cli_as_dict("--encrypt") == expected_args(postconfig_cmd=postconfig_encrypt)


def test_decrypt_alone():
    from jrnl.commands import postconfig_decrypt

    assert cli_as_dict("--decrypt") == expected_args(postconfig_cmd=postconfig_decrypt)


def test_end_date_alone():
    expected = expected_args(end_date="2020-01-01")
    assert expected == cli_as_dict("-until 2020-01-01")
    assert expected == cli_as_dict("-to 2020-01-01")


def test_not_empty():
    with pytest.raises(SystemExit) as wrapped_e:
        cli_as_dict("-not")
    assert wrapped_e.value.code == 2


def test_not_alone():
    assert cli_as_dict("-not test") == expected_args(excluded=["test"])


def test_not_multiple_alone():
    assert cli_as_dict("-not one -not two") == expected_args(excluded=["one", "two"])
    assert cli_as_dict("-not one -not two -not three") == expected_args(
        excluded=["one", "two", "three"]
    )


@pytest.mark.parametrize(
    "cli",
    [
        "two -not one -not three",
        "-not one two -not three",
        "-not one -not three two",
    ],
)
def test_not_mixed(cli):
    result = expected_args(excluded=["one", "three"], text=["two"])
    assert cli_as_dict(cli) == result


def test_not_interspersed():
    result = expected_args(excluded=["one", "three"], text=["two", "two", "two"])
    assert cli_as_dict("two -not one two -not three two") == result


def test_export_alone():
    assert cli_as_dict("--export json") == expected_args(export="json")


def test_import_alone():
    from jrnl.commands import postconfig_import

    assert cli_as_dict("--import") == expected_args(postconfig_cmd=postconfig_import)


def test_file_flag_alone():
    assert cli_as_dict("--file test.txt") == expected_args(filename="test.txt")
    assert cli_as_dict("--file 'lorem ipsum.txt'") == expected_args(
        filename="lorem ipsum.txt"
    )


def test_limit_alone():
    assert cli_as_dict("-n 5") == expected_args(limit=5)
    assert cli_as_dict("-n 999") == expected_args(limit=999)


def test_limit_shorthand_alone():
    assert cli_as_dict("-5") == expected_args(limit=5)
    assert cli_as_dict("-999") == expected_args(limit=999)


def test_list_alone():
    from jrnl.commands import postconfig_list

    assert cli_as_dict("--ls") == expected_args(postconfig_cmd=postconfig_list)


def test_on_date_alone():
    assert cli_as_dict("-on 'saturday'") == expected_args(on_date="saturday")


def test_month_alone():
    assert cli_as_dict("-month 1") == expected_args(month="1")
    assert cli_as_dict("-month 01") == expected_args(month="01")
    assert cli_as_dict("-month January") == expected_args(month="January")
    assert cli_as_dict("-month Jan") == expected_args(month="Jan")


def test_day_alone():
    assert cli_as_dict("-day 1") == expected_args(day="1")
    assert cli_as_dict("-day 01") == expected_args(day="01")


def test_year_alone():
    assert cli_as_dict("-year 2021") == expected_args(year="2021")
    assert cli_as_dict("-year 21") == expected_args(year="21")


def test_today_in_history_alone():
    assert cli_as_dict("-today-in-history") == expected_args(today_in_history=True)


def test_short_alone():
    assert cli_as_dict("--short") == expected_args(short=True)


def test_starred_alone():
    assert cli_as_dict("-starred") == expected_args(starred=True)


def test_start_date_alone():
    assert cli_as_dict("-from 2020-01-01") == expected_args(start_date="2020-01-01")
    assert cli_as_dict("-from 'January 1st'") == expected_args(start_date="January 1st")


def test_and_alone():
    assert cli_as_dict("-and") == expected_args(strict=True)


def test_tags_alone():
    assert cli_as_dict("--tags") == expected_args(tags=True)


def test_text_alone():
    assert cli_as_dict("lorem ipsum dolor sit amet") == expected_args(
        text=["lorem", "ipsum", "dolor", "sit", "amet"]
    )


def test_version_alone():
    from jrnl.commands import preconfig_version

    assert cli_as_dict("--version") == expected_args(preconfig_cmd=preconfig_version)


def test_editor_override():
    parsed_args = cli_as_dict('--config-override editor "nano"')
    assert parsed_args == expected_args(config_override=[["editor", "nano"]])


def test_color_override():
    assert cli_as_dict("--config-override colors.body blue") == expected_args(
        config_override=[["colors.body", "blue"]]
    )


def test_multiple_overrides():
    parsed_args = cli_as_dict(
        "--config-override colors.title green "
        '--config-override editor "nano" '
        '--config-override journal.scratchpad "/tmp/scratchpad"'
    )
    assert parsed_args == expected_args(
        config_override=[
            ["colors.title", "green"],
            ["editor", "nano"],
            ["journal.scratchpad", "/tmp/scratchpad"],
        ]
    )


# @see https://github.com/jrnl-org/jrnl/issues/520
@pytest.mark.parametrize(
    "cli",
    [
        "-and second @oldtag @newtag",
        "second @oldtag @newtag -and",
        "second -and @oldtag @newtag",
        "second @oldtag -and @newtag",
    ],
)
def test_and_ordering(cli):
    result = expected_args(strict=True, text=["second", "@oldtag", "@newtag"])
    assert cli_as_dict(cli) == result


# @see https://github.com/jrnl-org/jrnl/issues/520
@pytest.mark.parametrize(
    "cli",
    [
        "--edit second @oldtag @newtag",
        "second @oldtag @newtag --edit",
        "second --edit @oldtag @newtag",
        "second @oldtag --edit @newtag",
    ],
)
def test_edit_ordering(cli):
    result = expected_args(edit=True, text=["second", "@oldtag", "@newtag"])
    assert cli_as_dict(cli) == result


class TestDeserialization:
    @pytest.mark.parametrize(
        "input_str",
        [
            ["editor", "nano"],
            ["colors.title", "blue"],
            ["default", "/tmp/egg.txt"],
        ],
    )
    def test_deserialize_multiword_strings(self, input_str):
        runtime_config = make_yaml_valid_dict(input_str)
        assert runtime_config.__class__ == dict
        assert input_str[0] in runtime_config
        assert runtime_config[input_str[0]] == input_str[1]

    def test_deserialize_multiple_datatypes(self):
        cfg = make_yaml_valid_dict(["linewrap", "23"])
        assert cfg["linewrap"] == 23

        cfg = make_yaml_valid_dict(["encrypt", "false"])
        assert cfg["encrypt"] is False

        cfg = make_yaml_valid_dict(["editor", "vi -c startinsert"])
        assert cfg["editor"] == "vi -c startinsert"

        cfg = make_yaml_valid_dict(["highlight", "true"])
        assert cfg["highlight"] is True
