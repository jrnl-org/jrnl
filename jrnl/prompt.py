# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import getpass
import sys


def create_password(
    journal_name: str, prompt: str = "Enter password for new journal: "
) -> str:
    while True:
        pw = getpass.getpass(prompt)
        if not pw:
            print("Password can't be an empty string!", file=sys.stderr)
            continue
        elif pw == getpass.getpass("Enter password again: "):
            break

        print("Passwords did not match, please try again", file=sys.stderr)

    if yesno("Do you want to store the password in your keychain?", default=True):
        from .EncryptedJournal import set_keychain

        set_keychain(journal_name, pw)
    return pw


def yesno(prompt, default=True):
    prompt = f"{prompt.strip()} {'[Y/n]' if default else '[y/N]'} "
    response = input(prompt)
    return {"y": True, "n": False}.get(response.lower().strip(), default)
