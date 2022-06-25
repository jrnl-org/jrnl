# Copyright (C) 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import json
import os
import re
from xml.etree import ElementTree

from pytest_bdd import then
from pytest_bdd.parsers import parse
from ruamel.yaml import YAML

from jrnl.config import scope_config

from .helpers import assert_equal_tags_ignoring_order
from .helpers import does_directory_contain_files
from .helpers import parse_should_or_should_not
from .helpers import get_nested_val


@then("we should get no error")
def should_get_no_error(cli_run):
    assert cli_run["status"] == 0, cli_run["status"]


@then(parse('the output should match "{regex}"'))
def output_should_match(regex, cli_run):
    out = cli_run["stdout"]
    matches = re.findall(regex, out)
    assert matches, f"\nRegex didn't match:\n{regex}\n{str(out)}\n{str(matches)}"


@then(parse("the output {should_or_should_not} contain\n{expected_output}"))
@then(parse('the output {should_or_should_not} contain "{expected_output}"'))
@then(
    parse(
        "the {which_output_stream} output {should_or_should_not} contain\n{expected_output}"
    )
)
@then(
    parse(
        'the {which_output_stream} output {should_or_should_not} contain "{expected_output}"'
    )
)
def output_should_contain(
    expected_output, which_output_stream, cli_run, should_or_should_not
):
    we_should = parse_should_or_should_not(should_or_should_not)

    output_str = f"\nEXPECTED:\n{expected_output}\n\nACTUAL STDOUT:\n{cli_run['stdout']}\n\nACTUAL STDERR:\n{cli_run['stderr']}"
    assert expected_output
    if which_output_stream is None:
        assert ((expected_output in cli_run["stdout"]) == we_should) or (
            (expected_output in cli_run["stderr"]) == we_should
        ), output_str

    elif which_output_stream == "standard":
        assert (expected_output in cli_run["stdout"]) == we_should, output_str

    elif which_output_stream == "error":
        assert (expected_output in cli_run["stderr"]) == we_should, output_str

    else:
        assert (
            expected_output in cli_run[which_output_stream]
        ) == we_should, output_str


@then(parse("the output should not contain\n{expected_output}"))
@then(parse('the output should not contain "{expected_output}"'))
def output_should_not_contain(expected_output, cli_run):
    assert expected_output not in cli_run["stdout"]


@then(parse("the output should be\n{expected_output}"))
@then(parse('the output should be "{expected_output}"'))
def output_should_be(expected_output, cli_run):
    actual = cli_run["stdout"].strip()
    expected = expected_output.strip()
    assert expected == actual


@then("the output should be empty")
def output_should_be_empty(cli_run):
    actual = cli_run["stdout"].strip()
    assert actual == ""


@then(parse('the output should contain the date "{date}"'))
def output_should_contain_date(date, cli_run):
    assert date and date in cli_run["stdout"]


@then("the output should contain pyproject.toml version")
def output_should_contain_version(cli_run, toml_version):
    out = cli_run["stdout"]
    assert toml_version in out, toml_version


@then("the version in the config file should be up-to-date")
def config_file_version(config_on_disk, toml_version):
    config_version = config_on_disk["version"]
    assert config_version == toml_version


@then(parse("the output should be {width:d} columns wide"))
def output_should_be_columns_wide(cli_run, width):
    out = cli_run["stdout"]
    out_lines = out.splitlines()
    for line in out_lines:
        assert len(line) <= width


@then(
    parse(
        'the default journal "{journal_file}" should be in the "{journal_dir}" directory'
    )
)
def default_journal_location(journal_file, journal_dir, config_on_disk, temp_dir):
    default_journal_path = config_on_disk["journals"]["default"]
    expected_journal_path = (
        os.path.join(temp_dir.name, journal_file)
        if journal_dir == "."
        else os.path.join(temp_dir.name, journal_dir, journal_file)
    )
    # Use os.path.samefile here because both paths might not be fully expanded.
    assert os.path.samefile(default_journal_path, expected_journal_path)


@then(
    parse(
        'the config for journal "{journal_name}" {should_or_should_not} contain "{some_yaml}"'
    )
)
@then(
    parse(
        'the config for journal "{journal_name}" {should_or_should_not} contain\n{some_yaml}'
    )
)
@then(parse('the config {should_or_should_not} contain "{some_yaml}"'))
@then(parse("the config {should_or_should_not} contain\n{some_yaml}"))
def config_var_on_disk(config_on_disk, journal_name, should_or_should_not, some_yaml):
    we_should = parse_should_or_should_not(should_or_should_not)

    actual = config_on_disk
    if journal_name:
        actual = actual["journals"][journal_name]

    expected = YAML(typ="safe").load(some_yaml)

    actual_slice = actual
    if type(actual) is dict:
        # `expected` objects formatted in yaml only compare one level deep
        actual_slice = {key: actual.get(key, None) for key in expected.keys()}

    assert (expected == actual_slice) == we_should


