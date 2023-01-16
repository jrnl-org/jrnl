# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import keyring

from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg


def get_keyring_password(journal_name: str = "default") -> str | None:
    try:
        return keyring.get_password("jrnl", journal_name)
    except keyring.errors.KeyringError as e:
        if not isinstance(e, keyring.errors.NoKeyringError):
            print_msg(Message(MsgText.KeyringRetrievalFailure, MsgStyle.ERROR))
        return None


def set_keyring_password(password: str, journal_name: str = "default") -> None:
    try:
        return keyring.set_password("jrnl", journal_name, password)
    except keyring.errors.KeyringError as e:
        if isinstance(e, keyring.errors.NoKeyringError):
            msg = Message(MsgText.KeyringBackendNotFound, MsgStyle.WARNING)
        else:
            msg = Message(MsgText.KeyringRetrievalFailure, MsgStyle.ERROR)
        print_msg(msg)
