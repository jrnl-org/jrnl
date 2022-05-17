# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import getpass

from jrnl.messages import Message
from jrnl.messages import MsgText
from jrnl.messages import MsgStyle
from jrnl.output import print_msg
from jrnl.output import print_msgs


def create_password(journal_name: str) -> str:
    while True:
        pw = getpass.getpass(str(MsgText.PasswordFirstEntry))
        if not pw:
            print_msg(Message(MsgText.PasswordCanNotBeEmpty, MsgStyle.PLAIN))
            continue
        elif pw == getpass.getpass(str(MsgText.PasswordConfirmEntry)):
            break

        print_msg(Message(MsgText.PasswordDidNotMatch, MsgStyle.ERROR))

    if yesno(Message(MsgText.PasswordStoreInKeychain), default=True):
        from .EncryptedJournal import set_keychain

        set_keychain(journal_name, pw)
    return pw


def yesno(prompt: Message, default: bool = True) -> bool:
    response = print_msgs(
        [
            prompt,
            Message(
                MsgText.YesOrNoPromptDefaultYes
                if default
                else MsgText.YesOrNoPromptDefaultNo
            ),
        ],
        style=MsgStyle.PROMPT,
        delimiter=" ",
        get_input=True,
    )

    answers = {
        str(MsgText.OneCharacterYes): True,
        str(MsgText.OneCharacterNo): False,
    }

    # Does using `lower()` work in all languages?
    return answers.get(str(response).lower().strip(), default)
