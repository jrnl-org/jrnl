# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

"""
Certain functions to support the *behave* test suite.

They are placed here so they are importable in multiple places, as otherwise
imports fail when running the suite outside of the project's root folder.

"""
import jrnl.time


def _mock_getpass(inputs):
    def prompt_return(prompt=""):
        if type(inputs) == str:
            return inputs
        try:
            return next(inputs)
        except StopIteration:
            raise KeyboardInterrupt

    return prompt_return


def _mock_input(inputs):
    def prompt_return(prompt=""):
        try:
            val = next(inputs)
            print(prompt, val)
            return val
        except StopIteration:
            raise KeyboardInterrupt

    return prompt_return


def _mock_time_parse(context):
    original_parse = jrnl.time.parse
    if "now" not in context:
        return original_parse

    def wrapper(input, *args, **kwargs):
        input = context.now if input == "now" else input
        return original_parse(input, *args, **kwargs)

    return wrapper
