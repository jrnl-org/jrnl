import json
import os
import shutil
from xml.etree import ElementTree

from behave import given, then


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
    out_json = json.loads(out)
    assert field in out_json
    assert key in out_json[field]


@then('the json output should contain {path} = "{value}"')
def check_json_output_path(context, path, value):
    """ E.g.
    the json output should contain entries.0.title = "hello"
    """
    out = context.stdout_capture.getvalue()
    struct = json.loads(out)

    for node in path.split("."):
        try:
            struct = struct[int(node)]
        except ValueError:
            struct = struct[node]
    assert struct == value, struct


@then("the output should be a valid XML string")
def assert_valid_xml_string(context):
    output = context.stdout_capture.getvalue()
    xml_tree = ElementTree.fromstring(output)
    assert xml_tree, output


@then('"entries" node in the xml output should have {number:d} elements')
def assert_xml_output_entries_count(context, number):
    output = context.stdout_capture.getvalue()
    xml_tree = ElementTree.fromstring(output)

    xml_tags = (node.tag for node in xml_tree)
    assert "entries" in xml_tags, str(list(xml_tags))

    actual_entry_count = len(xml_tree.find("entries"))
    assert actual_entry_count == number, actual_entry_count


@then('"tags" in the xml output should contain {expected_tags_json_list}')
def assert_xml_output_tags(context, expected_tags_json_list):
    output = context.stdout_capture.getvalue()
    xml_tree = ElementTree.fromstring(output)

    xml_tags = (node.tag for node in xml_tree)
    assert "tags" in xml_tags, str(list(xml_tags))

    expected_tags = json.loads(expected_tags_json_list)
    actual_tags = set(t.attrib["name"] for t in xml_tree.find("tags"))
    assert actual_tags == set(expected_tags), [actual_tags, set(expected_tags)]


@given('we created a directory named "{dir_name}"')
def create_directory(context, dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)


@then('"{dir_name}" should contain the files {expected_files_json_list}')
def assert_dir_contains_files(context, dir_name, expected_files_json_list):
    actual_files = os.listdir(dir_name)
    expected_files = json.loads(expected_files_json_list)
    assert actual_files == expected_files, [actual_files, expected_files]


@then('the content of exported yaml "{file_path}" should be')
def assert_exported_yaml_file_content(context, file_path):
    expected_content = context.text.strip().splitlines()

    with open(file_path, "r") as f:
        actual_content = f.read().strip().splitlines()

    for actual_line, expected_line in zip(actual_content, expected_content):
        if actual_line.startswith("tags: ") and expected_line.startswith("tags: "):
            assert_equal_tags_ignoring_order(actual_line, expected_line)
        else:
            assert actual_line.strip() == expected_line.strip(), [
                actual_line.strip(),
                expected_line.strip(),
            ]


def assert_equal_tags_ignoring_order(actual_line, expected_line):
    actual_tags = set(tag.strip() for tag in actual_line[len("tags: ") :].split(","))
    expected_tags = set(
        tag.strip() for tag in expected_line[len("tags: ") :].split(",")
    )
    assert actual_tags == expected_tags, [actual_tags, expected_tags]
