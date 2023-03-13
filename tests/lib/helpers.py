# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import functools
import os


def does_directory_contain_files(file_list, directory_path):
    if not os.path.isdir(directory_path):
        return False

    for file in file_list.split("\n"):
        fullpath = directory_path + "/" + file
        if not os.path.isfile(fullpath):
            return False

    return True


def does_directory_contain_n_files(directory_path, number):
    count = 0
    if not os.path.isdir(directory_path):
        return False

    files = [
        f
        for f in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, f))
    ]
    count = len(files)

    return int(number) == count


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


# @see: https://stackoverflow.com/a/65782539/569146
def get_nested_val(dictionary, path, *default):
    try:
        return functools.reduce(lambda x, y: x[y], path.split("."), dictionary)
    except KeyError:
        if default:
            return default[0]
        raise


# @see: https://stackoverflow.com/a/41599695/569146
def spy_wrapper(wrapped_function):
    from unittest import mock

    mock = mock.MagicMock()

    def wrapper(self, *args, **kwargs):
        mock(*args, **kwargs)
        return wrapped_function(self, *args, **kwargs)

    wrapper.mock = mock
    return wrapper


def get_fixture(request, name, default=None):
    try:
        return request.getfixturevalue(name)
    except LookupError:
        return default
