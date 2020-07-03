import argparse
import re
import textwrap

from .plugins import util
from .plugins import IMPORT_FORMATS
from .plugins import EXPORT_FORMATS
from .commands import preconfig_version
from .commands import preconfig_diagnostic
from .commands import postconfig_list
from .util import deprecated_cmd
from .util import get_journal_name


class WrappingFormatter(argparse.RawDescriptionHelpFormatter):
    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(" ", text).strip()
        return textwrap.wrap(text, width=56)


def parse_args_before_config(args=[]):
    """
    Argument parsing that is doable before the config is available.
    Everything else goes into "text" for later parsing.
    """
    parser = argparse.ArgumentParser(
        formatter_class=WrappingFormatter,
        add_help=False,
        description="The command-line note-taking and journaling app.",
        epilog="",
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
        help="prints version information",
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
        help="list all configured journals",
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
        metavar="FILENAME",
        dest="encrypt",
        help="Encrypts your existing journal with a new password",
        nargs="?",
        default=False,
        const=None,
    )
    standalone.add_argument(
        "--decrypt",
        metavar="FILENAME",
        dest="decrypt",
        help="Decrypts your journal and stores it in plain text",
        nargs="?",
        default=False,
        const=None,
    )
    standalone.add_argument(
        "--import",
        metavar="TYPE",
        dest="import_",
        choices=IMPORT_FORMATS,
        help=f"Import entries into your journal. TYPE can be: {util.oxford_list(IMPORT_FORMATS)} (default: jrnl)",
        default=False,
        const="jrnl",
        nargs="?",
    )
    standalone.add_argument(
        "-i",
        metavar="FILENAME",
        dest="input",
        help="Optionally specifies input file when using --import.",
        default=False,
        const=None,
    )

    compose_msg = """    To add a new entry into your journal, simply write it on the command line:

        jrnl yesterday: I was walking and I found this big log.

    The date and the following colon ("yesterday:") are optional. If you leave
    them out, "now" will be used:

        jrnl Then I rolled the log over, and underneath was a tiny little stick.

    Also, you can mark extra special entries ("star" them) with an asterisk:

        jrnl *That log had a child!

    Please note that asterisks might be a special character in your shell, so you
    might have to escape them. When in doubt about escaping, put single quotes
    around your entire entry:

        jrnl 'saturday at 8pm: *Always pass on what you have learned. -Yoda'"""

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
    reading.add_argument(
        "-until", dest="end_date", help=argparse.SUPPRESS,
    )
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
        "Options for Searching", textwrap.dedent(search_options_msg)
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
        help=f"Display selected entries in an alternate format (other than jrnl). TYPE can be: {util.oxford_list(EXPORT_FORMATS)}.",
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
        "-s", dest="short", action="store_true", help=argparse.SUPPRESS,
    )
    exporting.add_argument(
        "-o",
        metavar="FILENAME",
        dest="output",
        help="Optionally specifies output file (or directory) when using --format.",
        default=False,
        const=None,
    )

    # Handle '-123' as a shortcut for '-n 123'
    num = re.compile(r"^-(\d+)$")
    args = [num.sub(r"-n \1", arg) for arg in args]

    # return parser.parse_args(args)
    return parser.parse_intermixed_args(args)


def parse_args_after_config(args, config):
    # print(str(args))  # @todo take this out

    args = get_journal_name(args, config)

    return args
