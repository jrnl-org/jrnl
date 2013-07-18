from behave import *
from jrnl import Journal, jrnl
import os

@given('we use "{config_file}"')
def set_config(context, config_file):
    full_path = os.path.join("features/configs", config_file)
    jrnl.CONFIG_PATH = os.path.abspath(full_path)

@when('we run "{command}"')
def run(context, command):
    args = command.split()[1:]
    jrnl.cli(args)

@then('we should get no error')
def no_error(context):
    assert context.failed is False

@then('the output should be')
def check_output(context):
    text = context.text.strip().splitlines()
    out = context.stdout_capture.getvalue().strip().splitlines()
    for line_text, line_out in zip(text, out):
        assert line_text.strip() == line_out.strip()
