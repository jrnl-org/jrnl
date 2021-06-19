# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import os



def does_directory_contain_files(file_list, directory_path):
    if not os.path.isdir(directory_path):
        return False

    for file in file_list.split("\n"):
        fullpath = directory_path + "/" + file
        if not os.path.isfile(fullpath):
            return False

    return True


def parse_should_or_should_not(should_or_should_not):
    if should_or_should_not == "should":
        return True
    elif should_or_should_not == "should not":
        return False
    else:
        raise Exception(
            "should_or_should_not valid values are 'should' or 'should not'"
        )


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
