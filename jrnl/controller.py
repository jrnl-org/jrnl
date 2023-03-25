# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
import sys
from typing import TYPE_CHECKING

from jrnl import install
from jrnl import plugins
from jrnl import time
from jrnl.config import DEFAULT_JOURNAL_KEY
from jrnl.config import get_config_path
from jrnl.config import get_journal_name
from jrnl.config import get_templates_path
from jrnl.config import scope_config
from jrnl.editor import get_text_from_editor
from jrnl.editor import get_text_from_stdin
from jrnl.exception import JrnlException
from jrnl.journals import open_journal
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg
from jrnl.output import print_msgs
from jrnl.override import apply_overrides
from jrnl.path import absolute_path

if TYPE_CHECKING:
    from argparse import Namespace

    from jrnl.journals import Entry
    from jrnl.journals import Journal


def run(args: "Namespace"):
    """
    Flow:
    1. Run standalone command if it doesn't require config (help, version, etc), then exit
    2. Load config
    3. Run standalone command if it does require config (encrypt, decrypt, etc), then exit
    4. Load specified journal
    5. Start append mode, or search mode
    6. Perform actions with results from search mode (if needed)
    7. Profit
    """

    # Run command if possible before config is available
    if callable(args.preconfig_cmd):
        return args.preconfig_cmd(args)

    # Load the config, and extract journal name
    config = install.load_or_install_jrnl(args.config_file_path)
    original_config = config.copy()

    # Apply config overrides
    config = apply_overrides(args, config)

    args = get_journal_name(args, config)
    config = scope_config(config, args.journal_name)

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
        "old_entries": journal.entries,
    }

    if _is_append_mode(**kwargs):
        append_mode(**kwargs)
        return

    # If not append mode, then we're in search mode (only 2 modes exist)
    search_mode(**kwargs)
    entries_found_count = len(journal)
    _print_entries_found_count(entries_found_count, args)

    # Actions
    _perform_actions_on_search_results(**kwargs)

    if entries_found_count != 0 and _has_action_args(args):
        _print_changed_counts(journal)
    else:
        # display only occurs if no other action occurs
        _display_search_results(**kwargs)


def _perform_actions_on_search_results(**kwargs):
    args = kwargs["args"]

    # Perform actions (if needed)
    if args.change_time:
        _change_time_search_results(**kwargs)

    if args.delete:
        _delete_search_results(**kwargs)

    # open results in editor (if `--edit` was used)
    if args.edit:
        _edit_search_results(**kwargs)


def _is_append_mode(args: "Namespace", config: dict, **kwargs) -> bool:
    """Determines if we are in append mode (as opposed to search mode)"""
    # Are any search filters present? If so, then search mode.
    append_mode = (
        not _has_search_args(args)
        and not _has_action_args(args)
        and not _has_display_args(args)
    )

    # Might be writing and want to move to editor part of the way through
    if args.edit and args.text:
        append_mode = True

    # If the text is entirely tags, then we are also searching (not writing)
    if append_mode and args.text and _has_only_tags(config["tagsymbols"], args.text):
        append_mode = False

    return append_mode


def _read_template_file(template_arg: str, template_path_from_config: str) -> str:
    """
    This function is called when either a template file is passed with --template, or config.template is set.

    The processing logic is:
        If --template was not used: Load the global template file.
        If --template was used:
            * Check $XDG_DATA_HOME/jrnl/templates/template_arg.
            * Check template_arg as an absolute / relative path.

        If a file is found, its contents are returned as a string.
        If not, a JrnlException is raised.
    """
    logging.debug(
        "Append mode: Either a template arg was passed, or the global config is set."
    )

    # If filename is unset, we are in this flow due to a global template being configured
    if not template_arg:
        logging.debug("Append mode: Global template configuration detected.")
        global_template_path = absolute_path(template_path_from_config)
        try:
            with open(global_template_path, encoding="utf-8") as f:
                template_data = f.read()
                return template_data
        except FileNotFoundError:
            raise JrnlException(
                Message(
                    MsgText.CantReadTemplateGlobalConfig,
                    MsgStyle.ERROR,
                    {
                        "global_template_path": global_template_path,
                    },
                )
            )
    else:  # A template CLI arg was passed.
        logging.debug("Trying to load template from $XDG_DATA_HOME/jrnl/templates/")
        jrnl_template_dir = get_templates_path()
        logging.debug(f"Append mode: jrnl templates directory: {jrnl_template_dir}")
        template_path = jrnl_template_dir / template_arg
        try:
            with open(template_path, encoding="utf-8") as f:
                template_data = f.read()
                return template_data
        except FileNotFoundError:
            logging.debug(
                f"Couldn't open {template_path}. Treating --template argument like a local / abs path."
            )
            pass

        normalized_template_arg_filepath = absolute_path(template_arg)
        try:
            with open(normalized_template_arg_filepath, encoding="utf-8") as f:
                template_data = f.read()
                return template_data
        except FileNotFoundError:
            raise JrnlException(
                Message(
                    MsgText.CantReadTemplateCLIArg,
                    MsgStyle.ERROR,
                    {
                        "normalized_template_arg_filepath": normalized_template_arg_filepath,
                        "jrnl_template_dir": template_path,
                    },
                )
            )


