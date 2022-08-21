# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg
from jrnl.output import print_msgs


def create_password(journal_name: str) -> str:
    kwargs = {
        "get_input": True,
        "hide_input": True,
    }
    while True:
        pw = print_msg(
            Message(
                MsgText.PasswordFirstEntry,
                MsgStyle.PROMPT,
                params={"journal_name": journal_name},
            ),
            **kwargs
        )

        if not pw:
            print_msg(Message(MsgText.PasswordCanNotBeEmpty, MsgStyle.WARNING))
            continue

        elif pw == print_msg(
            Message(MsgText.PasswordConfirmEntry, MsgStyle.PROMPT), **kwargs
        ):
            break

        print_msg(Message(MsgText.PasswordDidNotMatch, MsgStyle.ERROR))

    if yesno(Message(MsgText.PasswordStoreInKeychain), default=True):
        from jrnl.EncryptedJournal import set_keychain

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
