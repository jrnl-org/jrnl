# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
import sys

from . import install
from . import plugins
from .Journal import open_journal
from .color import ERROR_COLOR
from .color import RESET_COLOR
from .config import get_journal_name
from .config import scope_config
from .config import get_config_path
from .editor import get_text_from_editor
from .editor import get_text_from_stdin
from .exception import UserAbort
from . import time
from .override import apply_overrides


def run(args):
    """
    Flow:
    1. Run standalone command if it doesn't require config (help, version, etc), then exit
    2. Load config
    3. Run standalone command if it does require config (encrypt, decrypt, etc), then exit
    4. Load specified journal
    5. Start write mode, or search mode
    6. Profit
    """

    # Run command if possible before config is available
    if callable(args.preconfig_cmd):
        return args.preconfig_cmd(args)

    # Load the config, and extract journal name
    try:
        config = install.load_or_install_jrnl()
        original_config = config.copy()

        # Apply config overrides
        overrides = args.config_override
        if overrides:
            config = apply_overrides(overrides, config)

        args = get_journal_name(args, config)
        config = scope_config(config, args.journal_name)
    except UserAbort as err:
        print(f"\n{err}", file=sys.stderr)
        sys.exit(1)

    # Run post-config command now that config is ready
    if callable(args.postconfig_cmd):
        return args.postconfig_cmd(
            args=args, config=config, original_config=original_config
        )

    # --- All the standalone commands are now done --- #

    # Get the journal we're going to be working with
    journal = open_journal(args.journal_name, config)

    kwargs = {
        "args": args,
        "config": config,
        "journal": journal,
    }

    if _is_write_mode(**kwargs):
        write_mode(**kwargs)
    else:
        search_mode(**kwargs)


def _is_write_mode(args, config, **kwargs):
    """Determines if we are in write mode (as opposed to search mode)"""
    write_mode = True

    # Are any search filters present? If so, then search mode.
    write_mode = not any(
        (
            args.contains,
            args.delete,
            args.edit,
            args.export,
            args.end_date,
            args.today_in_history,
            args.month,
            args.day,
            args.year,
            args.limit,
            args.on_date,
            args.short,
            args.starred,
            args.start_date,
            args.strict,
            args.tags,
        )
    )

    # Might be writing and want to move to editor part of the way through
    if args.edit and args.text:
        write_mode = True

    # If the text is entirely tags, then we are also searching (not writing)
    if (
        write_mode
        and args.text
        and all(word[0] in config["tagsymbols"] for word in " ".join(args.text).split())
    ):
        write_mode = False

    return write_mode


def write_mode(args, config, journal, **kwargs):
    """
    Gets input from the user to write to the journal
    1. Check for input from cli
    2. Check input being piped in
    3. Open editor if configured (prepopulated with template if available)
    4. Use stdin.read as last resort
    6. Write any found text to journal, or exit
    """
    logging.debug("Write mode: starting")

    if args.text:
        logging.debug("Write mode: cli text detected: %s", args.text)
        raw = " ".join(args.text).strip()
        if args.edit:
            raw = _write_in_editor(config, raw)

    elif not sys.stdin.isatty():
        logging.debug("Write mode: receiving piped text")
        raw = sys.stdin.read()

    else:
        raw = _write_in_editor(config)

    if not raw:
        logging.error("Write mode: couldn't get raw text")
        sys.exit()

    logging.debug(
        'Write mode: appending raw text to journal "%s": %s', args.journal_name, raw
    )
    journal.new_entry(raw)
    print(f"[Entry added to {args.journal_name} journal]", file=sys.stderr)
    journal.write()
    logging.debug("Write mode: completed journal.write()", args.journal_name, raw)


def search_mode(args, journal, **kwargs):
    """
    Search for entries in a journal, then either:
    1. Send them to configured editor for user manipulation
    2. Delete them (with confirmation for each entry)
    3. Display them (with formatting options)
    """
    kwargs = {
        **kwargs,
        "args": args,
        "journal": journal,
        "old_entries": journal.entries,
    }

    # Filters the journal entries in place
    _search_journal(**kwargs)

    # Where do the search results go?
    if args.edit:
        _edit_search_results(**kwargs)

    elif args.delete:
        _delete_search_results(**kwargs)

    else:
        _display_search_results(**kwargs)


