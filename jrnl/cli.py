#!/usr/bin/env python

"""
    jrnl

    license: MIT, see LICENSE for more details.
"""

from .Journal import PlainJournal, open_journal
from .EncryptedJournal import EncryptedJournal
from . import util
from . import install
from . import plugins
from .util import ERROR_COLOR, RESET_COLOR, UserAbort
import jrnl
import argparse
import sys
import re
import logging

log = logging.getLogger(__name__)
logging.getLogger("keyring.backend").setLevel(logging.ERROR)


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        dest="version",
        action="store_true",
        help="prints version information and exits",
    )
    parser.add_argument(
        "-ls", dest="ls", action="store_true", help="displays accessible journals"
    )
    parser.add_argument(
        "-d", "--debug", dest="debug", action="store_true", help="execute in debug mode"
    )

    composing = parser.add_argument_group(
        "Composing",
        'To write an entry simply write it on the command line, e.g. "jrnl yesterday at 1pm: Went to the gym."',
    )
    composing.add_argument("text", metavar="", nargs="*")

    reading = parser.add_argument_group(
        "Reading",
        "Specifying either of these parameters will display posts of your journal",
    )
    reading.add_argument(
        "-from", dest="start_date", metavar="DATE", help="View entries after this date"
    )
    reading.add_argument(
        "-until",
        "-to",
        dest="end_date",
        metavar="DATE",
        help="View entries before this date",
    )
    reading.add_argument(
        "-contains", dest="contains", help="View entries containing a specific string"
    )
    reading.add_argument(
        "-on", dest="on_date", metavar="DATE", help="View entries on this date"
    )
    reading.add_argument(
        "-and",
        dest="strict",
        action="store_true",
        help="Filter by tags using AND (default: OR)",
    )
    reading.add_argument(
        "-starred",
        dest="starred",
        action="store_true",
        help="Show only starred entries",
    )
    reading.add_argument(
        "-n",
        dest="limit",
        default=None,
        metavar="N",
        help="Shows the last n entries matching the filter. '-n 3' and '-3' have the same effect.",
        nargs="?",
        type=int,
    )
    reading.add_argument(
        "-not",
        dest="excluded",
        nargs="+",
        default=[],
        metavar="E",
        help="Exclude entries with these tags",
    )

    exporting = parser.add_argument_group(
        "Export / Import", "Options for transmogrifying your journal"
    )
    exporting.add_argument(
        "-s",
        "--short",
        dest="short",
        action="store_true",
        help="Show only titles or line containing the search tags",
    )
    exporting.add_argument(
        "--tags",
        dest="tags",
        action="store_true",
        help="Returns a list of all tags and number of occurences",
    )
    exporting.add_argument(
        "--export",
        metavar="TYPE",
        dest="export",
        choices=plugins.EXPORT_FORMATS,
        help="Export your journal. TYPE can be {}.".format(
            plugins.util.oxford_list(plugins.EXPORT_FORMATS)
        ),
        default=False,
        const=None,
    )
    exporting.add_argument(
        "-o",
        metavar="OUTPUT",
        dest="output",
        help="Optionally specifies output file when using --export. If OUTPUT is a directory, exports each entry into an individual file instead.",
        default=False,
        const=None,
    )
    exporting.add_argument(
        "--import",
        metavar="TYPE",
        dest="import_",
        choices=plugins.IMPORT_FORMATS,
        help="Import entries into your journal. TYPE can be {}, and it defaults to jrnl if nothing else is specified.".format(
            plugins.util.oxford_list(plugins.IMPORT_FORMATS)
        ),
        default=False,
        const="jrnl",
        nargs="?",
    )
    exporting.add_argument(
        "-i",
        metavar="INPUT",
        dest="input",
        help="Optionally specifies input file when using --import.",
        default=False,
        const=None,
    )
    exporting.add_argument(
        "--encrypt",
        metavar="FILENAME",
        dest="encrypt",
        help="Encrypts your existing journal with a new password",
        nargs="?",
        default=False,
        const=None,
    )
    exporting.add_argument(
        "--decrypt",
        metavar="FILENAME",
        dest="decrypt",
        help="Decrypts your journal and stores it in plain text",
        nargs="?",
        default=False,
        const=None,
    )
    exporting.add_argument(
        "--edit",
        dest="edit",
        help="Opens your editor to edit the selected entries.",
        action="store_true",
    )

    # Handle '-123' as a shortcut for '-n 123'
    num = re.compile(r"^-(\d+)$")
    if args is None:
        args = sys.argv[1:]
    return parser.parse_args([num.sub(r"-n \1", a) for a in args])


