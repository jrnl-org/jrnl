#!/usr/bin/env python
# encoding: utf-8

"""
    jrnl

    license: MIT, see LICENSE for more details.
"""

try:
    from . import Journal
    from . import util
    from . import exporters
    from . import install
except (SystemError, ValueError):
    import Journal
    import util
    import exporters
    import install
import os
import tempfile
import subprocess
import argparse
import sys
try: import simplejson as json
except ImportError: import json

xdg_config = os.environ.get('XDG_CONFIG_HOME')
CONFIG_PATH = os.path.join(xdg_config, "jrnl") if xdg_config else os.path.expanduser('~/.jrnl_config')
PYCRYPTO = install.module_exists("Crypto")


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    composing = parser.add_argument_group('Composing', 'Will make an entry out of whatever follows as arguments')
    composing.add_argument('-date', dest='date', help='Date, e.g. "yesterday at 5pm"')
    composing.add_argument('-star', dest='star', help='Stars an entry (DayOne journals only)', action="store_true")
    composing.add_argument('text', metavar='text', nargs="*",  help='Log entry (or tags by which to filter in viewing mode)')

    reading = parser.add_argument_group('Reading', 'Specifying either of these parameters will display posts of your journal')
    reading.add_argument('-from', dest='start_date', metavar="DATE", help='View entries after this date')
    reading.add_argument('-until', '-to', dest='end_date', metavar="DATE", help='View entries before this date')
    reading.add_argument('-and', dest='strict', action="store_true", help='Filter by tags using AND (default: OR)')
    reading.add_argument('-n', dest='limit', default=None, metavar="N", help='Shows the last n entries matching the filter', nargs="?", type=int)
    reading.add_argument('-short', dest='short', action="store_true", help='Show only titles or line containing the search tags')

    exporting = parser.add_argument_group('Export / Import', 'Options for transmogrifying your journal')
    exporting.add_argument('--tags', dest='tags', action="store_true", help='Returns a list of all tags and number of occurences')
    exporting.add_argument('--export', metavar='TYPE', dest='export', help='Export your journal to Markdown, JSON or Text', nargs='?', default=False, const=None)
    exporting.add_argument('-o', metavar='OUTPUT', dest='output', help='The output of the file can be provided when using with --export', nargs='?', default=False, const=None)
    exporting.add_argument('--encrypt',  metavar='FILENAME', dest='encrypt', help='Encrypts your existing journal with a new password', nargs='?', default=False, const=None)
    exporting.add_argument('--decrypt',  metavar='FILENAME', dest='decrypt', help='Decrypts your journal and stores it in plain text', nargs='?', default=False, const=None)
    exporting.add_argument('--delete-last', dest='delete_last', help='Deletes the last entry from your journal file.', action="store_true")

    return parser.parse_args(args)

def guess_mode(args, config):
    """Guesses the mode (compose, read or export) from the given arguments"""
    compose = True
    export = False
    if args.decrypt is not False or args.encrypt is not False or args.export is not False or args.tags or args.delete_last:
        compose = False
        export = True
    elif args.start_date or args.end_date or args.limit or args.strict or args.short:
        # Any sign of displaying stuff?
        compose = False
    elif not args.date and args.text and all(word[0] in config['tagsymbols'] for word in " ".join(args.text).split()):
        # No date and only tags?
        compose = False

    return compose, export

def get_text_from_editor(config):
    tmpfile = os.path.join(tempfile.gettempdir(), "jrnl")
    subprocess.call(config['editor'].split() + [tmpfile])
    if os.path.exists(tmpfile):
        with open(tmpfile) as f:
            raw = f.read()
        os.remove(tmpfile)
    else:
        util.prompt('[Nothing saved to file]')
        raw = ''

    return raw


def encrypt(journal, filename=None):
    """ Encrypt into new file. If filename is not set, we encrypt the journal file itself. """
    journal.config['password'] = ""
    journal.make_key(prompt="Enter new password:")
    journal.config['encrypt'] = True
    journal.write(filename)
    util.prompt("Journal encrypted to {0}.".format(filename or journal.config['journal']))

def decrypt(journal, filename=None):
    """ Decrypts into new file. If filename is not set, we encrypt the journal file itself. """
    journal.config['encrypt'] = False
    journal.config['password'] = ""
    journal.write(filename)
    util.prompt("Journal decrypted to {0}.".format(filename or journal.config['journal']))

