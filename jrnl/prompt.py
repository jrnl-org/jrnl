# Copyright © 2012-2023 jrnl contributors
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
        from jrnl.keyring import set_keyring_password

        set_keyring_password(pw, journal_name)

    return pw


def prompt_password(first_try: bool = True) -> str:
    if not first_try:
        print_msg(Message(MsgText.WrongPasswordTryAgain, MsgStyle.WARNING))

    return (
        print_msg(
            Message(MsgText.Password, MsgStyle.PROMPT),
            get_input=True,
            hide_input=True,
        )
        or ""
    )


def yesno(prompt: Message | str, default: bool = True) -> bool:
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