@then(
    parse(
        'the config in memory for journal "{journal_name}" {should_or_should_not} contain "{some_yaml}"'
    )
)
@then(
    parse(
        'the config in memory for journal "{journal_name}" {should_or_should_not} contain\n{some_yaml}'
    )
)
@then(parse('the config in memory {should_or_should_not} contain "{some_yaml}"'))
@then(parse("the config in memory {should_or_should_not} contain\n{some_yaml}"))
def config_var_in_memory(
    config_in_memory, journal_name, should_or_should_not, some_yaml
):
    we_should = parse_should_or_should_not(should_or_should_not)

    actual = config_in_memory["overrides"]
    if journal_name:
        actual = actual["journals"][journal_name]

    expected = YAML(typ="safe").load(some_yaml)

    actual_slice = actual
    if type(actual) is dict:
        # `expected` objects formatted in yaml only compare one level deep
        actual_slice = {key: get_nested_val(actual, key) for key in expected.keys()}

    assert (expected == actual_slice) == we_should


@then("we should be prompted for a password")
def password_was_called(cli_run):
    assert cli_run["mocks"]["user_input"].called


@then("we should not be prompted for a password")
def password_was_not_called(cli_run):
    assert not cli_run["mocks"]["user_input"].called


@then(parse("the cache directory should contain the files\n{file_list}"))
def assert_dir_contains_files(file_list, cache_dir):
    assert does_directory_contain_files(file_list, cache_dir["path"])


@then(parse("the journal directory should contain\n{file_list}"))
def journal_directory_should_contain(config_on_disk, file_list):
    scoped_config = scope_config(config_on_disk, "default")

    assert does_directory_contain_files(file_list, scoped_config["journal"])


@then(parse('journal "{journal_name}" should not exist'))
def journal_directory_should_not_exist(config_on_disk, journal_name):
    scoped_config = scope_config(config_on_disk, journal_name)

    assert not does_directory_contain_files(
        scoped_config["journal"], "."
    ), f'Journal "{journal_name}" does exist'


@then(parse("the journal {should_or_should_not} exist"))
def journal_should_not_exist(config_on_disk, should_or_should_not):
    scoped_config = scope_config(config_on_disk, "default")
    expected_path = scoped_config["journal"]

    contains_files = does_directory_contain_files(expected_path, ".")

    if should_or_should_not == "should":
        assert contains_files
    elif should_or_should_not == "should not":
        assert not contains_files
    else:
        raise Exception(
            "should_or_should_not valid values are 'should' or 'should not'"
        )


@then(parse('the journal "{journal_name}" directory {should_or_should_not} exist'))
def directory_should_not_exist(config_on_disk, should_or_should_not, journal_name):
    scoped_config = scope_config(config_on_disk, journal_name)
    expected_path = scoped_config["journal"]
    we_should = parse_should_or_should_not(should_or_should_not)
    dir_exists = os.path.isdir(expected_path)

    assert dir_exists == we_should


@then(parse('the content of file "{file_path}" in the cache should be\n{file_content}'))
def content_of_file_should_be(file_path, file_content, cache_dir):
    assert cache_dir["exists"]
    expected_content = file_content.strip().splitlines()

    with open(os.path.join(cache_dir["path"], file_path), "r") as f:
        actual_content = f.read().strip().splitlines()

    for actual_line, expected_line in zip(actual_content, expected_content):
        if actual_line.startswith("tags: ") and expected_line.startswith("tags: "):
            assert_equal_tags_ignoring_order(
                actual_line, expected_line, actual_content, expected_content
            )
        else:
            assert actual_line.strip() == expected_line.strip(), [
                [actual_line.strip(), expected_line.strip()],
                [actual_content, expected_content],
            ]


@then(parse("the cache should contain the files\n{file_list}"))
def cache_dir_contains_files(file_list, cache_dir):
    assert cache_dir["exists"]

    actual_files = os.listdir(cache_dir["path"])
    expected_files = file_list.split("\n")

    # sort to deal with inconsistent default file ordering on different OS's
    actual_files.sort()
    expected_files.sort()

    assert actual_files == expected_files, [actual_files, expected_files]


