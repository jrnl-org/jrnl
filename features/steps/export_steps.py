# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import json
import os
import shutil
import random
import string
from xml.etree import ElementTree

from behave import given
from behave import then


@then("the output should be parsable as json")
def check_output_json(context):
    out = context.stdout_capture.getvalue()
    assert json.loads(out), out


@then('"{field}" in the json output should have {number:d} elements')
@then('"{field}" in the json output should have 1 element')
def check_output_field(context, field, number=1):
    out = context.stdout_capture.getvalue()
    out_json = json.loads(out)
    assert field in out_json, [field, out_json]
    assert len(out_json[field]) == number, len(out_json[field])


@then('"{field}" in the json output should not contain "{key}"')
def check_output_field_not_key(context, field, key):
    out = context.stdout_capture.getvalue()
    out_json = json.loads(out)
    assert field in out_json
    assert key not in out_json[field]


@then('"{field}" in the json output should contain "{key}"')
def check_output_field_key(context, field, key):
    out = context.stdout_capture.getvalue()
    struct = json.loads(out)

    for node in field.split("."):
        try:
            struct = struct[int(node)]
        except ValueError:
            assert node in struct
            struct = struct[node]

    assert key in struct


@then("the json output should contain {path}")
@then('the json output should contain {path} = "{value}"')
def check_json_output_path(context, path, value=None):
    """E.g.
    the json output should contain entries.0.title = "hello"
    """
    out = context.stdout_capture.getvalue()
    struct = json.loads(out)

    for node in path.split("."):
        try:
            struct = struct[int(node)]
        except ValueError:
            struct = struct[node]

    if value is not None:
        assert struct == value, struct
    else:
        assert struct is not None


@then(
    'entry {entry_number:d} should have an array "{name}" with {items_number:d} elements'
)
def entry_array_count(context, entry_number, name, items_number):
    # note that entry_number is 1-indexed.
    out = context.stdout_capture.getvalue()
    out_json = json.loads(out)
    assert len(out_json["entries"][entry_number - 1][name]) == items_number


@then("the output should be a valid XML string")
def assert_valid_xml_string(context):
    output = context.stdout_capture.getvalue()
    xml_tree = ElementTree.fromstring(output)
    assert xml_tree, output


@then('"{item}" node in the xml output should have {number:d} elements')
def assert_xml_output_entries_count(context, item, number):
    output = context.stdout_capture.getvalue()
    xml_tree = ElementTree.fromstring(output)

    xml_tags = (node.tag for node in xml_tree)
    assert item in xml_tags, str(list(xml_tags))

    actual_entry_count = len(xml_tree.find(item))
    assert actual_entry_count == number, actual_entry_count


@then('there should be {number:d} "{item}" elements')
def count_elements(context, number, item):
    output = context.stdout_capture.getvalue()
    xml_tree = ElementTree.fromstring(output)
    assert len(xml_tree.findall(".//" + item)) == number


@then('"tags" in the xml output should contain {expected_tags_json_list}')
def assert_xml_output_tags(context, expected_tags_json_list):
    output = context.stdout_capture.getvalue()
    xml_tree = ElementTree.fromstring(output)

    xml_tags = (node.tag for node in xml_tree)
    assert "tags" in xml_tags, str(list(xml_tags))

    expected_tags = json.loads(expected_tags_json_list)
    actual_tags = set(t.attrib["name"] for t in xml_tree.find("tags"))
    assert actual_tags == set(expected_tags), [actual_tags, set(expected_tags)]


@given('we create cache directory "{dir_name}"')
@given("we create a cache directory")
def create_directory(context, dir_name=None):
    if not dir_name:
        dir_name = "cache_" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=20)
        )

    working_dir = os.path.join("features", "cache", dir_name)
    if os.path.exists(working_dir):
        shutil.rmtree(working_dir)
    os.makedirs(working_dir)
    context.cache_dir = dir_name


@then('cache "{dir_name}" should contain the files')
@then('cache "{dir_name}" should contain the files {expected_files_json_list}')
@then("the cache should contain the files")
def assert_dir_contains_files(context, dir_name=None, expected_files_json_list=""):
    if not dir_name:
        dir_name = context.cache_dir

    working_dir = os.path.join("features", "cache", dir_name)
    actual_files = os.listdir(working_dir)

    expected_files = context.text or expected_files_json_list
    expected_files = expected_files.split("\n")

    # sort to deal with inconsistent default file ordering on different OS's
    actual_files.sort()
    expected_files.sort()

    assert actual_files == expected_files, [actual_files, expected_files]


@then('the content of file "{file_path}" in cache directory "{cache_dir}" should be')
@then('the content of file "{file_path}" in the cache should be')
def assert_exported_yaml_file_content(context, file_path, cache_dir=None):
    if not cache_dir:
        cache_dir = context.cache_dir

    expected_content = context.text.strip().splitlines()
    full_file_path = os.path.join("features", "cache", cache_dir, file_path)

    with open(full_file_path, "r") as f:
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


def assert_equal_tags_ignoring_order(
    actual_line, expected_line, actual_content, expected_content
):
    actual_tags = set(tag.strip() for tag in actual_line[len("tags: ") :].split(","))
    expected_tags = set(
        tag.strip() for tag in expected_line[len("tags: ") :].split(",")
    )
    assert actual_tags == expected_tags, [
        [actual_tags, expected_tags],
        [expected_content, actual_content],
    ]
