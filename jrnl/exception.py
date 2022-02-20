# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
import textwrap

from enum import Enum


class JrnlExceptionMessage(Enum):
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

    KeyboardInterrupt = "Aborted by user"

    EditorMisconfigured = """
        No such file or directory: '{editor_key}'

        Please check the 'editor' key in your config file for errors:
            editor: '{editor_key}'
        """

    JournalFailedUpgrade = """
        The following journal{s} failed to upgrade:
        {failed_journals}

        Please tell us about this problem at the following URL:
        https://github.com/jrnl-org/jrnl/issues/new?title=JournalFailedUpgrade
        """

    NothingToDelete = """
        No entries to delete, because the search returned no results.
        """

    NoTextReceived = """
        Nothing saved to file.
        """

    UpgradeAborted = """
        jrnl was NOT upgraded
        """

    EditorNotConfigured = """
        There is no editor configured.

        To use the --edit option, please specify an editor your config file:
            {config_file}

        For examples of how to configure an external editor, see:
            https://jrnl.sh/en/stable/external-editors/
        """

    AltConfigNotFound = """
        Alternate configuration file not found at the given path:
            {config_file}
        """

    PasswordMaxTriesExceeded = """
        Too many attempts with wrong password.
        """

    SomeTest = """
        Some error or something

        This is a thing to test with this message or whatever and maybe it just
        keeps going forever because it's super long for no apparent reason
        """


class JrnlException(Exception):
    """Common exceptions raised by jrnl."""

    def __init__(self, exception_msg: JrnlExceptionMessage, **kwargs):
        self.exception_msg = exception_msg
        self.title = str(exception_msg.name)
        self.message = self._get_error_message(**kwargs)

    def _get_error_message(self, **kwargs):
        msg = self.exception_msg.value
        msg = msg.format(**kwargs)
        msg = textwrap.dedent(msg)
        return msg