def append_mode(args: "Namespace", config: dict, journal: "Journal", **kwargs) -> None:
    """
    Gets input from the user to write to the journal
    0. Check for a template passed as an argument, or in the global config
    1. Check for input from cli
    2. Check input being piped in
    3. Open editor if configured (prepopulated with template if available)
    4. Use stdin.read as last resort
    6. Write any found text to journal, or exit
    """
    logging.debug("Append mode: starting")

    if args.template or config["template"]:
        logging.debug(f"Append mode: template CLI arg detected: {args.template}")
        # Read template file and pass as raw text into the composer
        template_data = _read_template_file(args.template, config["template"])
        raw = _write_in_editor(config, template_data)
        if raw == template_data:
            logging.error("Append mode: raw text was the same as the template")
            raise JrnlException(Message(MsgText.NoChangesToTemplate, MsgStyle.NORMAL))
    elif args.text:
        logging.debug(f"Append mode: cli text detected: {args.text}")
        raw = " ".join(args.text).strip()
        if args.edit:
            raw = _write_in_editor(config, raw)

    elif not sys.stdin.isatty():
        logging.debug("Append mode: receiving piped text")
        raw = sys.stdin.read()

    else:
        raw = _write_in_editor(config)

    if not raw or raw.isspace():
        logging.error("Append mode: couldn't get raw text or entry was empty")
        raise JrnlException(Message(MsgText.NoTextReceived, MsgStyle.NORMAL))

    logging.debug(
        f"Append mode: appending raw text to journal '{args.journal_name}': {raw}"
    )
    journal.new_entry(raw)
    if args.journal_name != DEFAULT_JOURNAL_KEY:
        print_msg(
            Message(
                MsgText.JournalEntryAdded,
                MsgStyle.NORMAL,
                {"journal_name": args.journal_name},
            )
        )
    journal.write()
    logging.debug("Append mode: completed journal.write()")


def search_mode(args: "Namespace", journal: "Journal", **kwargs) -> None:
    """
    Search for entries in a journal, and return the
    results. If no search args, then return all results
    """
    logging.debug("Search mode: starting")

    # If no search args, then return all results (don't filter anything)
    if not _has_search_args(args) and not _has_display_args(args) and not args.text:
        logging.debug("Search mode: has no search args")
        return

    logging.debug("Search mode: has search args")
    _filter_journal_entries(args, journal)


def _write_in_editor(config: dict, prepopulated_text: str | None = None) -> str:
    if config["editor"]:
        logging.debug("Append mode: opening editor")
        raw = get_text_from_editor(config, prepopulated_text)
    else:
        raw = get_text_from_stdin()

    return raw


def _filter_journal_entries(args: "Namespace", journal: "Journal", **kwargs) -> None:
    """Filter journal entries in-place based upon search args"""
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
        tagged=args.tagged,
        exclude=args.excluded,
        exclude_starred=args.exclude_starred,
        exclude_tagged=args.exclude_tagged,
        contains=args.contains,
    )
    journal.limit(args.limit)


def _print_entries_found_count(count: int, args: "Namespace") -> None:
    logging.debug(f"count: {count}")
    if count == 0:
        if args.edit or args.change_time:
            print_msg(Message(MsgText.NothingToModify, MsgStyle.WARNING))
        elif args.delete:
            print_msg(Message(MsgText.NothingToDelete, MsgStyle.WARNING))
        else:
            print_msg(Message(MsgText.NoEntriesFound, MsgStyle.NORMAL))
        return
    elif args.limit and args.limit == count:
        # Don't show count if the user expects a limited number of results
        logging.debug("args.limit is true-ish")
        return

    logging.debug("Printing general summary")
    my_msg = (
        MsgText.EntryFoundCountSingular if count == 1 else MsgText.EntryFoundCountPlural
    )
    print_msg(Message(my_msg, MsgStyle.NORMAL, {"num": count}))


def _other_entries(journal: "Journal", entries: list["Entry"]) -> list["Entry"]:
    """Find entries that are not in journal"""
    return [e for e in entries if e not in journal.entries]


