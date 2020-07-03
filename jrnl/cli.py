#!/usr/bin/env python

"""
    jrnl

    license: GPLv3, see LICENSE.md for more details.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
import packaging.version
import platform
import sys

from . import install, plugins, util
from .util import list_journals
from .parsing import parse_args_before_config
from .Journal import PlainJournal, open_journal
from .util import WARNING_COLOR, ERROR_COLOR, RESET_COLOR, UserAbort

log = logging.getLogger(__name__)
logging.getLogger("keyring.backend").setLevel(logging.ERROR)


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
        or any((args.short, args.tags, args.edit, args.delete))
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
    from .EncryptedJournal import EncryptedJournal

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
        level=logging.DEBUG if debug else logging.ERROR,
        format="%(levelname)-8s %(name)-12s %(message)s",
    )
    logging.getLogger("parsedatetime").setLevel(
        logging.INFO
    )  # disable parsedatetime debug logging


def run(manual_args=None):
    if packaging.version.parse(platform.python_version()) < packaging.version.parse(
        "3.7"
    ):
        print(
            f"""{WARNING_COLOR}
WARNING: Python versions below 3.7 will no longer be supported as of jrnl v2.5
(the next release). You are currently on Python {platform.python_version()}. Please update to
Python 3.7 (or higher) soon.
{RESET_COLOR}""",
            file=sys.stderr,
        )

    if manual_args is None:
        manual_args = sys.argv[1:]

    args = parse_args_before_config(manual_args)

    # import pprint
    # pp = pprint.PrettyPrinter(depth=4)
    # pp.pprint(args)

    configure_logger(args.debug)

    # Run command if possible before config is available
    if callable(args.preconfig_cmd):
        args.preconfig_cmd(args)
        sys.exit(0)

    # Load the config
    try:
        config = install.load_or_install_jrnl()
    except UserAbort as err:
        print(f"\n{err}", file=sys.stderr)
        sys.exit(1)

    # Run command now that config is available
    if callable(args.postconfig_cmd):
        args.postconfig_cmd(config=config, args=args)
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

    # This is where we finally open the journal!
    try:
        journal = open_journal(journal_name, config)
    except KeyboardInterrupt:
        print("[Interrupted while opening journal]", file=sys.stderr)
        sys.exit(1)

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

    elif args.delete:
        if journal.entries:
            entries_to_delete = journal.prompt_delete_entries()

            if entries_to_delete:
                journal.entries = old_entries
                journal.delete_entries(entries_to_delete)

                journal.write()
        else:
            print(
                "No entries deleted, because the search returned no results.",
                file=sys.stderr,
            )