def guess_mode(args, config):
    """Guesses the mode (compose, read or export) from the given arguments"""
    compose = True
    export = False
    import_ = False
    if args.import_ is not False:
        compose = False
        export = False
        import_ = True
    elif (
        args.decrypt is not False
        or args.encrypt is not False
        or args.export is not False
        or any((args.short, args.tags, args.edit))
    ):
        compose = False
        export = True
    elif any(
        (
            args.start_date,
            args.end_date,
            args.on_date,
            args.limit,
            args.strict,
            args.starred,
            args.contains,
        )
    ):
        # Any sign of displaying stuff?
        compose = False
    elif args.text and all(
        word[0] in config["tagsymbols"] for word in " ".join(args.text).split()
    ):
        # No date and only tags?
        compose = False

    return compose, export, import_


def encrypt(journal, filename=None):
    """ Encrypt into new file. If filename is not set, we encrypt the journal file itself. """
    journal.config["encrypt"] = True

    new_journal = EncryptedJournal.from_journal(journal)
    new_journal.write(filename)

    print(
        "Journal encrypted to {}.".format(filename or new_journal.config["journal"]),
        file=sys.stderr,
    )


def decrypt(journal, filename=None):
    """ Decrypts into new file. If filename is not set, we encrypt the journal file itself. """
    journal.config["encrypt"] = False

    new_journal = PlainJournal.from_journal(journal)
    new_journal.write(filename)
    print(
        "Journal decrypted to {}.".format(filename or new_journal.config["journal"]),
        file=sys.stderr,
    )


def list_journals(config):
    """List the journals specified in the configuration file"""
    result = f"Journals defined in {install.CONFIG_FILE_PATH}\n"
    ml = min(max(len(k) for k in config["journals"]), 20)
    for journal, cfg in config["journals"].items():
        result += " * {:{}} -> {}\n".format(
            journal, ml, cfg["journal"] if isinstance(cfg, dict) else cfg
        )
    return result


def update_config(config, new_config, scope, force_local=False):
    """Updates a config dict with new values - either global if scope is None
    or config['journals'][scope] is just a string pointing to a journal file,
    or within the scope"""
    if scope and type(config["journals"][scope]) is dict:  # Update to journal specific
        config["journals"][scope].update(new_config)
    elif scope and force_local:  # Convert to dict
        config["journals"][scope] = {"journal": config["journals"][scope]}
        config["journals"][scope].update(new_config)
    else:
        config.update(new_config)


def configure_logger(debug=False):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(levelname)-8s %(name)-12s %(message)s",
    )
    logging.getLogger("parsedatetime").setLevel(
        logging.INFO
    )  # disable parsedatetime debug logging