def _edit_search_results(
    config: dict, journal: "Journal", old_entries: list["Entry"], **kwargs
) -> None:
    """
    1. Send the given journal entries to the user-configured editor
    2. Print out stats on any modifications to journal
    3. Write modifications to journal
    """
    if not config["editor"]:
        raise JrnlException(
            Message(
                MsgText.EditorNotConfigured,
                MsgStyle.ERROR,
                {"config_file": get_config_path()},
            )
        )

    # separate entries we are not editing
    other_entries = _other_entries(journal, old_entries)

    # Send user to the editor
    try:
        edited = get_text_from_editor(config, journal.editable_str())
    except JrnlException as e:
        if e.has_message_text(MsgText.NoTextReceived):
            raise JrnlException(
                Message(MsgText.NoEditsReceivedJournalNotDeleted, MsgStyle.WARNING)
            )
        else:
            raise e

    journal.parse_editable_str(edited)

    # Put back entries we separated earlier, sort, and write the journal
    journal.entries += other_entries
    journal.sort()
    journal.write()


def _print_changed_counts(journal: "Journal", **kwargs) -> None:
    stats = journal.get_change_counts()
    msgs = []

    if stats["added"] > 0:
        my_msg = (
            MsgText.JournalCountAddedSingular
            if stats["added"] == 1
            else MsgText.JournalCountAddedPlural
        )
        msgs.append(Message(my_msg, MsgStyle.NORMAL, {"num": stats["added"]}))

    if stats["deleted"] > 0:
        my_msg = (
            MsgText.JournalCountDeletedSingular
            if stats["deleted"] == 1
            else MsgText.JournalCountDeletedPlural
        )
        msgs.append(Message(my_msg, MsgStyle.NORMAL, {"num": stats["deleted"]}))

    if stats["modified"] > 0:
        my_msg = (
            MsgText.JournalCountModifiedSingular
            if stats["modified"] == 1
            else MsgText.JournalCountModifiedPlural
        )
        msgs.append(Message(my_msg, MsgStyle.NORMAL, {"num": stats["modified"]}))

    if not msgs:
        msgs.append(Message(MsgText.NoEditsReceived, MsgStyle.NORMAL))

    print_msgs(msgs)


def _get_predit_stats(journal: "Journal") -> dict[str, int]:
    return {"count": len(journal)}


def _delete_search_results(
    journal: "Journal", old_entries: list["Entry"], **kwargs
) -> None:
    entries_to_delete = journal.prompt_action_entries(MsgText.DeleteEntryQuestion)

    journal.entries = old_entries

    if entries_to_delete:
        journal.delete_entries(entries_to_delete)

        journal.write()


def _change_time_search_results(
    args: "Namespace",
    journal: "Journal",
    old_entries: list["Entry"],
    no_prompt: bool = False,
    **kwargs,
) -> None:
    # separate entries we are not editing
    # @todo if there's only 1, don't prompt
    entries_to_change = journal.prompt_action_entries(MsgText.ChangeTimeEntryQuestion)

    if entries_to_change:
        date = time.parse(args.change_time)
        journal.entries = old_entries
        journal.change_date_entries(date, entries_to_change)

        journal.write()


def _display_search_results(args: "Namespace", journal: "Journal", **kwargs) -> None:
    if len(journal) == 0:
        return

    # Get export format from config file if not provided at the command line
    args.export = args.export or kwargs["config"].get("display_format")

    if args.tags:
        print(plugins.get_exporter("tags").export(journal))

    elif args.short or args.export == "short":
        print(journal.pprint(short=True))

    elif args.export == "pretty":
        print(journal.pprint())

    elif args.export:
        exporter = plugins.get_exporter(args.export)
        print(exporter.export(journal, args.filename))
    else:
        print(journal.pprint())


def _has_search_args(args: "Namespace") -> bool:
    """Looking for arguments that filter a journal"""
    return any(
        (
            args.contains,
            args.tagged,
            args.excluded,
            args.exclude_starred,
            args.exclude_tagged,
            args.end_date,
            args.today_in_history,
            args.month,
            args.day,
            args.year,
            args.limit,
            args.on_date,
            args.starred,
            args.start_date,
            args.strict,  # -and
        )
    )


def _has_action_args(args: "Namespace") -> bool:
    return any(
        (
            args.change_time,
            args.delete,
            args.edit,
        )
    )


def _has_display_args(args: "Namespace") -> bool:
    return any(
        (
            args.tags,
            args.short,
            args.export,  # --format
        )
    )


def _has_only_tags(tag_symbols: str, args_text: str) -> bool:
    return all(word[0] in tag_symbols for word in " ".join(args_text).split())
