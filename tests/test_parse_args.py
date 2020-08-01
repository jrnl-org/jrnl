from jrnl.cli import parse_args

import pytest
import shlex


def cli_as_dict(str):
    cli = shlex.split(str)
    args = parse_args(cli)
    return vars(args)


def expected_args(**kwargs):
    default_args = {
        "contains": None,
        "debug": False,
        "decrypt": False,
        "delete": False,
        "edit": False,
        "encrypt": False,
        "end_date": None,
        "excluded": [],
        "export": False,
        "input": False,
        "limit": None,
        "on_date": None,
        "output": False,
        "preconfig_cmd": None,
        "postconfig_cmd": None,
        "short": False,
        "starred": False,
        "start_date": None,
        "strict": False,
        "tags": False,
        "text": [],
    }
    return {**default_args, **kwargs}


def test_empty():
    assert cli_as_dict("") == expected_args()


def test_contains_alone():
    assert cli_as_dict("-contains whatever") == expected_args(contains="whatever")


def test_debug_alone():
    assert cli_as_dict("--debug") == expected_args(debug=True)


def test_delete_alone():
    assert cli_as_dict("--delete") == expected_args(delete=True)


def test_diagnostic_alone():
    from jrnl.commands import preconfig_diagnostic

    assert cli_as_dict("--diagnostic") == expected_args(
        preconfig_cmd=preconfig_diagnostic
    )


def test_edit_alone():
    assert cli_as_dict("--edit") == expected_args(edit=True)


def test_encrypt_alone():
    assert cli_as_dict("--encrypt 'test.txt'") == expected_args(encrypt="test.txt")


def test_end_date_alone():
    expected = expected_args(end_date="2020-01-01")
    assert expected == cli_as_dict("-until 2020-01-01")
    assert expected == cli_as_dict("-to 2020-01-01")


def test_not_alone():
    assert cli_as_dict("-not test") == expected_args(excluded=["test"])


def test_not_multiple_alone():
    assert cli_as_dict("-not one -not two") == expected_args(excluded=["one", "two"])
    assert cli_as_dict("-not one -not two -not three") == expected_args(
        excluded=["one", "two", "three"]
    )


@pytest.mark.parametrize(
    "cli",
    ["two -not one -not three", "-not one two -not three", "-not one -not three two",],
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


def test_input_flag_alone():
    assert cli_as_dict("-i test.txt") == expected_args(input="test.txt")
    assert cli_as_dict("-i 'lorem ipsum.txt'") == expected_args(input="lorem ipsum.txt")


def test_output_flag_alone():
    assert cli_as_dict("-o test.txt") == expected_args(output="test.txt")
    assert cli_as_dict("-o 'lorem ipsum.txt'") == expected_args(
        output="lorem ipsum.txt"
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