def run(manual_args=None):
    args = parse_args(manual_args)
    configure_logger(args.debug)
    if args.version:
        version_str = f"{jrnl.__title__} version {jrnl.__version__}"
        print(version_str)
        sys.exit(0)

    try:
        config = install.load_or_install_jrnl()
    except UserAbort as err:
        print(f"\n{err}", file=sys.stderr)
        sys.exit(1)

    if args.ls:
        print(list_journals(config))
        sys.exit(0)

    log.debug('Using configuration "%s"', config)
    original_config = config.copy()

    # If the first textual argument points to a journal file,
    # use this!

    journal_name = install.DEFAULT_JOURNAL_KEY
    if args.text and args.text[0] in config["journals"]:
        journal_name = args.text[0]
        args.text = args.text[1:]
    elif install.DEFAULT_JOURNAL_KEY not in config["journals"]:
        print("No default journal configured.", file=sys.stderr)
        print(list_journals(config), file=sys.stderr)
        sys.exit(1)

    config = util.scope_config(config, journal_name)

    log.debug('Using journal "%s"', journal_name)
    mode_compose, mode_export, mode_import = guess_mode(args, config)

    # How to quit writing?
    if "win32" in sys.platform:
        _exit_multiline_code = "on a blank line, press Ctrl+Z and then Enter"
    else:
        _exit_multiline_code = "press Ctrl+D"

    if mode_compose and not args.text:
        if not sys.stdin.isatty():
            # Piping data into jrnl
            raw = sys.stdin.read()
        elif config["editor"]:
            template = ""
            if config["template"]:
                try:
                    template = open(config["template"]).read()
                except OSError:
                    print(
                        f"[Could not read template at '{config['template']}']",
                        file=sys.stderr,
                    )
                    sys.exit(1)
            raw = util.get_text_from_editor(config, template)
        else:
            try:
                print(
                    "[Compose Entry; " + _exit_multiline_code + " to finish writing]\n",
                    file=sys.stderr,
                )
                raw = sys.stdin.read()
            except KeyboardInterrupt:
                print("[Entry NOT saved to journal.]", file=sys.stderr)
                sys.exit(0)
        if raw:
            args.text = [raw]
        else:
            sys.exit()

    # This is where we finally open the journal!
    try:
        journal = open_journal(journal_name, config)
    except KeyboardInterrupt:
        print(f"[Interrupted while opening journal]", file=sys.stderr)
        sys.exit(1)

    # Import mode
    if mode_import:
        plugins.get_importer(args.import_).import_(journal, args.input)

    # Writing mode
    elif mode_compose:
        raw = " ".join(args.text).strip()
        log.debug('Appending raw line "%s" to journal "%s"', raw, journal_name)
        journal.new_entry(raw)
        print(f"[Entry added to {journal_name} journal]", file=sys.stderr)
        journal.write()

    if not mode_compose:
        old_entries = journal.entries
        if args.on_date:
            args.start_date = args.end_date = args.on_date
        journal.filter(
            tags=args.text,
            start_date=args.start_date,
            end_date=args.end_date,
            strict=args.strict,
            short=args.short,
            starred=args.starred,
            exclude=args.excluded,
            contains=args.contains,
        )
        journal.limit(args.limit)

    # Reading mode
    if not mode_compose and not mode_export and not mode_import:
        print(journal.pprint())

    # Various export modes
    elif args.short:
        print(journal.pprint(short=True))

    elif args.tags:
        print(plugins.get_exporter("tags").export(journal))

    elif args.export is not False:
        exporter = plugins.get_exporter(args.export)
        print(exporter.export(journal, args.output))

    elif args.encrypt is not False:
        encrypt(journal, filename=args.encrypt)
        # Not encrypting to a separate file: update config!
        if not args.encrypt:
            update_config(
                original_config, {"encrypt": True}, journal_name, force_local=True
            )
            install.save_config(original_config)

    elif args.decrypt is not False:
        decrypt(journal, filename=args.decrypt)
        # Not decrypting to a separate file: update config!
        if not args.decrypt:
            update_config(
                original_config, {"encrypt": False}, journal_name, force_local=True
            )
            install.save_config(original_config)

    elif args.edit:
        if not config["editor"]:
            print(
                "[{1}ERROR{2}: You need to specify an editor in {0} to use the --edit function.]".format(
                    install.CONFIG_FILE_PATH, ERROR_COLOR, RESET_COLOR
                ),
                file=sys.stderr,
            )
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
            prompts.append(
                "{} {} deleted".format(
                    num_deleted, "entry" if num_deleted == 1 else "entries"
                )
            )
        if num_edited:
            prompts.append(
                "{} {} modified".format(
                    num_edited, "entry" if num_deleted == 1 else "entries"
                )
            )
        if prompts:
            print("[{}]".format(", ".join(prompts).capitalize()), file=sys.stderr)
        journal.entries += other_entries
        journal.sort()
        journal.write()
