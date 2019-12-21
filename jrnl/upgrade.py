import sys

from . import __version__
from . import Journal
from . import util
from .EncryptedJournal import EncryptedJournal
from .util import UserAbort
import os


def backup(filename, binary=False):
    print(f"  Created a backup at {filename}.backup", file=sys.stderr)
    filename = os.path.expanduser(os.path.expandvars(filename))
    with open(filename, "rb" if binary else "r") as original:
        contents = original.read()
    with open(filename + ".backup", "wb" if binary else "w") as backup:
        backup.write(contents)


def upgrade_jrnl_if_necessary(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        config_file = f.read()
    if not config_file.strip().startswith("{"):
        return

    config = util.load_config(config_path)

    print(
        f"""Welcome to jrnl {__version__}.

It looks like you've been using an older version of jrnl until now. That's
okay - jrnl will now upgrade your configuration and journal files. Afterwards
you can enjoy all of the great new features that come with jrnl 2:

- Support for storing your journal in multiple files
- Faster reading and writing for large journals
- New encryption back-end that makes installing jrnl much easier
- Tons of bug fixes

Please note that jrnl 1.x is NOT forward compatible with this version of jrnl.
If you choose to proceed, you will not be able to use your journals with
older versions of jrnl anymore.
"""
    )

    encrypted_journals = {}
    plain_journals = {}
    other_journals = {}
    all_journals = []

    for journal_name, journal_conf in config["journals"].items():
        if isinstance(journal_conf, dict):
            path = journal_conf.get("journal")
            encrypt = journal_conf.get("encrypt")
        else:
            encrypt = config.get("encrypt")
            path = journal_conf

        path = os.path.expanduser(path)

        if encrypt:
            encrypted_journals[journal_name] = path
        elif os.path.isdir(path):
            other_journals[journal_name] = path
        else:
            plain_journals[journal_name] = path

    longest_journal_name = max([len(journal) for journal in config["journals"]])
    if encrypted_journals:
        print(
            f"\nFollowing encrypted journals will be upgraded to jrnl {__version__}:",
            file=sys.stderr,
        )
        for journal, path in encrypted_journals.items():
            print(
                "    {:{pad}} -> {}".format(journal, path, pad=longest_journal_name),
                file=sys.stderr,
            )

    if plain_journals:
        print(
            f"\nFollowing plain text journals will upgraded to jrnl {__version__}:",
            file=sys.stderr,
        )
        for journal, path in plain_journals.items():
            print(
                "    {:{pad}} -> {}".format(journal, path, pad=longest_journal_name),
                file=sys.stderr,
            )

    if other_journals:
        print("\nFollowing journals will be not be touched:", file=sys.stderr)
        for journal, path in other_journals.items():
            print(
                "    {:{pad}} -> {}".format(journal, path, pad=longest_journal_name),
                file=sys.stderr,
            )

    try:
        cont = util.yesno("\nContinue upgrading jrnl?", default=False)
        if not cont:
            raise KeyboardInterrupt
    except KeyboardInterrupt:
        raise UserAbort("jrnl NOT upgraded, exiting.")

    for journal_name, path in encrypted_journals.items():
        print(
            f"\nUpgrading encrypted '{journal_name}' journal stored in {path}...",
            file=sys.stderr,
        )
        backup(path, binary=True)
        old_journal = Journal.open_journal(
            journal_name, util.scope_config(config, journal_name), legacy=True
        )
        all_journals.append(EncryptedJournal.from_journal(old_journal))

    for journal_name, path in plain_journals.items():
        print(
            f"\nUpgrading plain text '{journal_name}' journal stored in {path}...",
            file=sys.stderr,
        )
        backup(path)
        old_journal = Journal.open_journal(
            journal_name, util.scope_config(config, journal_name), legacy=True
        )
        all_journals.append(Journal.PlainJournal.from_journal(old_journal))

    # loop through lists to validate
    failed_journals = [j for j in all_journals if not j.validate_parsing()]

    if len(failed_journals) > 0:
        print(
            "\nThe following journal{} failed to upgrade:\n{}".format(
                "s" if len(failed_journals) > 1 else "",
                "\n".join(j.name for j in failed_journals),
            ),
            file=sys.stderr,
        )

        raise UpgradeValidationException

    # write all journals - or - don't
    for j in all_journals:
        j.write()

    print("\nUpgrading config...", file=sys.stderr)
    backup(config_path)

    print("\nWe're all done here and you can start enjoying jrnl 2.", file=sys.stderr)


class UpgradeValidationException(Exception):
    """Raised when the contents of an upgraded journal do not match the old journal"""

    pass
