# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html


class UserAbort(Exception):
    pass


class UpgradeValidationException(Exception):
    """Raised when the contents of an upgraded journal do not match the old journal"""

    pass
