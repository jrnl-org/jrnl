from enum import Enum
from typing import NamedTuple
from typing import Mapping
from typing import Callable
from rich.panel import Panel
from rich import box


class _MsgColor(NamedTuple):
    """
    String representing a standard color to display
    see: https://rich.readthedocs.io/en/stable/appendix/colors.html
    """

    color: str


class MsgDecoration(Enum):
    NONE = {
        "callback": lambda x, **_: x,
        "args": {},
    }
    BRACKET = {
        # @todo this should be a more robust function
        "callback": lambda x, **_: f"[ {x} ]",
        "args": {},
    }
    BOX = {
        "callback": Panel,
        "args": {
            "expand": False,
            "padding": (0, 2),
            "title_align": "left",
            "box": box.HEAVY,
        },
    }

    @property
    def callback(self) -> Callable:
        return self.value["callback"]

    @property
    def args(self) -> dict:
        return self.value["args"]


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
    DeleteEntryQuestion = "Delete entry '{entry_title}'?"
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

    # --- Password --- #
    Password = "Password:"
    PasswordFirstEntry = "Enter new password: "
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


class MsgStyle(Enum):
    BARE = {
        "decoration": MsgDecoration.NONE,
        "color": _MsgColor("white"),
    }
    PLAIN = {
        "decoration": MsgDecoration.BRACKET,
        "color": _MsgColor("white"),
    }
    PROMPT = {
        "decoration": MsgDecoration.NONE,
        "color": _MsgColor("white"),
        "append_space": True,
    }
    TITLE = {
        "decoration": MsgDecoration.BOX,
        "color": _MsgColor("cyan"),
    }
    NORMAL = {
        "decoration": MsgDecoration.BOX,
        "color": _MsgColor("white"),
    }
    WARNING = {
        "decoration": MsgDecoration.BOX,
        "color": _MsgColor("yellow"),
    }
    ERROR = {
        "decoration": MsgDecoration.BOX,
        "color": _MsgColor("red"),
        "box_title": str(MsgText.Error),
    }
    ERROR_ON_NEW_LINE = {
        "decoration": MsgDecoration.BOX,
        "color": _MsgColor("red"),
        "prepend_newline": True,
        "box_title": str(MsgText.Error),
    }

    @property
    def decoration(self) -> MsgDecoration:
        return self.value["decoration"]

    @property
    def color(self) -> _MsgColor:
        return self.value["color"].color

    @property
    def prepend_newline(self) -> bool:
        return self.value.get("prepend_newline", False)

    @property
    def append_space(self) -> bool:
        return self.value.get("append_space", False)

    @property
    def box_title(self) -> MsgText:
        return self.value.get("box_title", None)


class Message(NamedTuple):
    text: MsgText
    style: MsgStyle = MsgStyle.NORMAL
    params: Mapping = {}
