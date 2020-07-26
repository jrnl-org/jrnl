import logging
import sys

from . import util
from . import install
from . import plugins

from .util import ERROR_COLOR
from .util import RESET_COLOR

log = logging.getLogger(__name__)


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
            args.limit,
            args.on_date,
            args.short,
            args.starred,
            args.start_date,
            args.strict,
            args.tags,
        )
    )

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
    log.debug("Write mode: starting")

    if args.text:
        log.debug("Write mode: cli text detected: %s", args.text)
        raw = " ".join(args.text).strip()

    elif not sys.stdin.isatty():
        log.debug("Write mode: receiving piped text")
        raw = sys.stdin.read()

    else:
        raw = _write_in_editor(config)

    if not raw:
        log.error("Write mode: couldn't get raw text")
        sys.exit()

    log.debug(
        'Write mode: appending raw text to journal "%s": %s', args.journal_name, raw
    )
    journal.new_entry(raw)
    print(f"[Entry added to {args.journal_name} journal]", file=sys.stderr)
    journal.write()
    log.debug("Write mode: completed journal.write()", args.journal_name, raw)


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


def _write_in_editor(config):
    if config["editor"]:
        log.debug("Write mode: opening editor")
        template = _get_editor_template(config)
        raw = util.get_text_from_editor(config, template)

    else:
        _how_to_quit = "Ctrl+z and then Enter" if "win32" in sys.platform else "Ctrl+d"
        print(
            f"[Writing Entry; on a blank line, press {_how_to_quit} to finish writing]\n",
            file=sys.stderr,
        )
        try:
            raw = sys.stdin.read()
        except KeyboardInterrupt:
            log.error("Write mode: keyboard interrupt")
            print("[Entry NOT saved to journal]", file=sys.stderr)
            sys.exit(0)

    return raw


def _get_editor_template(config, **kwargs):
    log.debug("Write mode: loading template for entry")

    if not config["template"]:
        log.debug("Write mode: no template configured")
        return ""

    try:
        template = open(config["template"]).read()
        log.debug("Write mode: template loaded: %s", template)
    except OSError:
        log.error("Write mode: template not loaded")
        print(
            f"[Could not read template at '{config['template']}']", file=sys.stderr,
        )
        sys.exit(1)

    return template


def _search_journal(args, journal, **kwargs):
    """ Search the journal with the given args"""
    if args.on_date:
        args.start_date = args.end_date = args.on_date

    journal.filter(
        tags=args.text,
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

            Please specify an editor in config file ({install.CONFIG_FILE_PATH})
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
    edited = util.get_text_from_editor(config, journal.editable_str())
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
    if args.short:
        print(journal.pprint(short=True))

    elif args.tags:
        print(plugins.get_exporter("tags").export(journal))

    elif args.export:
        exporter = plugins.get_exporter(args.export)
        print(exporter.export(journal, args.filename))

    else:
        # Default display mode
        print(journal.pprint())
