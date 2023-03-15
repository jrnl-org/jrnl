# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import contextlib
import glob
import logging
import os
import sys

from rich.pretty import pretty_repr

from jrnl import __version__
from jrnl.config import DEFAULT_JOURNAL_KEY
from jrnl.config import get_config_path
from jrnl.config import get_default_colors
from jrnl.config import get_default_config
from jrnl.config import get_default_journal_path
from jrnl.config import load_config
from jrnl.config import save_config
from jrnl.config import verify_config_colors
from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg
from jrnl.path import absolute_path
from jrnl.path import expand_path
from jrnl.path import home_dir
from jrnl.prompt import yesno
from jrnl.upgrade import is_old_version


def upgrade_config(config_data: dict, alt_config_path: str | None = None) -> None:
    """Checks if there are keys missing in a given config dict, and if so, updates the config file accordingly.
    This essentially automatically ports jrnl installations if new config parameters are introduced in later
    versions.
    Also checks for existence of and difference in version number between config dict and current jrnl version,
    and if so, update the config file accordingly.
    Supply alt_config_path if using an alternate config through --config-file."""
    default_config = get_default_config()
    missing_keys = set(default_config).difference(config_data)
    if missing_keys:
        for key in missing_keys:
            config_data[key] = default_config[key]

    different_version = config_data["version"] != __version__
    if different_version:
        config_data["version"] = __version__

    if missing_keys or different_version:
        save_config(config_data, alt_config_path)
        config_path = alt_config_path if alt_config_path else get_config_path()
        print_msg(
            Message(
                MsgText.ConfigUpdated, MsgStyle.NORMAL, {"config_path": config_path}
            )
        )


def find_default_config() -> str:
    config_path = (
        get_config_path()
        if os.path.exists(get_config_path())
        else os.path.join(home_dir(), ".jrnl_config")
    )
    return config_path


def find_alt_config(alt_config: str) -> str:
    if not os.path.exists(alt_config):
        raise JrnlException(
            Message(
                MsgText.AltConfigNotFound, MsgStyle.ERROR, {"config_file": alt_config}
            )
        )

    return alt_config


def load_or_install_jrnl(alt_config_path: str) -> dict:
    """
    If jrnl is already installed, loads and returns a default config object.
    If alternate config is specified via --config-file flag, it will be used.
    Else, perform various prompts to install jrnl.
    """
    config_path = (
        find_alt_config(alt_config_path) if alt_config_path else find_default_config()
    )

    if os.path.exists(config_path):
        logging.debug("Reading configuration from file %s", config_path)
        config = load_config(config_path)

        if config is None:
            raise JrnlException(
                Message(
                    MsgText.CantParseConfigFile,
                    MsgStyle.ERROR,
                    {
                        "config_path": config_path,
                    },
                )
            )

        if is_old_version(config_path):
            from jrnl import upgrade

            upgrade.upgrade_jrnl(config_path)

        upgrade_config(config, alt_config_path)
        verify_config_colors(config)

    else:
        logging.debug("Configuration file not found, installing jrnl...")
        config = install()

    logging.debug('Using configuration:\n"%s"', pretty_repr(config))
    return config


def install() -> dict:
    _initialize_autocomplete()

    # Where to create the journal?
    default_journal_path = get_default_journal_path()
    user_given_path = print_msg(
        Message(
            MsgText.InstallJournalPathQuestion,
            MsgStyle.PROMPT,
            params={
                "default_journal_path": default_journal_path,
            },
        ),
        get_input=True,
    )
    journal_path = absolute_path(user_given_path or default_journal_path)
    default_config = get_default_config()
    default_config["journals"][DEFAULT_JOURNAL_KEY]["journal"] = journal_path

    # If the folder doesn't exist, create it
    path = os.path.split(journal_path)[0]
    with contextlib.suppress(OSError):
        os.makedirs(path)

    # Encrypt it?
    encrypt = yesno(Message(MsgText.EncryptJournalQuestion), default=False)
    if encrypt:
        default_config["encrypt"] = True
        print_msg(Message(MsgText.JournalEncrypted, MsgStyle.NORMAL))

    # Use colors?
    use_colors = yesno(Message(MsgText.UseColorsQuestion), default=True)
    if use_colors:
        default_config["colors"] = get_default_colors()

    save_config(default_config)

    print_msg(
        Message(
            MsgText.InstallComplete,
            MsgStyle.NORMAL,
            params={"config_path": get_config_path()},
        )
    )

    return default_config


def _initialize_autocomplete() -> None:
    # readline is not included in Windows Active Python and perhaps some other distributions
    if sys.modules.get("readline"):
        import readline

        readline.set_completer_delims(" \t\n;")
        readline.parse_and_bind("tab: complete")
        readline.set_completer(_autocomplete_path)


def _autocomplete_path(text: str, state: int) -> list[str | None]:
    expansions = glob.glob(expand_path(text) + "*")
    expansions = [e + "/" if os.path.isdir(e) else e for e in expansions]
    expansions.append(None)
    return expansions[state]
