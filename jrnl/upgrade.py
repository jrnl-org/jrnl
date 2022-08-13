# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import os

from jrnl import Journal
from jrnl import __version__
from jrnl.config import is_config_json
from jrnl.config import load_config
from jrnl.config import scope_config
from jrnl.EncryptedJournal import EncryptedJournal
from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg
from jrnl.output import print_msgs
from jrnl.path import expand_path
from jrnl.prompt import yesno


def backup(filename, binary=False):
    filename = expand_path(filename)

    try:
        with open(filename, "rb" if binary else "r") as original:
            contents = original.read()

        with open(filename + ".backup", "wb" if binary else "w") as backup:
            backup.write(contents)

        print_msg(
            Message(
                MsgText.BackupCreated, MsgStyle.NORMAL, {"filename": "filename.backup"}
            )
        )

    except FileNotFoundError:
        print_msg(Message(MsgText.DoesNotExist, MsgStyle.WARNING, {"name": filename}))
        cont = yesno(f"\nCreate {filename}?", default=False)
        if not cont:
            raise JrnlException(Message(MsgText.UpgradeAborted, MsgStyle.WARNING))


def check_exists(path):
    """
    Checks if a given path exists.
    """
    return os.path.exists(path)


def upgrade_jrnl(config_path):
    config = load_config(config_path)

    print_msg(Message(MsgText.WelcomeToJrnl, MsgStyle.NORMAL, {"version": __version__}))

    encrypted_journals = {}
    plain_journals = {}
    other_journals = {}
    all_journals = []

    for journal_name, journal_conf in config["journals"].items():
        if isinstance(journal_conf, dict):
            path = expand_path(journal_conf.get("journal"))
            encrypt = journal_conf.get("encrypt")
        else:
            encrypt = config.get("encrypt")
            path = expand_path(journal_conf)

        if os.path.exists(path):
            path = os.path.expanduser(path)
        else:
            print_msg(Message(MsgText.DoesNotExist, MsgStyle.ERROR, {"name": path}))
            continue

        if encrypt:
            encrypted_journals[journal_name] = path
        elif os.path.isdir(path):
            other_journals[journal_name] = path
        else:
            plain_journals[journal_name] = path

    kwargs = {
        # longest journal name
        "pad": max([len(journal) for journal in config["journals"]]),
    }

    _print_journal_summary(
        journals=encrypted_journals,
        header=Message(
            MsgText.JournalsToUpgrade,
            params={
                "version": __version__,
            },
        ),
        **kwargs,
    )

    _print_journal_summary(
        journals=plain_journals,
        header=Message(
            MsgText.JournalsToUpgrade,
            params={
                "version": __version__,
            },
        ),
        **kwargs,
    )

    _print_journal_summary(
        journals=other_journals,
        header=Message(MsgText.JournalsToIgnore),
        **kwargs,
    )

    cont = yesno(Message(MsgText.ContinueUpgrade), default=False)
    if not cont:
        raise JrnlException(Message(MsgText.UpgradeAborted), MsgStyle.WARNING)

    for journal_name, path in encrypted_journals.items():
        print_msg(
            Message(
                MsgText.UpgradingJournal,
                params={
                    "journal_name": journal_name,
                    "path": path,
                },
            )
        )

        backup(path, binary=True)
        old_journal = Journal.open_journal(
            journal_name, scope_config(config, journal_name), legacy=True
        )
        all_journals.append(EncryptedJournal.from_journal(old_journal))

    for journal_name, path in plain_journals.items():
        print_msg(
            Message(
                MsgText.UpgradingJournal,
                params={
                    "journal_name": journal_name,
                    "path": path,
                },
            )
        )

        backup(path)
        old_journal = Journal.open_journal(
            journal_name, scope_config(config, journal_name), legacy=True
        )
        all_journals.append(Journal.PlainJournal.from_journal(old_journal))

    # loop through lists to validate
    failed_journals = [j for j in all_journals if not j.validate_parsing()]

    if len(failed_journals) > 0:
        raise JrnlException(
            Message(MsgText.AbortingUpgrade, MsgStyle.WARNING),
            Message(
                MsgText.JournalFailedUpgrade,
                MsgStyle.ERROR,
                {
                    "s": "s" if len(failed_journals) > 1 else "",
                    "failed_journals": "\n".join(j.name for j in failed_journals),
                },
            ),
        )

    # write all journals - or - don't
    for j in all_journals:
        j.write()

    print_msg(Message(MsgText.UpgradingConfig, MsgStyle.NORMAL))

    backup(config_path)

    print_msg(Message(MsgText.AllDoneUpgrade, MsgStyle.NORMAL))


def is_old_version(config_path):
    return is_config_json(config_path)


def _print_journal_summary(journals: dict, header: Message, pad: int) -> None:
    if not journals:
        return

    msgs = [header]
    for journal, path in journals.items():
        msgs.append(
            Message(
                MsgText.PaddedJournalName,
                params={
                    "journal_name": journal,
                    "path": path,
                    "pad": pad,
                },
            )
        )
    print_msgs(msgs)
