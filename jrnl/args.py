# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import argparse
import re
import textwrap

from .commands import postconfig_decrypt
from .commands import postconfig_encrypt
from .commands import postconfig_import
from .commands import postconfig_list
from .commands import preconfig_diagnostic
from .commands import preconfig_version
from .output import deprecated_cmd
from .plugins import EXPORT_FORMATS
from .plugins import IMPORT_FORMATS
from .plugins import util


def deserialize_config_args(input: str) -> dict:
    """Convert a delimited list of configuration key-value pairs into a flat dict

    Example:
    An input of
        `colors.title: blue, display_format: json, colors.date: green`
    will return
        ```json
        {
            'colors.title': 'blue',
            'display_format': 'json',
            'colors.date': 'green'
        }
        ```

    Args:
        input (str): list of configuration keys in dot-notation and their respective values.

    Returns:
        dict: A single level dict of the configuration keys in dot-notation and their respective desired values
    """
    slug_delimiter = ","
    key_value_separator = ":"
    _kvpairs = _split_at_delimiter(
        input, slug_delimiter, " "
    )  # Strip away all whitespace in input, not just leading
    runtime_modifications = {}
    for _p in _kvpairs:
        l, r = _split_at_delimiter(_p, key_value_separator)
        r = r.strip()
        if r.isdigit():
            r = int(r)
        elif r.lower() == "true":
            r = True
        elif r.lower() == "false":
            r = False
        runtime_modifications[l] = r
    return runtime_modifications


def _split_at_delimiter(
    input: str, slug_delimiter: str, whitespace_to_strip=None
) -> list:
    return input.strip(whitespace_to_strip).split(slug_delimiter)


class WrappingFormatter(argparse.RawTextHelpFormatter):
    """Used in help screen"""

    def _split_lines(self, text, width):
        text = text.split("\n\n")
        text = map(lambda t: self._whitespace_matcher.sub(" ", t).strip(), text)
        text = map(lambda t: textwrap.wrap(t, width=56), text)
        text = [item for sublist in text for item in sublist]
        return text


