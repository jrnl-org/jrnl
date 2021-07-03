# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html


import glob
import logging
import os
import sys

from .config import DEFAULT_JOURNAL_KEY
from .config import get_config_path
from .config import get_default_config
from .config import get_default_journal_path
from .config import load_config
from .config import save_config
from .config import verify_config_colors
from .exception import UserAbort
from .prompt import yesno
from .upgrade import is_old_version


def upgrade_config(config):
    """Checks if there are keys missing in a given config dict, and if so, updates the config file accordingly.
    This essentially automatically ports jrnl installations if new config parameters are introduced in later
    versions."""
    default_config = get_default_config()
    missing_keys = set(default_config).difference(config)
    if missing_keys:
        for key in missing_keys:
            config[key] = default_config[key]
        save_config(config)
        print(
            f"[Configuration updated to newest version at {get_config_path()}]",
            file=sys.stderr,
        )


def load_or_install_jrnl():
    """
    If jrnl is already installed, loads and returns a config object.
    Else, perform various prompts to install jrnl.
    """
    config_path = (
        get_config_path()
        if os.path.exists(get_config_path())
        else os.path.join(os.path.expanduser("~"), ".jrnl_config")
    )

    if os.path.exists(config_path):
        logging.debug("Reading configuration from file %s", config_path)
        config = load_config(config_path)

        if is_old_version(config_path):
            from . import upgrade

            try:
                upgrade.upgrade_jrnl(config_path)
            except upgrade.UpgradeValidationException:
                print("Aborting upgrade.", file=sys.stderr)
                print(
                    "Please tell us about this problem at the following URL:",
                    file=sys.stderr,
                )
                print(
                    "https://github.com/jrnl-org/jrnl/issues/new?title=UpgradeValidationException",
                    file=sys.stderr,
                )
                print("Exiting.", file=sys.stderr)
                sys.exit(1)

        upgrade_config(config)
        verify_config_colors(config)

    else:
        logging.debug("Configuration file not found, installing jrnl...")
        try:
            config = install()
        except KeyboardInterrupt:
            raise UserAbort("Installation aborted")

    logging.debug('Using configuration "%s"', config)
    return config


def install():
    _initialize_autocomplete()

    # Where to create the journal?
    default_journal_path = get_default_journal_path()
    path_query = f"Path to your journal file (leave blank for {default_journal_path}): "
    journal_path = os.path.abspath(input(path_query).strip() or default_journal_path)
    default_config = get_default_config()
    default_config["journals"][DEFAULT_JOURNAL_KEY] = os.path.expanduser(
        os.path.expandvars(journal_path)
    )

    # If the folder doesn't exist, create it
    path = os.path.split(default_config["journals"][DEFAULT_JOURNAL_KEY])[0]
    try:
        os.makedirs(path)
    except OSError:
        pass

    # Encrypt it?
    encrypt = yesno(
        "Do you want to encrypt your journal? You can always change this later",
        default=False,
    )
    if encrypt:
        default_config["encrypt"] = True
        print("Journal will be encrypted.", file=sys.stderr)

    save_config(default_config)
    return default_config


def _initialize_autocomplete():
    # readline is not included in Windows Active Python and perhaps some other distributions
    if sys.modules.get("readline"):
        import readline

        readline.set_completer_delims(" \t\n;")
        readline.parse_and_bind("tab: complete")
        readline.set_completer(_autocomplete_path)


def _autocomplete_path(text, state):
    expansions = glob.glob(os.path.expanduser(os.path.expandvars(text)) + "*")
    expansions = [e + "/" if os.path.isdir(e) else e for e in expansions]
    expansions.append(None)
    return expansions[state]
