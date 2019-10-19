from __future__ import unicode_literals
from __future__ import absolute_import

from behave import given, when, then
from jrnl import cli, install, Journal, util, plugins
from jrnl import __version__
from dateutil import parser as date_parser
from collections import defaultdict
import os
import json
import yaml
import keyring


class TestKeyring(keyring.backend.KeyringBackend):
    """A test keyring that just stores its valies in a hash"""

    priority = 1
    keys = defaultdict(dict)

    def set_password(self, servicename, username, password):
        self.keys[servicename][username] = password

    def get_password(self, servicename, username):
        return self.keys[servicename].get(username)

    def delete_password(self, servicename, username, password):
        self.keys[servicename][username] = None

# set the keyring for keyring lib
keyring.set_keyring(TestKeyring())


try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO
import tzlocal
import shlex
import sys


def ushlex(command):
    if sys.version_info[0] == 3:
        return shlex.split(command)
    return map(lambda s: s.decode('UTF8'), shlex.split(command.encode('utf8')))


def read_journal(journal_name="default"):
    config = util.load_config(install.CONFIG_FILE_PATH)
    with open(config['journals'][journal_name]) as journal_file:
        journal = journal_file.read()
    return journal


def open_journal(journal_name="default"):
    config = util.load_config(install.CONFIG_FILE_PATH)
    journal_conf = config['journals'][journal_name]
    if type(journal_conf) is dict:  # We can override the default config on a by-journal basis
        config.update(journal_conf)
    else:  # But also just give them a string to point to the journal file
        config['journal'] = journal_conf
    return Journal.open_journal(journal_name, config)


@given('we use the config "{config_file}"')
def set_config(context, config_file):
    full_path = os.path.join("features/configs", config_file)
    install.CONFIG_FILE_PATH = os.path.abspath(full_path)
    if config_file.endswith("yaml"):
        # Add jrnl version to file for 2.x journals
        with open(install.CONFIG_FILE_PATH, 'a') as cf:
            cf.write("version: {}".format(__version__))


@when('we run "{command}" and enter')
@when('we run "{command}" and enter "{inputs}"')
def run_with_input(context, command, inputs=None):
    text = inputs or context.text
    args = ushlex(command)[1:]
    buffer = StringIO(text.strip())
    util.STDIN = buffer
    try:
        cli.run(args or [])
        context.exit_status = 0
    except SystemExit as e:
        context.exit_status = e.code


@when('we run "{command}"')
def run(context, command):
    args = ushlex(command)[1:]
    try:
        cli.run(args or None)
        context.exit_status = 0
    except SystemExit as e:
        context.exit_status = e.code


@given('we load template "{filename}"')
def load_template(context, filename):
    full_path = os.path.join("features/data/templates", filename)
    exporter = plugins.template_exporter.__exporter_from_file(full_path)
    plugins.__exporter_types[exporter.names[0]] = exporter


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


@then('the json output should contain {path} = "{value}"')
def check_json_output_path(context, path, value):
    """ E.g.
    the json output should contain entries.0.title = "hello"
    """
    out = context.stdout_capture.getvalue()
    struct = json.loads(out)

    for node in path.split('.'):
        try:
            struct = struct[int(node)]
        except ValueError:
            struct = struct[node]
    assert struct == value, struct


@then('the output should be')
@then('the output should be "{text}"')
def check_output(context, text=None):
    text = (text or context.text).strip().splitlines()
    out = context.stdout_capture.getvalue().strip().splitlines()
    assert len(text) == len(out), "Output has {} lines (expected: {})".format(len(out), len(text))
    for line_text, line_out in zip(text, out):
        assert line_text.strip() == line_out.strip(), [line_text.strip(), line_out.strip()]


@then('the output should contain "{text}" in the local time')
def check_output_time_inline(context, text):
    out = context.stdout_capture.getvalue()
    local_tz = tzlocal.get_localzone()
    utc_time = date_parser.parse(text)
    local_date = utc_time.astimezone(local_tz).strftime("%Y-%m-%d %H:%M")
    assert local_date in out, local_date


@then('the output should contain')
@then('the output should contain "{text}"')
def check_output_inline(context, text=None):
    text = text or context.text
    out = context.stdout_capture.getvalue()
    if isinstance(out, bytes):
        out = out.decode('utf-8')
    assert text in out, text


@then('the output should not contain "{text}"')
def check_output_not_inline(context, text):
    out = context.stdout_capture.getvalue()
    if isinstance(out, bytes):
        out = out.decode('utf-8')
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
    assert text in journal, journal


@then('journal "{journal_name}" should not exist')
def journal_doesnt_exist(context, journal_name="default"):
    with open(install.CONFIG_FILE_PATH) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
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
    config = util.load_config(install.CONFIG_FILE_PATH)
    if journal:
        config = config["journals"][journal]
    assert key in config
    assert config[key] == value


@then('the journal should have {number:d} entries')
@then('the journal should have {number:d} entry')
@then('journal "{journal_name}" should have {number:d} entries')
@then('journal "{journal_name}" should have {number:d} entry')
def check_journal_entries(context, number, journal_name="default"):
    journal = open_journal(journal_name)
    assert len(journal.entries) == number


@then('fail')
def debug_fail(context):
    assert False
