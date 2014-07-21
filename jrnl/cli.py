#!/usr/bin/env python
# encoding: utf-8

"""
    jrnl

    license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import
from . import Journal
from . import DayOneJournal
from . import util
from . import exporters
from . import install
import jrnl
import os
import argparse
import sys

xdg_config = os.environ.get('XDG_CONFIG_HOME')
CONFIG_PATH = os.path.join(xdg_config, "jrnl") if xdg_config else os.path.expanduser('~/.jrnl_config')
PYCRYPTO = install.module_exists("Crypto")


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', dest='version', action="store_true", help="prints version information and exits")
    parser.add_argument('-ls', dest='ls', action="store_true", help="displays accessible journals")

    composing = parser.add_argument_group('Composing', 'To write an entry simply write it on the command line, e.g. "jrnl yesterday at 1pm: Went to the gym."')
    composing.add_argument('text', metavar='', nargs="*")

    reading = parser.add_argument_group('Reading', 'Specifying either of these parameters will display posts of your journal')
    reading.add_argument('-from', dest='start_date', metavar="DATE", help='View entries after this date')
    reading.add_argument('-until', '-to', dest='end_date', metavar="DATE", help='View entries before this date')
    reading.add_argument('-on', dest='on_date', metavar="DATE", help='View entries on this date')
    reading.add_argument('-and', dest='strict', action="store_true", help='Filter by tags using AND (default: OR)')
    reading.add_argument('-starred', dest='starred', action="store_true", help='Show only starred entries')
    reading.add_argument('-n', dest='limit', default=None, metavar="N", help="Shows the last n entries matching the filter. '-n 3' and '-3' have the same effect.", nargs="?", type=int)

    exporting = parser.add_argument_group('Export / Import', 'Options for transmogrifying your journal')
    exporting.add_argument('--short', dest='short', action="store_true", help='Show only titles or line containing the search tags')
    exporting.add_argument('--tags', dest='tags', action="store_true", help='Returns a list of all tags and number of occurences')
    exporting.add_argument('--export', metavar='TYPE', dest='export', choices=['text', 'txt', 'markdown', 'md', 'json'], help='Export your journal. TYPE can be json, markdown, or text.', default=False, const=None)
    exporting.add_argument('-o', metavar='OUTPUT', dest='output', help='Optionally specifies output file when using --export. If OUTPUT is a directory, exports each entry into an individual file instead.', default=False, const=None)
    exporting.add_argument('--encrypt', metavar='FILENAME', dest='encrypt', help='Encrypts your existing journal with a new password', nargs='?', default=False, const=None)
    exporting.add_argument('--decrypt', metavar='FILENAME', dest='decrypt', help='Decrypts your journal and stores it in plain text', nargs='?', default=False, const=None)
    exporting.add_argument('--edit', dest='edit', help='Opens your editor to edit the selected entries.', action="store_true")

    return parser.parse_args(args)


def guess_mode(args, config):
    """Guesses the mode (compose, read or export) from the given arguments"""
    compose = True
    export = False
    if args.decrypt is not False or args.encrypt is not False or args.export is not False or any((args.short, args.tags, args.edit)):
        compose = False
        export = True
    elif any((args.start_date, args.end_date, args.on_date, args.limit, args.strict, args.starred)):
        # Any sign of displaying stuff?
        compose = False
    elif args.text and all(word[0] in config['tagsymbols'] for word in u" ".join(args.text).split()):
        # No date and only tags?
        compose = False

    return compose, export


def encrypt(journal, filename=None):
    """ Encrypt into new file. If filename is not set, we encrypt the journal file itself. """
    password = util.getpass("Enter new password: ")
    journal.make_key(password)
    journal.config['encrypt'] = True
    journal.write(filename)
    if util.yesno("Do you want to store the password in your keychain?", default=True):
        util.set_keychain(journal.name, password)
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


def list_journals(config):
    """List the journals specified in the configuration file"""
    sep = "\n"
    journal_list = sep.join(config['journals'])
    return journal_list


def update_config(config, new_config, scope, force_local=False):
    """Updates a config dict with new values - either global if scope is None
    or config['journals'][scope] is just a string pointing to a journal file,
    or within the scope"""
    if scope and type(config['journals'][scope]) is dict:  # Update to journal specific
        config['journals'][scope].update(new_config)
    elif scope and force_local:  # Convert to dict
        config['journals'][scope] = {"journal": config['journals'][scope]}
        config['journals'][scope].update(new_config)
    else:
        config.update(new_config)


def run(manual_args=None):
    args = parse_args(manual_args)
    args.text = [p.decode('utf-8') if util.PY2 and not isinstance(p, unicode) else p for p in args.text]
    if args.version:
        version_str = "{0} version {1}".format(jrnl.__title__, jrnl.__version__)
        print(util.py2encode(version_str))
        sys.exit(0)

    if not os.path.exists(CONFIG_PATH):
        config = install.install_jrnl(CONFIG_PATH)
    else:
        config = util.load_and_fix_json(CONFIG_PATH)
        install.upgrade_config(config, config_path=CONFIG_PATH)

    if args.ls:
        print(util.py2encode(list_journals(config)))
        sys.exit(0)

    original_config = config.copy()
    # check if the configuration is supported by available modules
    if config['encrypt'] and not PYCRYPTO:
        util.prompt("According to your jrnl_conf, your journal is encrypted, however PyCrypto was not found. To open your journal, install the PyCrypto package from http://www.pycrypto.org.")
        sys.exit(1)

    # If the first textual argument points to a journal file,
    # use this!
    journal_name = args.text[0] if (args.text and args.text[0] in config['journals']) else 'default'
    if journal_name is not 'default':
        args.text = args.text[1:]
    # If the first remaining argument looks like e.g. '-3', interpret that as a limiter
    if not args.limit and args.text and args.text[0].startswith("-"):
        try:
            args.limit = int(args.text[0].lstrip("-"))
            args.text = args.text[1:]
        except:
            pass

    journal_conf = config['journals'].get(journal_name)
    if type(journal_conf) is dict:  # We can override the default config on a by-journal basis
        config.update(journal_conf)
    else:  # But also just give them a string to point to the journal file
        config['journal'] = journal_conf
    config['journal'] = os.path.expanduser(os.path.expandvars(config['journal']))
    touch_journal(config['journal'])
    mode_compose, mode_export = guess_mode(args, config)

    # How to quit writing?
    if "win32" in sys.platform:
        _exit_multiline_code = "on a blank line, press Ctrl+Z and then Enter"
    else:
        _exit_multiline_code = "press Ctrl+D"

    if mode_compose and not args.text:
        if not sys.stdin.isatty():
            # Piping data into jrnl
            raw = util.py23_read()
        elif config['editor']:
            raw = util.get_text_from_editor(config)
        else:
            try:
                raw = util.py23_read("[Compose Entry; " + _exit_multiline_code + " to finish writing]\n")
            except KeyboardInterrupt:
                util.prompt("[Entry NOT saved to journal.]")
                sys.exit(0)
        if raw:
            args.text = [raw]
        else:
            mode_compose = False

    # open journal file or folder
    if os.path.isdir(config['journal']):
        if config['journal'].strip("/").endswith(".dayone") or \
           "entries" in os.listdir(config['journal']):
            journal = DayOneJournal.DayOne(**config)
        else:
            util.prompt(u"[Error: {0} is a directory, but doesn't seem to be a DayOne journal either.".format(config['journal']))
            sys.exit(1)
    else:
        journal = Journal.Journal(journal_name, **config)

    # Writing mode
    if mode_compose:
        raw = " ".join(args.text).strip()
        if util.PY2 and type(raw) is not unicode:
            raw = raw.decode(sys.getfilesystemencoding())
        journal.new_entry(raw)
        util.prompt("[Entry added to {0} journal]".format(journal_name))
        journal.write()
    else:
        old_entries = journal.entries
        if args.on_date:
            args.start_date = args.end_date = args.on_date
        journal.filter(tags=args.text,
                       start_date=args.start_date, end_date=args.end_date,
                       strict=args.strict,
                       short=args.short,
                       starred=args.starred)
        journal.limit(args.limit)

    # Reading mode
    if not mode_compose and not mode_export:
        print(util.py2encode(journal.pprint()))

    # Various export modes
    elif args.short:
        print(util.py2encode(journal.pprint(short=True)))

    elif args.tags:
        print(util.py2encode(exporters.to_tag_list(journal)))

    elif args.export is not False:
        print(util.py2encode(exporters.export(journal, args.export, args.output)))

    elif (args.encrypt is not False or args.decrypt is not False) and not PYCRYPTO:
        util.prompt("PyCrypto not found. To encrypt or decrypt your journal, install the PyCrypto package from http://www.pycrypto.org.")

    elif args.encrypt is not False:
        encrypt(journal, filename=args.encrypt)
        # Not encrypting to a separate file: update config!
        if not args.encrypt:
            update_config(original_config, {"encrypt": True}, journal_name, force_local=True)
            install.save_config(original_config, config_path=CONFIG_PATH)

    elif args.decrypt is not False:
        decrypt(journal, filename=args.decrypt)
        # Not decrypting to a separate file: update config!
        if not args.decrypt:
            update_config(original_config, {"encrypt": False}, journal_name, force_local=True)
            install.save_config(original_config, config_path=CONFIG_PATH)

    elif args.edit:
        if not config['editor']:
            util.prompt(u"[You need to specify an editor in {0} to use the --edit function.]".format(CONFIG_PATH))
            sys.exit(1)
        other_entries = [e for e in old_entries if e not in journal.entries]
        # Edit
        old_num_entries = len(journal)
        edited = util.get_text_from_editor(config, journal.editable_str())
        journal.parse_editable_str(edited)
        num_deleted = old_num_entries - len(journal)
        num_edited = len([e for e in journal.entries if e.modified])
        prompts = []
        if num_deleted:
            prompts.append("{0} {1} deleted".format(num_deleted, "entry" if num_deleted == 1 else "entries"))
        if num_edited:
            prompts.append("{0} {1} modified".format(num_edited, "entry" if num_deleted == 1 else "entries"))
        if prompts:
            util.prompt("[{0}]".format(", ".join(prompts).capitalize()))
        journal.entries += other_entries
        journal.write()

if __name__ == "__main__":
    run()