@then(parse("the output should be valid {language_name}"))
def assert_output_is_valid_language(cli_run, language_name):
    language_name = language_name.upper()
    if language_name == "XML":
        xml_tree = ElementTree.fromstring(cli_run["stdout"])
        assert xml_tree, "Invalid XML"
    elif language_name == "JSON":
        assert json.loads(cli_run["stdout"]), "Invalid JSON"
    else:
        assert False, f"Language name {language_name} not recognized"


@then(parse('"{node_name}" in the parsed output should have {number:d} elements'))
def assert_parsed_output_item_count(node_name, number, parsed_output):
    lang = parsed_output["lang"]
    obj = parsed_output["obj"]

    if lang == "XML":
        xml_node_names = (node.tag for node in obj)
        assert node_name in xml_node_names, str(list(xml_node_names))

        actual_entry_count = len(obj.find(node_name))
        assert actual_entry_count == number, actual_entry_count

    elif lang == "JSON":
        my_obj = obj

        for node in node_name.split("."):
            try:
                my_obj = my_obj[int(node)]
            except ValueError:
                assert node in my_obj
                my_obj = my_obj[node]

        assert len(my_obj) == number, len(my_obj)

    else:
        assert False, f"Language name {lang} not recognized"


@then(parse('"{field_name}" in the parsed output should {comparison}\n{expected_keys}'))
def assert_output_field_content(field_name, comparison, expected_keys, parsed_output):
    lang = parsed_output["lang"]
    obj = parsed_output["obj"]
    expected_keys = expected_keys.split("\n")
    if len(expected_keys) == 1:
        expected_keys = expected_keys[0]

    if lang == "XML":
        xml_node_names = (node.tag for node in obj)
        assert field_name in xml_node_names, str(list(xml_node_names))

        if field_name == "tags":
            actual_tags = set(t.attrib["name"] for t in obj.find("tags"))
            assert set(actual_tags) == set(expected_keys), [
                actual_tags,
                set(expected_keys),
            ]
        else:
            assert False, "This test only works for tags in XML"

    elif lang == "JSON":
        my_obj = obj

        for node in field_name.split("."):
            try:
                my_obj = my_obj[int(node)]
            except ValueError:
                assert node in my_obj, [my_obj.keys(), node]
                my_obj = my_obj[node]

        if comparison == "be":
            if type(my_obj) is str:
                assert expected_keys == my_obj, [my_obj, expected_keys]
            else:
                assert set(expected_keys) == set(my_obj), [
                    set(my_obj),
                    set(expected_keys),
                ]
        elif comparison == "contain":
            if type(my_obj) is str:
                assert expected_keys in my_obj, [my_obj, expected_keys]
            else:
                assert all(elem in my_obj for elem in expected_keys), [
                    my_obj,
                    expected_keys,
                ]
    else:
        assert False, f"Language name {lang} not recognized"


@then(parse('there should be {number:d} "{item}" elements'))
def count_elements(number, item, cli_run):
    actual_output = cli_run["stdout"]
    xml_tree = ElementTree.fromstring(actual_output)
    assert len(xml_tree.findall(".//" + item)) == number


@then(parse("the editor {should_or_should_not} have been called"))
@then(
    parse(
        "the editor {should_or_should_not} have been called with {num_args} arguments"
    )
)
def count_editor_args(num_args, cli_run, editor_state, should_or_should_not):
    we_should = parse_should_or_should_not(should_or_should_not)

    assert cli_run["mocks"]["editor"].called == we_should

    if isinstance(num_args, int):
        assert len(editor_state["command"]) == int(num_args)


@then(parse("the stdin prompt {should_or_should_not} have been called"))
def stdin_prompt_called(cli_run, should_or_should_not):
    we_should = parse_should_or_should_not(should_or_should_not)

    assert cli_run["mocks"]["stdin_input"].called == we_should


@then(parse('the editor filename should end with "{suffix}"'))
def editor_filename_suffix(suffix, editor_state):
    editor_filename = editor_state["tmpfile"]["name"]

    assert editor_state["tmpfile"]["name"].endswith(suffix), (editor_filename, suffix)


@then(parse('the editor file content should {comparison} "{str_value}"'))
@then(parse("the editor file content should {comparison} empty"))
@then(parse("the editor file content should {comparison}\n{str_value}"))
def contains_editor_file(comparison, str_value, editor_state):
    content = editor_state["tmpfile"]["content"]
    # content = f'\n"""\n{content}\n"""\n'
    if comparison == "be":
        assert content == str_value
    elif comparison == "contain":
        assert str_value in content
    else:
        assert False, f"Comparison '{comparison}' not supported"
