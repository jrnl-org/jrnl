# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from enum import Enum


class MsgText(Enum):
    def __str__(self) -> str:
        return self.value

    # -- Welcome --- #
    WelcomeToJrnl = """
        Welcome to jrnl {version}!

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

    AllDoneUpgrade = "We're all done here and you can start enjoying jrnl 2"

    # --- Prompts --- #
    InstallJournalPathQuestion = """
        Path to your journal file (leave blank for {default_journal_path}):
        """
    DeleteEntryQuestion = "Delete entry '{entry_title}'?"
    ChangeTimeEntryQuestion = "Change time for '{entry_title}'?"
    EncryptJournalQuestion = """
        Do you want to encrypt your journal? (You can always change this later)
        """
    YesOrNoPromptDefaultYes = "[Y/n]"
    YesOrNoPromptDefaultNo = "[y/N]"
    ContinueUpgrade = "Continue upgrading jrnl?"

    # these should be lowercase, if possible in language
    # "lowercase" means whatever `.lower()` returns
    OneCharacterYes = "y"
    OneCharacterNo = "n"

    # --- Exceptions ---#
    Error = "Error"
    UncaughtException = """
        {name}
        {exception}

        This is probably a bug. Please file an issue at:
        https://github.com/jrnl-org/jrnl/issues/new/choose
        """

    ConfigDirectoryIsFile = """
        Problem with config file!
        The path to your jrnl configuration directory is a file, not a directory:

        {config_directory_path}

        Removing this file will allow jrnl to save its configuration.
        """

    CantParseConfigFile = """
        Unable to parse config file at:
        {config_path}
        """

    LineWrapTooSmallForDateFormat = """
        The provided linewrap value of {config_linewrap} is too small by
        {columns} columns to display the timestamps in the configured time
        format for journal {journal}.

        You can avoid this error by specifying a linewrap value that is larger
        by at least {columns} in the configuration file or by using
        --config-override at the command line
        """

    CannotEncryptJournalType = """
        The journal {journal_name} can't be encrypted because it is a
        {journal_type} journal.

        To encrypt it, create a new journal referencing a file, export
        this journal to the new journal, then encrypt the new journal.
        """

    ConfigEncryptedForUnencryptableJournalType = """
        The config for journal "{journal_name}" has 'encrypt' set to true, but this type
        of journal can't be encrypted. Please fix your config file.
        """

    KeyboardInterruptMsg = "Aborted by user"

    CantReadTemplate = """
        Unreadable template
        Could not read template file at:
        {template}
        """

    NoDefaultJournal = "No default journal configured\n{journals}"

    DoesNotExist = "{name} does not exist"

    # --- Journal status ---#
    JournalNotSaved = "Entry NOT saved to journal"
    JournalEntryAdded = "Entry added to {journal_name} journal"

    JournalCountAddedSingular = "{num} entry added"
    JournalCountModifiedSingular = "{num} entry modified"
    JournalCountDeletedSingular = "{num} entry deleted"

    JournalCountAddedPlural = "{num} entries added"
    JournalCountModifiedPlural = "{num} entries modified"
    JournalCountDeletedPlural = "{num} entries deleted"

    JournalCreated = "Journal '{journal_name}' created at {filename}"
    DirectoryCreated = "Directory {directory_name} created"
    JournalEncrypted = "Journal will be encrypted"
    JournalEncryptedTo = "Journal encrypted to {path}"
    JournalDecryptedTo = "Journal decrypted to {path}"
    BackupCreated = "Created a backup at {filename}"

    # --- Editor ---#
    WritingEntryStart = """
        Writing Entry
        To finish writing, press {how_to_quit} on a blank line.
        """
    HowToQuitWindows = "Ctrl+z and then Enter"
    HowToQuitLinux = "Ctrl+d"

    EditorMisconfigured = """
        No such file or directory: '{editor_key}'

        Please check the 'editor' key in your config file for errors:
            editor: '{editor_key}'
        """

    EditorNotConfigured = """
        There is no editor configured

        To use the --edit option, please specify an editor your config file:
            {config_file}

        For examples of how to configure an external editor, see:
            https://jrnl.sh/en/stable/external-editors/
        """

    NoEditsReceived = "No edits to save, because nothing was changed"

    NoTextReceived = """
        No entry to save, because no text was received
        """

    # --- Upgrade --- #
    JournalFailedUpgrade = """
        The following journal{s} failed to upgrade:
        {failed_journals}

        Please tell us about this problem at the following URL:
        https://github.com/jrnl-org/jrnl/issues/new?title=JournalFailedUpgrade
        """

    UpgradeAborted = "jrnl was NOT upgraded"

    AbortingUpgrade = "Aborting upgrade..."

    ImportAborted = "Entries were NOT imported"

    JournalsToUpgrade = """
        The following journals will be upgraded to jrnl {version}:

        """

    JournalsToIgnore = """
        The following journals will not be touched:

        """

    UpgradingJournal = """
        Upgrading '{journal_name}' journal stored in {path}...
        """

    UpgradingConfig = "Upgrading config..."

    PaddedJournalName = "{journal_name:{pad}} -> {path}"

    # -- Config --- #
    AltConfigNotFound = """
        Alternate configuration file not found at the given path:
            {config_file}
        """

    ConfigUpdated = """
        Configuration updated to newest version at {config_path}
        """

    ConfigDoubleKeys = """
        There is at least one duplicate key in your configuration file.

        Details:
        {error_message}
        """

    # --- Password --- #
    Password = "Password:"
    PasswordFirstEntry = "Enter password for journal '{journal_name}': "
    PasswordConfirmEntry = "Enter password again: "
    PasswordMaxTriesExceeded = "Too many attempts with wrong password"
    PasswordCanNotBeEmpty = "Password can't be empty!"
    PasswordDidNotMatch = "Passwords did not match, please try again"
    WrongPasswordTryAgain = "Wrong password, try again"
    PasswordStoreInKeychain = "Do you want to store the password in your keychain?"

    # --- Search --- #
    NothingToDelete = """
        No entries to delete, because the search returned no results
        """

    NothingToModify = """
        No entries to modify, because the search returned no results
        """

    NoEntriesFound = "no entries found"
    EntryFoundCountSingular = "{num} entry found"
    EntryFoundCountPlural = "{num} entries found"

    # --- Formats --- #
    HeadingsPastH6 = """
        Headings increased past H6 on export - {date} {title}
        """

    YamlMustBeDirectory = """
        YAML export must be to a directory, not a single file
        """

    JournalExportedTo = "Journal exported to {path}"

    # --- Import --- #
    ImportSummary = """
        {count} imported to {journal_name} journal
        """

    # --- Color --- #
    InvalidColor = "{key} set to invalid color: {color}"

    # --- Keyring --- #
    KeyringBackendNotFound = """
        Keyring backend not found.

        Please install one of the supported backends by visiting:
          https://pypi.org/project/keyring/
        """

    KeyringRetrievalFailure = "Failed to retrieve keyring"

    # --- Deprecation --- #
    DeprecatedCommand = """
        The command {old_cmd} is deprecated and will be removed from jrnl soon.
        Please use {new_cmd} instead.
        """
