# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

"""
Functions in this file are standalone commands. All standalone commands are split into
two categories depending on whether they require the config to be loaded to be able to
run.

1. "preconfig" commands don't require the config at all, and can be run before the
   config has been loaded.
2. "postconfig" commands require to config to have already been loaded, parsed, and
   scoped before they can be run.

Also, please note that all (non-builtin) imports should be scoped to each function to
avoid any possible overhead for these standalone commands.
"""
import platform
import sys

from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg
from jrnl.prompt import create_password


def preconfig_diagnostic(_):
    from jrnl import __title__
    from jrnl import __version__

    print(
        f"{__title__}: {__version__}\n"
        f"Python: {sys.version}\n"
        f"OS: {platform.system()} {platform.release()}"
    )


def preconfig_version(_):
    import textwrap

    from jrnl import __title__
    from jrnl import __version__

    output = f"""
    {__title__} {__version__}

    Copyright © 2012-2022 jrnl contributors

    This is free software, and you are welcome to redistribute it under certain
    conditions; for details, see: https://www.gnu.org/licenses/gpl-3.0.html
    """

    output = textwrap.dedent(output).strip()

    print(output)


def postconfig_list(args, config, **kwargs):
    from jrnl.output import list_journals

    print(list_journals(config, args.export))


def postconfig_import(args, config, **kwargs):
    from jrnl.Journal import open_journal
    from jrnl.plugins import get_importer

    # Requires opening the journal
    journal = open_journal(args.journal_name, config)

    format = args.export if args.export else "jrnl"
    get_importer(format).import_(journal, args.filename)


def postconfig_encrypt(args, config, original_config, **kwargs):
    """
    Encrypt a journal in place, or optionally to a new file
    """
    from jrnl.config import update_config
    from jrnl.EncryptedJournal import EncryptedJournal
    from jrnl.install import save_config
    from jrnl.Journal import open_journal

    # Open the journal
    journal = open_journal(args.journal_name, config)

    if hasattr(journal, "can_be_encrypted") and not journal.can_be_encrypted:
        raise JrnlException(
            Message(
                MsgText.CannotEncryptJournalType,
                MsgStyle.ERROR,
                {
                    "journal_name": args.journal_name,
                    "journal_type": journal.__class__.__name__,
                },
            )
        )

    new_journal = EncryptedJournal.from_journal(journal)

    # If journal is encrypted, create new password
    if journal.config["encrypt"] is True:
        print(f"Journal {journal.name} is already encrypted. Create a new password.")
        new_journal.password = create_password(new_journal.name)

    journal.config["encrypt"] = True
    new_journal.write(args.filename)

    print_msg(
        Message(
            MsgText.JournalEncryptedTo,
            MsgStyle.NORMAL,
            {"path": args.filename or new_journal.config["journal"]},
        )
    )

    # Update the config, if we encrypted in place
    if not args.filename:
        update_config(
            original_config, {"encrypt": True}, args.journal_name, force_local=True
        )
        save_config(original_config)


def postconfig_decrypt(args, config, original_config, **kwargs):
    """Decrypts into new file. If filename is not set, we encrypt the journal file itself."""
    from jrnl.config import update_config
    from jrnl.install import save_config
    from jrnl.Journal import PlainJournal
    from jrnl.Journal import open_journal

    journal = open_journal(args.journal_name, config)
    journal.config["encrypt"] = False

    new_journal = PlainJournal.from_journal(journal)
    new_journal.write(args.filename)
    print_msg(
        Message(
            MsgText.JournalDecryptedTo,
            MsgStyle.NORMAL,
            {"path": args.filename or new_journal.config["journal"]},
        )
    )

    # Update the config, if we decrypted in place
    if not args.filename:
        update_config(
            original_config, {"encrypt": False}, args.journal_name, force_local=True
        )
        save_config(original_config)