def parse_args(args=[]):
    """
    Argument parsing that is doable before the config is available.
    Everything else goes into "text" for later parsing.
    """
    parser = argparse.ArgumentParser(
        formatter_class=WrappingFormatter,
        add_help=False,
        description="Collect your thoughts and notes without leaving the command line",
        epilog=textwrap.dedent(
            """
        Thank you to all of our contributors! Come see the whole list of code and
        financial contributors at https://github.com/jrnl-org/jrnl. And special
        thanks to Bad Lip Reading for the Yoda joke in the Writing section above."""
        ),
    )

    optional = parser.add_argument_group("Optional Arguments")
    optional.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="Print information useful for troubleshooting",
    )

    standalone = parser.add_argument_group(
        "Standalone Commands",
        "These commands will exit after they complete. You may only run one at a time.",
    )
    standalone.add_argument("--help", action="help", help="Show this help message")
    standalone.add_argument("-h", action="help", help=argparse.SUPPRESS)
    standalone.add_argument(
        "--version",
        action="store_const",
        const=preconfig_version,
        dest="preconfig_cmd",
        help="Print version information",
    )
    standalone.add_argument(
        "-v",
        action="store_const",
        const=preconfig_version,
        dest="preconfig_cmd",
        help=argparse.SUPPRESS,
    )
    standalone.add_argument(
        "--diagnostic",
        action="store_const",
        const=preconfig_diagnostic,
        dest="preconfig_cmd",
        help=argparse.SUPPRESS,
    )
    standalone.add_argument(
        "--list",
        action="store_const",
        const=postconfig_list,
        dest="postconfig_cmd",
        help="List all configured journals",
    )
    standalone.add_argument(
        "--ls",
        action="store_const",
        const=postconfig_list,
        dest="postconfig_cmd",
        help=argparse.SUPPRESS,
    )
    standalone.add_argument(
        "-ls",
        action="store_const",
        const=lambda **kwargs: deprecated_cmd(
            "-ls", "--list or --ls", callback=postconfig_list, **kwargs
        ),
        dest="postconfig_cmd",
        help=argparse.SUPPRESS,
    )
    standalone.add_argument(
        "--encrypt",
        help="Encrypt selected journal with a password",
        action="store_const",
        metavar="TYPE",
        const=postconfig_encrypt,
        dest="postconfig_cmd",
    )
    standalone.add_argument(
        "--decrypt",
        help="Decrypt selected journal and store it in plain text",
        action="store_const",
        metavar="TYPE",
        const=postconfig_decrypt,
        dest="postconfig_cmd",
    )
    standalone.add_argument(
        "--import",
        action="store_const",
        metavar="TYPE",
        const=postconfig_import,
        dest="postconfig_cmd",
        help=f"""
        Import entries from another journal.

        Optional parameters:

        --file FILENAME (default: uses stdin)

        --format [{util.oxford_list(IMPORT_FORMATS)}] (default: jrnl)
        """,
    )
    standalone.add_argument(
        "--file",
        metavar="FILENAME",
        dest="filename",
        help=argparse.SUPPRESS,
        default=None,
    )
    standalone.add_argument("-i", dest="filename", help=argparse.SUPPRESS)

    compose_msg = """
    To add a new entry into your journal, simply write it on the command line:

        jrnl yesterday: I was walking and I found this big log.

    The date and the following colon ("yesterday:") are optional. If you leave
    them out, "now" will be used:

        jrnl Then I rolled the log over.

    Also, you can mark extra special entries ("star" them) with an asterisk:

        jrnl *And underneath was a tiny little stick.

    Please note that asterisks might be a special character in your shell, so you
    might have to escape them. When in doubt about escaping, put quotes around
    your entire entry:

        jrnl "saturday at 2am: *Then I was like 'That log had a child!'" """

    composing = parser.add_argument_group(
        "Writing", textwrap.dedent(compose_msg).strip()
    )
    composing.add_argument("text", metavar="", nargs="*")

    read_msg = (
        "To find entries from your journal, use any combination of the below filters."
    )
    reading = parser.add_argument_group("Searching", textwrap.dedent(read_msg))
    reading.add_argument(
        "-on", dest="on_date", metavar="DATE", help="Show entries on this date"
    )
    reading.add_argument(
        "-today-in-history",
        dest="today_in_history",
        action="store_true",
        help="Show entries of today over the years",
    )
    reading.add_argument(
        "-month",
        dest="month",
        metavar="DATE",
        help="Show entries on this month of any year",
    )
    reading.add_argument(
        "-day",
        dest="day",
        metavar="DATE",
        help="Show entries on this day of any month",
    )
    reading.add_argument(
        "-year",
        dest="year",
        metavar="DATE",
        help="Show entries of a specific year",
    )
    reading.add_argument(
        "-from",
        dest="start_date",
        metavar="DATE",
        help="Show entries after, or on, this date",
    )
    reading.add_argument(
        "-to",
        dest="end_date",
        metavar="DATE",
        help="Show entries before, or on, this date (alias: -until)",
    )
    reading.add_argument("-until", dest="end_date", help=argparse.SUPPRESS)
    reading.add_argument(
        "-contains",
        dest="contains",
        metavar="TEXT",
        help="Show entries containing specific text (put quotes around text with spaces)",
    )
    reading.add_argument(
        "-and",
        dest="strict",
        action="store_true",
        help='Show only entries that match all conditions, like saying "x AND y" (default: OR)',
    )
    reading.add_argument(
        "-starred",
        dest="starred",
        action="store_true",
        help="Show only starred entries (marked with *)",
    )
    reading.add_argument(
        "-n",
        dest="limit",
        default=None,
        metavar="NUMBER",
        help="Show a maximum of NUMBER entries (note: '-n 3' and '-3' have the same effect)",
        nargs="?",
        type=int,
    )
    reading.add_argument(
        "-not",
        dest="excluded",
        nargs="?",
        default=[],
        metavar="TAG",
        action="append",
        help="Exclude entries with this tag",
    )

    search_options_msg = """    These help you do various tasks with the selected entries from your search.
    If used on their own (with no search), they will act on your entire journal"""
    exporting = parser.add_argument_group(
        "Searching Options", textwrap.dedent(search_options_msg)
    )
    exporting.add_argument(
        "--edit",
        dest="edit",
        help="Opens the selected entries in your configured editor",
        action="store_true",
    )
    exporting.add_argument(
        "--delete",
        dest="delete",
        action="store_true",
        help="Interactively deletes selected entries",
    )
    exporting.add_argument(
        "--format",
        metavar="TYPE",
        dest="export",
        choices=EXPORT_FORMATS,
        help=f"""
        Display selected entries in an alternate format.

        TYPE can be: {util.oxford_list(EXPORT_FORMATS)}.

        Optional parameters:

        --file FILENAME Write output to file instead of stdout
        """,
        default=False,
    )
    exporting.add_argument(
        "--export",
        metavar="TYPE",
        dest="export",
        choices=EXPORT_FORMATS,
        help=argparse.SUPPRESS,
    )
    exporting.add_argument(
        "--tags",
        dest="tags",
        action="store_true",
        help="Alias for '--format tags'. Returns a list of all tags and number of occurences",
    )
    exporting.add_argument(
        "--short",
        dest="short",
        action="store_true",
        help="Show only titles or line containing the search tags",
    )
    exporting.add_argument(
        "-s",
        dest="short",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    exporting.add_argument(
        "-o",
        dest="filename",
        help=argparse.SUPPRESS,
    )

    config_overrides = parser.add_argument_group(
        "Config file overrides",
        textwrap.dedent("These are one-off overrides of the config file options"),
    )
    config_overrides.add_argument(
        "--config-override",
        dest="config_override",
        action="store",
        type=deserialize_config_args,
        nargs="?",
        default=None,
        metavar="CONFIG_KV_PAIR",
        help="""
        Override configured key-value pairs with CONFIG_KV_PAIR for this command invocation only. 

        Examples: \n
        \t - Use a different editor for this jrnl entry, call: \n
            \t jrnl --config-override editor: "nano" \n
        \t - Override color selections\n
           \t jrnl --config-override colors.body: blue, colors.title: green
        """,
    )

    # Handle '-123' as a shortcut for '-n 123'
    num = re.compile(r"^-(\d+)$")
    args = [num.sub(r"-n \1", arg) for arg in args]

    parsed_args = parser.parse_intermixed_args(args)
    return parsed_args
