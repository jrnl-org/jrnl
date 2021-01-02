# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html


class UserAbort(Exception):
    pass


class UpgradeValidationException(Exception):
    """Raised when the contents of an upgraded journal do not match the old journal"""

    pass


class JrnlError(Exception):
    """Common exceptions raised by jrnl. """

    def __init__(self, error_type, **kwargs):
        self.error_type = error_type
        self.message = self.get_error_message(**kwargs)

    def get_error_message(self, **kwargs):

        error_messages = {
            "ConfigDirectoryIsFile": "The path to your jrnl configuration directory is a file, not a directory:\n"
            + "{config_directory_path}\n"
            + "Removing this file will allow jrnl to save its configuration."
        }

        return error_messages[self.error_type].format(**kwargs)

    pass