def _write_in_editor(config, template=None):
    if config["editor"]:
        logging.debug("Write mode: opening editor")
        if not template:
            template = _get_editor_template(config)
        raw = get_text_from_editor(config, template)

    else:
        raw = get_text_from_stdin()

    return raw


def _get_editor_template(config, **kwargs):
    logging.debug("Write mode: loading template for entry")

    if not config["template"]:
        logging.debug("Write mode: no template configured")
        return ""

    try:
        template = open(config["template"]).read()
        logging.debug("Write mode: template loaded: %s", template)
    except OSError:
        logging.error("Write mode: template not loaded")
        print(
            f"[Could not read template at '{config['template']}']",
            file=sys.stderr,
        )
        sys.exit(1)

    return template


def _search_journal(args, journal, **kwargs):
    """Search the journal with the given args"""
    if args.on_date:
        args.start_date = args.end_date = args.on_date

    if args.today_in_history:
        now = time.parse("now")
        args.day = now.day
        args.month = now.month

    journal.filter(
        tags=args.text,
        month=args.month,
        day=args.day,
        year=args.year,
        start_date=args.start_date,
        end_date=args.end_date,
        strict=args.strict,
        starred=args.starred,
        exclude=args.excluded,
        contains=args.contains,
    )
    journal.limit(args.limit)


def _edit_search_results(config, journal, old_entries, **kwargs):
    """
    1. Send the given journal entries to the user-configured editor
    2. Print out stats on any modifications to journal
    3. Write modifications to journal
    """
    if not config["editor"]:
        print(
            f"""
            [{ERROR_COLOR}ERROR{RESET_COLOR}: There is no editor configured.]

            Please specify an editor in config file ({get_config_path()})
            to use the --edit option.
            """,
            file=sys.stderr,
        )
        sys.exit(1)

    # separate entries we are not editing
    other_entries = [e for e in old_entries if e not in journal.entries]

    # Get stats now for summary later
    old_stats = _get_predit_stats(journal)

    # Send user to the editor
    edited = get_text_from_editor(config, journal.editable_str())
    journal.parse_editable_str(edited)

    # Print summary if available
    _print_edited_summary(journal, old_stats)

    # Put back entries we separated earlier, sort, and write the journal
    journal.entries += other_entries
    journal.sort()
    journal.write()


def _print_edited_summary(journal, old_stats, **kwargs):
    stats = {
        "deleted": old_stats["count"] - len(journal),
        "modified": len([e for e in journal.entries if e.modified]),
    }

    prompts = []

    if stats["deleted"]:
        prompts.append(
            f"{stats['deleted']} {_pluralize_entry(stats['deleted'])} deleted"
        )

    if stats["modified"]:
        prompts.append(
            f"{stats['modified']} {_pluralize_entry(stats['modified'])} modified"
        )

    if prompts:
        print(f"[{', '.join(prompts).capitalize()}]", file=sys.stderr)


def _get_predit_stats(journal):
    return {"count": len(journal)}


def _pluralize_entry(num):
    return "entry" if num == 1 else "entries"


def _delete_search_results(journal, old_entries, **kwargs):
    if not journal.entries:
        print(
            "[No entries deleted, because the search returned no results.]",
            file=sys.stderr,
        )
        sys.exit(1)

    entries_to_delete = journal.prompt_delete_entries()

    if entries_to_delete:
        journal.entries = old_entries
        journal.delete_entries(entries_to_delete)

        journal.write()


def _display_search_results(args, journal, **kwargs):
    if args.short or args.export == "short":
        print(journal.pprint(short=True))

    elif args.export == "pretty":
        print(journal.pprint())

    elif args.tags:
        print(plugins.get_exporter("tags").export(journal))

    elif args.export:
        exporter = plugins.get_exporter(args.export)
        print(exporter.export(journal, args.filename))
    elif kwargs["config"].get("display_format"):
        exporter = plugins.get_exporter(kwargs["config"]["display_format"])
        print(exporter.export(journal, args.filename))
    else:
        print(journal.pprint())