def touch_journal(filename):
    """If filename does not exist, touch the file"""
    if not os.path.exists(filename):
        util.prompt("[Journal created at {0}]".format(filename))
        open(filename, 'a').close()

def update_config(config, new_config, scope):
    """Updates a config dict with new values - either global if scope is None
    of config['journals'][scope] is just a string pointing to a journal file,
    or within the scope"""
    if scope and type(config['journals'][scope]) is dict: # Update to journal specific
        config['journals'][scope].update(new_config)
    else:
        config.update(new_config)


def cli(manual_args=None):
    if not os.path.exists(CONFIG_PATH):
        config = install.install_jrnl(CONFIG_PATH)
    else:
        with open(CONFIG_PATH) as f:
            try:
                config = json.load(f)
            except ValueError as e:
                util.prompt("[There seems to be something wrong with your jrnl config at {0}: {1}]".format(CONFIG_PATH, e.message))
                util.prompt("[Entry was NOT added to your journal]")
                sys.exit(1)
        install.update_config(config, config_path=CONFIG_PATH)

    original_config = config.copy()
    # check if the configuration is supported by available modules
    if config['encrypt'] and not PYCRYPTO:
        util.prompt("According to your jrnl_conf, your journal is encrypted, however PyCrypto was not found. To open your journal, install the PyCrypto package from http://www.pycrypto.org.")
        sys.exit(1)

    args = parse_args(manual_args)

    # If the first textual argument points to a journal file,
    # use this!
    journal_name = args.text[0] if (args.text and args.text[0] in config['journals']) else 'default'
    if journal_name is not 'default':
        args.text = args.text[1:]
    journal_conf = config['journals'].get(journal_name)
    if type(journal_conf) is dict: # We can override the default config on a by-journal basis
        config.update(journal_conf)
    else: # But also just give them a string to point to the journal file
        config['journal'] = journal_conf
    touch_journal(config['journal'])
    mode_compose, mode_export = guess_mode(args, config)

    # open journal file or folder
    if os.path.isdir(config['journal']):
        if config['journal'].strip("/").endswith(".dayone") or \
           "entries" in os.listdir(config['journal']):
            journal = Journal.DayOne(**config)
        else:
            util.prompt("[Error: {0} is a directory, but doesn't seem to be a DayOne journal either.".format(config['journal']))
            sys.exit(1)
    else:
        journal = Journal.Journal(**config)

    if mode_compose and not args.text:
        if config['editor']:
            raw = get_text_from_editor(config)
        else:
            raw = util.py23_input("[Compose Entry] ")
        if raw:
            args.text = [raw]
        else:
            mode_compose = False

    # Writing mode
    if mode_compose:
        raw = " ".join(args.text).strip()
        if util.PY2 and type(raw) is not unicode:
            raw = raw.decode(sys.getfilesystemencoding())
        entry = journal.new_entry(raw, args.date)
        entry.starred = args.star
        util.prompt("[Entry added to {0} journal]".format(journal_name))
        journal.write()
    else:
        journal.filter(tags=args.text,
                       start_date=args.start_date, end_date=args.end_date,
                       strict=args.strict,
                       short=args.short)
        journal.limit(args.limit)

    # Reading mode
    if not mode_compose and not mode_export:
        print(journal.pprint())

    # Various export modes
    elif args.tags:
        print(exporters.to_tag_list(journal))

    elif args.export is not False:
        print(exporters.export(journal, args.export, args.output))

    elif (args.encrypt is not False or args.decrypt is not False) and not PYCRYPTO:
        util.prompt("PyCrypto not found. To encrypt or decrypt your journal, install the PyCrypto package from http://www.pycrypto.org.")

    elif args.encrypt is not False:
        encrypt(journal, filename=args.encrypt)
        # Not encrypting to a separate file: update config!
        if not args.encrypt:
            update_config(original_config, {"encrypt": True, "password": ""}, journal_name)
            install.save_config(original_config, config_path=CONFIG_PATH)

    elif args.decrypt is not False:
        decrypt(journal, filename=args.decrypt)
        # Not decrypting to a separate file: update config!
        if not args.decrypt:
            update_config(original_config, {"encrypt": False, "password": ""}, journal_name)
            install.save_config(original_config, config_path=CONFIG_PATH)

    elif args.delete_last:
        last_entry = journal.entries.pop()
        util.prompt("[Deleted Entry:]")
        print(last_entry)
        journal.write()

if __name__ == "__main__":
    cli()

