# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
import textwrap


class UserAbort(Exception):
    pass


class UpgradeValidationException(Exception):
    """Raised when the contents of an upgraded journal do not match the old journal"""

    pass


class JrnlError(Exception):
    """Common exceptions raised by jrnl."""

    def __init__(self, error_type, **kwargs):
        self.error_type = error_type
        self.message = self._get_error_message(**kwargs)

    def _get_error_message(self, **kwargs):
        error_messages = {
            "ConfigDirectoryIsFile": """
                The path to your jrnl configuration directory is a file, not a directory:

                {config_directory_path}

                Removing this file will allow jrnl to save its configuration.
                """,
            "LineWrapTooSmallForDateFormat": """
                The provided linewrap value of {config_linewrap} is too small by
                {columns} columns to display the timestamps in the configured time
                format for journal {journal}.

                You can avoid this error by specifying a linewrap value that is larger
                by at least {columns} in the configuration file or by using
                --config-override at the command line
                """,
            "CannotEncryptJournalType": """
                The journal {journal_name} can't be encrypted because it is a
                {journal_type} journal.

                To encrypt it, create a new journal referencing a file, export
                this journal to the new journal, then encrypt the new journal.
                """,
        }

        msg = error_messages[self.error_type].format(**kwargs)
        msg = textwrap.dedent(msg)
        return msg
