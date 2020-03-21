#!/usr/bin/env python

import glob
import getpass
import os
import xdg.BaseDirectory
from . import util
from . import upgrade
from . import __version__
from .Journal import PlainJournal
from .EncryptedJournal import EncryptedJournal
from .util import UserAbort, verify_config
import yaml
import logging
import sys

if "win32" not in sys.platform:
    # readline is not included in Windows Active Python
    import readline

DEFAULT_CONFIG_NAME = "jrnl.yaml"
DEFAULT_JOURNAL_NAME = "journal.txt"
DEFAULT_JOURNAL_KEY = "default"
XDG_RESOURCE = "jrnl"

USER_HOME = os.path.expanduser("~")

CONFIG_PATH = xdg.BaseDirectory.save_config_path(XDG_RESOURCE) or USER_HOME
CONFIG_FILE_PATH = os.path.join(CONFIG_PATH, DEFAULT_CONFIG_NAME)
CONFIG_FILE_PATH_FALLBACK = os.path.join(USER_HOME, ".jrnl_config")

JOURNAL_PATH = xdg.BaseDirectory.save_data_path(XDG_RESOURCE) or USER_HOME
JOURNAL_FILE_PATH = os.path.join(JOURNAL_PATH, DEFAULT_JOURNAL_NAME)

log = logging.getLogger(__name__)


def module_exists(module_name):
    """Checks if a module exists and can be imported"""
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True


default_config = {
    "version": __version__,
    "journals": {"default": JOURNAL_FILE_PATH},
    "editor": os.getenv("VISUAL") or os.getenv("EDITOR") or "",
    "encrypt": False,
    "template": False,
    "default_hour": 9,
    "default_minute": 0,
    "timeformat": "%Y-%m-%d %H:%M",
    "tagsymbols": "@",
    "highlight": True,
    "linewrap": 79,
    "indent_character": "|",
    "colors": {"date": "none", "title": "none", "body": "none", "tags": "none",},
}


def upgrade_config(config):
    """Checks if there are keys missing in a given config dict, and if so, updates the config file accordingly.
    This essentially automatically ports jrnl installations if new config parameters are introduced in later
    versions."""
    missing_keys = set(default_config).difference(config)
    if missing_keys:
        for key in missing_keys:
            config[key] = default_config[key]
        save_config(config)
        print(
            f"[Configuration updated to newest version at {CONFIG_FILE_PATH}]",
            file=sys.stderr,
        )


def save_config(config):
    config["version"] = __version__
    with open(CONFIG_FILE_PATH, "w") as f:
        yaml.safe_dump(
            config, f, encoding="utf-8", allow_unicode=True, default_flow_style=False
        )


def load_or_install_jrnl():
    """
    If jrnl is already installed, loads and returns a config object.
    Else, perform various prompts to install jrnl.
    """
    config_path = (
        CONFIG_FILE_PATH
        if os.path.exists(CONFIG_FILE_PATH)
        else CONFIG_FILE_PATH_FALLBACK
    )
    if os.path.exists(config_path):
        log.debug("Reading configuration from file %s", config_path)
        config = util.load_config(config_path)

        try:
            upgrade.upgrade_jrnl_if_necessary(config_path)
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
        verify_config(config)

        return config
    else:
        log.debug("Configuration file not found, installing jrnl...")
        try:
            config = install()
        except KeyboardInterrupt:
            raise UserAbort("Installation aborted")
        return config


def install():
    if "win32" not in sys.platform:
        readline.set_completer_delims(" \t\n;")
        readline.parse_and_bind("tab: complete")
        readline.set_completer(autocomplete)

    # Where to create the journal?
    path_query = f"Path to your journal file (leave blank for {JOURNAL_FILE_PATH}): "
    journal_path = input(path_query).strip() or JOURNAL_FILE_PATH
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
    encrypt = util.yesno(
        "Do you want to encrypt your journal? You can always change this later",
        default=False,
    )
    if encrypt:
        default_config["encrypt"] = True
        print("Journal will be encrypted.", file=sys.stderr)

    save_config(default_config)
    return default_config


def autocomplete(text, state):
    expansions = glob.glob(os.path.expanduser(os.path.expandvars(text)) + "*")
    expansions = [e + "/" if os.path.isdir(e) else e for e in expansions]
    expansions.append(None)
    return expansions[state]
