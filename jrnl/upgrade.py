import util
from . import __version__
from . import Journal
import sys
from .EncryptedJournal import EncryptedJournal


def upgrade_jrnl_if_necessary(config_path):
    with open(config_path) as f:
        config_file = f.read()
    if not config_file.strip().startswith("{"):
        return

    config = util.load_config(config_path)

    util.prompt("""Welcome to jrnl {}.

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
""".format(__version__))
    encrypted_journals = {}
    plain_journals = {}
    for journal, journal_conf in config['journals'].items():
        if isinstance(journal_conf, dict):
            if journal_conf.get("encrypt"):
                encrypted_journals[journal] = journal_conf.get("journal")
            else:
                plain_journals[journal] = journal_conf.get("journal")
        else:
            if config.get('encrypt'):
                encrypted_journals[journal] = journal_conf
            else:
                plain_journals[journal] = journal_conf
    if encrypted_journals:
        longest_journal_name = max([len(journal) for journal in config['journals']])
        util.prompt("\nFollowing encrypted journals will be upgraded to jrnl {}:".format(__version__))
        for journal, path in encrypted_journals.items():
            util.prompt("    {:{pad}} -> {}".format(journal, path, pad=longest_journal_name))
        if plain_journals:
            util.prompt("\nFollowing plain text journals will be not be touched:")
            for journal, path in plain_journals.items():
                util.prompt("    {:{pad}} -> {}".format(journal, path, pad=longest_journal_name))

    cont = util.yesno("Continue upgrading jrnl?", default=False)
    if not cont:
        util.prompt("jrnl NOT upgraded, exiting.")
        sys.exit(1)

    for journal_name, path in encrypted_journals.items():
        util.prompt("Upgrading {} journal (stored in {}).".format(journal_name, path))
        old_journal = Journal.open_journal(journal_name, config, legacy=True)
        new_journal = EncryptedJournal.from_journal(old_journal)
        new_journal.write()
        # util.get_password(keychain=journal, validator=lambda pwd: upgrade_encrypted_journal(path, pwd))

    with open(config_path + ".backup", 'w') as config_backup:
        config_backup.write(config_file)

    util.prompt("""\n\nYour old config has been backed up to {}.backup.
We're all done here and you can start enjoying jrnl 2.""".format(config_path))
