from behave import *
from jrnl import jrnl, Journal, util
from dateutil import parser as date_parser
import os
import sys
import json
import pytz
import keyring
try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO

def _parse_args(command):
    nargs=[]
    concats = []
    for a in command.split()[1:]:
        if a.startswith("'"):
            concats.append(a.strip("'"))
        elif a.endswith("'"):
            concats.append(a.strip("'"))
            nargs.append(u" ".join(concats))
            concats = []
        else:
            nargs.append(a)
    return nargs

def read_journal(journal_name="default"):
    with open(jrnl.CONFIG_PATH) as config_file:
        config = json.load(config_file)
    with open(config['journals'][journal_name]) as journal_file:
        journal = journal_file.read()
    return journal

def open_journal(journal_name="default"):
    with open(jrnl.CONFIG_PATH) as config_file:
        config = json.load(config_file)
    journal_conf = config['journals'][journal_name]
    if type(journal_conf) is dict:  # We can override the default config on a by-journal basis
        config.update(journal_conf)
    else:  # But also just give them a string to point to the journal file
        config['journal'] = journal_conf
    return Journal.Journal(**config)

@given('we use the config "{config_file}"')
def set_config(context, config_file):
    full_path = os.path.join("features/configs", config_file)
    jrnl.CONFIG_PATH = os.path.abspath(full_path)

@when('we run "{command}" and enter')
@when('we run "{command}" and enter "{inputs}"')
def run_with_input(context, command, inputs=None):
    text = inputs or context.text
    args = _parse_args(command)
    buffer = StringIO(text.strip())
    jrnl.util.STDIN = buffer
    try:
        jrnl.cli(args or None)
        context.exit_status = 0
    except SystemExit as e:
        context.exit_status = e.code

@when('we run "{command}"')
def run(context, command):
    args = _parse_args(command)
    try:
        jrnl.cli(args or None)
        context.exit_status = 0
    except SystemExit as e:
        context.exit_status = e.code

@when('we set the keychain password of "{journal}" to "{password}"')
def set_keychain(context, journal, password):
    keyring.set_password('jrnl', journal, password)

@then('we should get an error')
def has_error(context):
    assert context.exit_status != 0, context.exit_status

@then('we should get no error')
def no_error(context):
    assert context.exit_status is 0, context.exit_status

@then('the output should be parsable as json')
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

@then('the output should be')
def check_output(context):
    text = context.text.strip().splitlines()
    out = context.stdout_capture.getvalue().strip().splitlines()
    for line_text, line_out in zip(text, out):
        assert line_text.strip() == line_out.strip(), [line_text.strip(), line_out.strip()]

@then('the output should contain "{text}" in the local time')
def check_output_time_inline(context, text):
    out = context.stdout_capture.getvalue()
    local_tz = pytz.timezone(util.get_local_timezone())
    utc_time = date_parser.parse(text)
    date = utc_time + local_tz._utcoffset
    local_date = date.strftime("%Y-%m-%d %H:%M")
    assert local_date in out, local_date

@then('the output should contain "{text}"')
def check_output_inline(context, text):
    out = context.stdout_capture.getvalue()
    assert text in out

@then('the output should not contain "{text}"')
def check_output_not_inline(context, text):
    out = context.stdout_capture.getvalue()
    assert text not in out

@then('we should see the message "{text}"')
def check_message(context, text):
    out = context.messages.getvalue()
    assert text in out, [text, out]

@then('we should not see the message "{text}"')
def check_not_message(context, text):
    out = context.messages.getvalue()
    assert text not in out, [text, out]

@then('the journal should contain "{text}"')
@then('journal "{journal_name}" should contain "{text}"')
def check_journal_content(context, text, journal_name="default"):
    journal = read_journal(journal_name)
    assert text in journal

@then('journal "{journal_name}" should not exist')
def journal_doesnt_exist(context, journal_name="default"):
    with open(jrnl.CONFIG_PATH) as config_file:
        config = json.load(config_file)
    journal_path = config['journals'][journal_name]
    assert not os.path.exists(journal_path)

@then('the config should have "{key}" set to "{value}"')
@then('the config for journal "{journal}" should have "{key}" set to "{value}"')
def config_var(context, key, value, journal=None):
    t, value = value.split(":")
    value = {
        "bool": lambda v: v.lower() == "true",
        "int": int,
        "str": str
    }[t](value)
    with open(jrnl.CONFIG_PATH) as config_file:
        config = json.load(config_file)
    if journal:
        config = config["journals"][journal]
    assert key in config
    assert config[key] == value

@then('the journal should have {number:d} entries')
@then('the journal should have {number:d} entry')
@then('journal "{journal_name}" should have {number:d} entries')
@then('journal "{journal_name}" should have {number:d} entry')
def check_journal_content(context, number, journal_name="default"):
    journal = open_journal(journal_name)
    assert len(journal.entries) == number

@then('fail')
def debug_fail(context):
    assert False
