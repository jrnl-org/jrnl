#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import
import readline
import glob
import getpass
import os
import xdg.BaseDirectory
from . import util
from . import upgrade
from . import __version__
from .Journal import PlainJournal
from .EncryptedJournal import EncryptedJournal
import yaml
import logging

DEFAULT_CONFIG_NAME = 'jrnl.yaml'
DEFAULT_JOURNAL_NAME = 'journal.txt'
XDG_RESOURCE = 'jrnl'

USER_HOME = os.path.expanduser('~')

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
    'version': __version__,
    'journals': {
        "default": JOURNAL_FILE_PATH
    },
    'editor': os.getenv('VISUAL') or os.getenv('EDITOR') or "",
    'encrypt': False,
    'template': False,
    'default_hour': 9,
    'default_minute': 0,
    'timeformat': "%Y-%m-%d %H:%M",
    'tagsymbols': '@',
    'highlight': True,
    'linewrap': 79,
}


def upgrade_config(config):
    """Checks if there are keys missing in a given config dict, and if so, updates the config file accordingly.
    This essentially automatically ports jrnl installations if new config parameters are introduced in later
    versions."""
    missing_keys = set(default_config).difference(config)
    if missing_keys or config['version'] != __version__:
        for key in missing_keys:
            config[key] = default_config[key]
        save_config(config)
        print("[Configuration updated to newest version at {}]".format(CONFIG_FILE_PATH))


def save_config(config):
    config['version'] = __version__
    with open(CONFIG_FILE_PATH, 'w') as f:
        yaml.safe_dump(config, f, encoding='utf-8', allow_unicode=True, default_flow_style=False)


def load_or_install_jrnl():
    """
    If jrnl is already installed, loads and returns a config object.
    Else, perform various prompts to install jrnl.
    """
    config_path = CONFIG_FILE_PATH if os.path.exists(CONFIG_FILE_PATH) else CONFIG_FILE_PATH_FALLBACK
    if os.path.exists(config_path):
        log.debug('Reading configuration from file %s', config_path)
        config = util.load_config(config_path)
        upgrade.upgrade_jrnl_if_necessary(config_path)
        upgrade_config(config)
        return config
    else:
        log.debug('Configuration file not found, installing jrnl...')
        return install()

def create(journal_name, default_journal_file_path=None, config=None):
    def autocomplete(text, state):
        expansions = glob.glob(os.path.expanduser(os.path.expandvars(text)) + '*')
        expansions = [e + "/" if os.path.isdir(e) else e for e in expansions]
        expansions.append(None)
        return expansions[state]
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(autocomplete)

    # Take the default config if none is provided
    if config is None:
        config = default_config

    # Set up the default journal file path
    if default_journal_file_path is None:
        default_journal_file_path = JOURNAL_FILE_PATH

    # Where to create the journal?
    path_query = 'Path to your journal file (leave blank for {}): '.format(default_journal_file_path)
    journal_path = util.py23_input(path_query).strip() or \
                   default_journal_file_path
    journal_path = os.path.expanduser(os.path.expandvars(journal_path))
    config['journals'][journal_name] = {'journal': journal_path}

    # if the provided filename already taken, ask what to do
    if os.path.exists(journal_path) and not util.yesno("File {} already exists. Do you still want to use it?".format(journal_path), default=False):
        sys.exit(1)

    path = os.path.split(config['journals'][journal_name]['journal'])[0]  # If the folder doesn't exist, create it
    try:
        os.makedirs(path)
    except OSError:
        pass

    # Encrypt it?
    password = getpass.getpass("Enter password for journal (leave blank for no encryption): ")
    if password:
        config['journals'][journal_name]['password'] = password
        config['journals'][journal_name]['encrypt'] = True
        if util.yesno("Do you want to store the password in your keychain?", default=True):
            util.set_keychain(journal_name, password)
        else:
            util.set_keychain(journal_name, None)
        EncryptedJournal._create(journal_path, password)
        print("Journal will be encrypted.")
    else:
        PlainJournal._create(journal_path)

    save_config(config)
    return config

def install():
    return create('default')
