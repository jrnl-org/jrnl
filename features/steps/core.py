from behave import *
from jrnl import jrnl
import os
import sys
import json
import StringIO

def read_journal(journal_name="default"):
    with open(jrnl.CONFIG_PATH) as config_file:
        config = json.load(config_file)
    with open(config['journals'][journal_name]) as journal_file:
        journal = journal_file.read()
    return journal

@given('we use the config "{config_file}"')
def set_config(context, config_file):
    full_path = os.path.join("features/configs", config_file)
    jrnl.CONFIG_PATH = os.path.abspath(full_path)

@when('we run "{command}" and enter')
@when('we run "{command}" and enter "{inputs}"')
def run_with_input(context, command, inputs=None):
    text = inputs or context.text
    args = command.split()[1:]
    buffer = StringIO.StringIO(text.strip())
    jrnl.util.STDIN = buffer
    jrnl.cli(args)

@when('we run "{command}"')
def run(context, command):
    args = command.split()[1:]
    jrnl.cli(args or None)


@then('we should get no error')
def no_error(context):
    assert context.failed is False

@then('the output should be')
def check_output(context):
    text = context.text.strip().splitlines()
    out = context.stdout_capture.getvalue().strip().splitlines()
    for line_text, line_out in zip(text, out):
        assert line_text.strip() == line_out.strip()

@then('the output should contain "{text}"')
def check_output_inline(context, text):
    out = context.stdout_capture.getvalue()
    print out
    assert text in out

@then('the journal should contain "{text}"')
@then('journal {journal_name} should contain "{text}"')
def check_journal_content(context, text, journal_name="default"):
    journal = read_journal(journal_name)
    assert text in journal

