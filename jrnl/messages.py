from enum import Enum
from typing import NamedTuple
from typing import Mapping


class _MsgColor(NamedTuple):
    # This is a colorama color, and colorama doesn't support enums or type hints
    # see: https://github.com/tartley/colorama/issues/91
    color: str


class MsgType(Enum):
    TITLE = _MsgColor("cyan")
    NORMAL = _MsgColor("white")
    WARNING = _MsgColor("yellow")
    ERROR = _MsgColor("red")

    @property
    def color(self) -> _MsgColor:
        return self.value.color


class MsgText(Enum):
    def __str__(self) -> str:
        return self.value

    # --- Exceptions ---#
    UncaughtException = """
        ERROR
        {exception}

        This is probably a bug. Please file an issue at:
        https://github.com/jrnl-org/jrnl/issues/new/choose
        """

    ConfigDirectoryIsFile = """
        The path to your jrnl configuration directory is a file, not a directory:

        {config_directory_path}

        Removing this file will allow jrnl to save its configuration.
        """

    LineWrapTooSmallForDateFormat = """
        The provided linewrap value of {config_linewrap} is too small by
        {columns} columns to display the timestamps in the configured time
        format for journal {journal}.

        You can avoid this error by specifying a linewrap value that is larger
        by at least {columns} in the configuration file or by using
        --config-override at the command line
        """

    CannotEncryptJournalType = """
        The journal {journal_name} can't be encrypted because it is a
        {journal_type} journal.

        To encrypt it, create a new journal referencing a file, export
        this journal to the new journal, then encrypt the new journal.
        """

    KeyboardInterruptMsg = "Aborted by user"

    # --- Journal status ---#
    JournalNotSaved = "Entry NOT saved to journal"

    # --- Editor ---#
    WritingEntryStart = """
        Writing Entry
        To finish writing, press {how_to_quit} on a blank line.
        """
    HowToQuitWindows = "Ctrl+z and then Enter"
    HowToQuitLinux = "Ctrl+d"

    EditorMisconfigured = """
        No such file or directory: '{editor_key}'

        Please check the 'editor' key in your config file for errors:
            editor: '{editor_key}'
        """

    EditorNotConfigured = """
        There is no editor configured

        To use the --edit option, please specify an editor your config file:
            {config_file}

        For examples of how to configure an external editor, see:
            https://jrnl.sh/en/stable/external-editors/
        """

    NoTextReceived = """
        Nothing saved to file
        """

    # --- Upgrade --- #
    JournalFailedUpgrade = """
        The following journal{s} failed to upgrade:
        {failed_journals}

        Please tell us about this problem at the following URL:
        https://github.com/jrnl-org/jrnl/issues/new?title=JournalFailedUpgrade
        """

    UpgradeAborted = """
        jrnl was NOT upgraded
        """

    # -- Config --- #
    AltConfigNotFound = """
        Alternate configuration file not found at the given path:
            {config_file}
        """

    # --- Password --- #
    PasswordMaxTriesExceeded = """
        Too many attempts with wrong password
        """

    # --- Search --- #
    NothingToDelete = """
        No entries to delete, because the search returned no results
        """


class Message(NamedTuple):
    text: MsgText
    type: MsgType = MsgType.NORMAL
    params: Mapping = {}
