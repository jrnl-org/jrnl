#!/usr/bin/env python
# encoding: utf-8

"""
    jrnl

    license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals
from __future__ import absolute_import
from . import Journal
from . import util
from . import install
from . import plugins
from .util import WARNING_COLOR, ERROR_COLOR, RESET_COLOR
import jrnl
import argparse
import sys
import logging
import os

log = logging.getLogger(__name__)


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', dest='version', action="store_true", help="prints version information and exits")
    parser.add_argument('-ls', dest='ls', action="store_true", help="displays accessible journals")
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='execute in debug mode')

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
    exporting.add_argument('-s', '--short', dest='short', action="store_true", help='Show only titles or line containing the search tags')
    exporting.add_argument('--tags', dest='tags', action="store_true", help='Returns a list of all tags and number of occurences')
    exporting.add_argument('--export', metavar='TYPE', dest='export', choices=plugins.BaseExporter.PLUGIN_NAMES, help='Export your journal. TYPE can be {}.'.format(plugins.BaseExporter.get_plugin_types_string()), default=False, const=None)
    exporting.add_argument('-o', metavar='OUTPUT', dest='output', help='Optionally specifies output file when using --export. If OUTPUT is a directory, exports each entry into an individual file instead.', default=False, const=None)
    exporting.add_argument('--import', metavar='TYPE', dest='import_', choices=plugins.BaseImporter.PLUGIN_NAMES, help='Import entries into your journal. TYPE can be {}, and it defaults to jrnl if nothing else is specified.'.format(plugins.BaseImporter.get_plugin_types_string()), default=False, const='jrnl', nargs='?')
    exporting.add_argument('-i', metavar='INPUT', dest='input', help='Optionally specifies input file when using --import.', default=False, const=None)
    exporting.add_argument('--encrypt', metavar='FILENAME', dest='encrypt', help='Encrypts your existing journal with a new password', nargs='?', default=False, const=None)
    exporting.add_argument('--decrypt', metavar='FILENAME', dest='decrypt', help='Decrypts your journal and stores it in plain text', nargs='?', default=False, const=None)
    exporting.add_argument('--edit', dest='edit', help='Opens your editor to edit the selected entries.', action="store_true")

    return parser.parse_args(args)


class CommandEnum:
    READ = 1
    COMPOSE_NEW_ENTRY = 2
    EDIT_EXISTING_ENTRY = 3 # Existing entries with external editor
    EXPORT = 4
    IMPORT = 5
    LS = 6
    VERSION = 7
    LIST_TAGS = 8
    ENCRYPT = 9
    DECRYPT = 10


def guess_command(args, config):
    """Guess what the user wants to do from the given arguments"""

    if args.version is not False:
        return CommandEnum.VERSION
    elif args.ls is not False:
        return CommandEnum.LS
    elif args.import_ is not False:
        return CommandEnum.IMPORT
    elif args.tags is not False:
        return CommandEnum.LIST_TAGS
    elif args.edit is not False:
        return CommandEnum.EDIT_EXISTING_ENTRY
    elif args.export is not False:
        return CommandEnum.EXPORT
    elif args.decrypt is not False:
        return CommandEnum.DECRYPT
    elif args.encrypt is not False:
        return CommandEnum.ENCRYPT
    elif any((args.start_date, args.end_date, args.on_date, args.limit, args.strict, args.starred, args.short)):
        # Any sign of displaying stuff?
        return CommandEnum.READ
    elif args.text and all(word[0] in config['tagsymbols'] for word in " ".join(args.text).split()):
        # No date and only tags?
        return CommandEnum.READ

    return CommandEnum.COMPOSE_NEW_ENTRY


def do_command_list_tags(journal_name, config, original_config, args):
    log.debug("Running command 'list_tags'")

    journal = Journal.open_journal(journal_name, config)
    filter_journal(journal, args)

    print(util.py2encode(plugins.get_exporter("tags").export(journal)))


def do_command_read(journal_name, config, original_config, args):
    log.debug("Running command 'read'")

    journal = Journal.open_journal(journal_name, config)
    filter_journal(journal, args)

    print(util.py2encode(journal.pprint(short=args.short)))


def do_command_new_entry(journal_name, config, original_config, args):
    log.debug("Running command 'write'")

    if args.text:
        raw = " ".join(args.text).strip()
    else:
        if "win32" in sys.platform:
            _exit_multiline_code = "on a blank line, press Ctrl+Z and then Enter"
        else:
            _exit_multiline_code = "press Ctrl+D"

        if not sys.stdin.closed and not sys.stdin.isatty():
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
            print("No text exit...")
            exit(0)

    if util.PY2 and type(raw) is not unicode:
        raw = raw.decode(sys.getfilesystemencoding())

    journal = Journal.open_journal(journal_name, config)
    log.debug('Appending raw line "%s" to journal "%s"', raw, journal_name)
    journal.new_entry(raw)
    util.prompt("[Entry added to {0} journal]".format(journal_name))
    journal.write()

def do_command_edit_existing_entry(journal_name, config, original_config, args):
    log.debug("Running command 'edit existing entry'")
    journal = Journal.open_journal(journal_name, config)

    if not config['editor']:
        util.prompt("[{1}ERROR{2}: You need to specify an editor in {0} to use the --edit function.]".format(install.CONFIG_FILE_PATH, ERROR_COLOR, RESET_COLOR))
        sys.exit(1)

    old_entries = journal.entries
    filter_journal(journal, args)
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
    journal.sort()
    journal.write()



def do_command_import(journal_name, config, original_config, args):
    log.debug("Running command 'import'")

    journal = Journal.open_journal(journal_name, config)

    plugins.get_importer(args.import_).import_(journal, args.input)


def do_command_export(journal_name, config, original_config, args):
    log.debug("Running command 'export'")

    journal = Journal.open_journal(journal_name, config)
    filter_journal(journal, args)

    exporter = plugins.get_exporter(args.export)
    print(exporter.export(journal, args.output))


def do_command_encrypt(journal_name, config, original_config, args):
    log.debug("Running command 'encrypt'")
    journal = Journal.open_journal(journal_name, config)

    encrypt(journal, filename=args.encrypt)
    # Not encrypting to a separate file: update config!
    if not args.encrypt:
        update_config(original_config, {"encrypt": True}, journal_name, force_local=True)
        install.save_config(original_config)


def do_command_decrypt(journal_name, config, original_config, args):
    log.debug("Running command 'decrypt'")
    journal = Journal.open_journal(journal_name, config)

    decrypt(journal, filename=args.decrypt)
    # Not decrypting to a separate file: update config!
    if not args.decrypt:
        update_config(original_config, {"encrypt": False}, journal_name, force_local=True)
        install.save_config(original_config)


action_for = {
    CommandEnum.LIST_TAGS: do_command_list_tags,
    CommandEnum.READ: do_command_read,
    CommandEnum.COMPOSE_NEW_ENTRY: do_command_new_entry,
    CommandEnum.EDIT_EXISTING_ENTRY: do_command_edit_existing_entry,
    CommandEnum.IMPORT: do_command_import,
    CommandEnum.EXPORT: do_command_export,
    CommandEnum.ENCRYPT: do_command_encrypt,
    CommandEnum.DECRYPT: do_command_decrypt,
}


def encrypt(journal, filename=None):
    """ Encrypt into new file. If filename is not set, we encrypt the journal file itself. """
    from . import EncryptedJournal

    journal.config['password'] = util.getpass("Enter new password: ")
    journal.config['encrypt'] = True

    new_journal = EncryptedJournal.EncryptedJournal(None, **journal.config)
    new_journal.entries = journal.entries
    new_journal.write(filename)

    if util.yesno("Do you want to store the password in your keychain?", default=True):
        util.set_keychain(journal.name, journal.config['password'])

    util.prompt("Journal encrypted to {0}.".format(filename or new_journal.config['journal']))


def decrypt(journal, filename=None):
    """ Decrypts into new file. If filename is not set, we encrypt the journal file itself. """
    journal.config['encrypt'] = False
    journal.config['password'] = ""

    new_journal = Journal.PlainJournal(filename, **journal.config)
    new_journal.entries = journal.entries
    new_journal.write(filename)
    util.prompt("Journal decrypted to {0}.".format(filename or new_journal.config['journal']))


def list_journals(config):
    """List the journals specified in the configuration file"""
    result = "Journals defined in {}\n".format(install.CONFIG_FILE_PATH)
    ml = min(max(len(k) for k in config['journals']), 20)
    for journal, cfg in config['journals'].items():
        result += " * {:{}} -> {}\n".format(journal, ml, cfg['journal'] if isinstance(cfg, dict) else cfg)
    return result


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


def configure_logger(debug=False):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(levelname)-8s %(name)-12s %(message)s'
    )
    logging.getLogger('parsedatetime').setLevel(logging.INFO)  # disable parsedatetime debug logging


def filter_journal(journal, args):
    log.debug("Performing filtering...")

    if args.on_date:
        args.start_date = args.end_date = args.on_date
    journal.filter(tags=args.text,
                   start_date=args.start_date, end_date=args.end_date,
                   strict=args.strict,
                   short=args.short,
                   starred=args.starred)
    journal.limit(args.limit)

def run(manual_args=None):
    args = parse_args(manual_args)
    configure_logger(args.debug)
    args.text = [p.decode('utf-8') if util.PY2 and not isinstance(p, unicode) else p for p in args.text]

    if args.version:
        version_str = "{0} version {1}".format(jrnl.__title__, jrnl.__version__)
        print(util.py2encode(version_str))
        sys.exit(0)

    config = install.load_or_install_jrnl()
    log.debug('Using configuration "%s"', config)
    original_config = config.copy()

    if args.ls:
        util.prnt(list_journals(config))
        sys.exit(0)

    # Guess journal name
    # If the first textual argument points to a journal file, use this!
    journal_name = args.text[0] if (args.text and args.text[0] in config['journals']) else 'default'
    if journal_name is not 'default':
        args.text = args.text[1:]
    elif "default" not in config['journals']:
        util.prompt("No default journal configured.")
        util.prompt(list_journals(config))
        sys.exit(1)
    log.debug('Using journal "%s"', journal_name)

    # Find limiter
    # If the first remaining argument looks like e.g. '-3', interpret that as a limiter
    if not args.limit and args.text and args.text[0].startswith("-"):
        try:
            args.limit = int(args.text[0].lstrip("-"))
            args.text = args.text[1:]
        except:
            pass

    # Guess and execute command
    command = guess_command(args, config)
    if command in action_for:
        action_for[command](journal_name, config, original_config, args)
    else:
        print("Unknown command number: " + command)
        exit(1)

    exit(0)
