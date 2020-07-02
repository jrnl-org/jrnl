import argparse
import re

from . import plugins
from .commands import preconfig_version
from .commands import preconfig_diagnostic
from .commands import postconfig_list
from .commands import deprecated_cmd


def parse_args_before_config(args=None):
    """
    Argument parsing that is doable before the config is available.
    Everything else goes into "text" for later parsing.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="store_const",
        const=preconfig_version,
        dest="preconfig_cmd",
        help="prints version information and exits",
    )

    parser.add_argument(
        "--cmd1",
        action="store_const",
        const=lambda: print("cmd1"),
        dest="preconfig_cmd",
    )
    parser.add_argument(
        "--diagnostic",
        action="store_const",
        const=preconfig_diagnostic,
        dest="preconfig_cmd",
        help="outputs diagnostic information and exits",
    )

    parser.add_argument(
        "--ls",
        "--list",
        action="store_const",
        const=postconfig_list,
        dest="postconfig_cmd",
        help="lists all configured journals",
    )

    parser.add_argument(
        "-ls",
        action="store_const",
        const=lambda **kwargs: deprecated_cmd(
            "-ls", "--ls or --list", callback=postconfig_list, **kwargs
        ),
        dest="postconfig_cmd",
        help="displays accessible journals",
    )

    parser.add_argument(
        "-d", "--debug", dest="debug", action="store_true", help="execute in debug mode"
    )

    composing = parser.add_argument_group(
        "Composing",
        'To write an entry simply write it on the command line, e.g. "jrnl yesterday at 1pm: Went to the gym."',
    )

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
        nargs="?",
        default=[],
        metavar="E",
        action="append",
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

    exporting.add_argument(
        "--delete",
        dest="delete",
        action="store_true",
        help="Opens an interactive interface for deleting entries.",
    )

    # Everything else
    composing.add_argument("text", metavar="", nargs="*")

    if not args:
        args = []

    # Handle '-123' as a shortcut for '-n 123'
    num = re.compile(r"^-(\d+)$")
    args = [num.sub(r"-n \1", arg) for arg in args]

    # return parser.parse_args(args)
    return parser.parse_intermixed_args(args)


def parse_args_after_config(args=None):
    return None
