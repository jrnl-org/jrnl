#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import
import readline
import glob
import getpass
import os
import xdg.BaseDirectory
from . import util
import yaml

DEFAULT_CONFIG_NAME = 'jrnl.yaml'
DEFAULT_JOURNAL_NAME = 'journal.txt'
XDG_RESOURCE = 'jrnl'

USER_HOME = os.path.expanduser('~')

CONFIG_PATH = xdg.BaseDirectory.save_config_path(XDG_RESOURCE) or USER_HOME
CONFIG_FILE_PATH = os.path.join(CONFIG_PATH, DEFAULT_CONFIG_NAME)
CONFIG_FILE_PATH_FALLBACK = os.path.join(USER_HOME, ".jrnl_config")

JOURNAL_PATH = xdg.BaseDirectory.save_data_path(XDG_RESOURCE) or USER_HOME
JOURNAL_FILE_PATH = os.path.join(JOURNAL_PATH, DEFAULT_JOURNAL_NAME)


def module_exists(module_name):
    """Checks if a module exists and can be imported"""
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

default_config = {
    'journals': {
        "default": JOURNAL_FILE_PATH
    },
    'editor': os.getenv('VISUAL') or os.getenv('EDITOR') or "",
    'encrypt': False,
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
    if missing_keys:
        for key in missing_keys:
            config[key] = default_config[key]
        save_config(config)
        print("[.jrnl_conf updated to newest version]")


def save_config(config):
    yaml.safe_dump(config, file(CONFIG_FILE_PATH, 'w'), encoding='utf-8', allow_unicode=True, default_flow_style=False)


def install_jrnl():
    """
    If jrnl is already installed, loads and returns a config object.
    Else, perform various prompts to install jrnl.
    """
    if os.path.exists(CONFIG_FILE_PATH):
        config = util.load_config(CONFIG_FILE_PATH)
        upgrade_config(config)
        return config
    elif os.path.exists(CONFIG_FILE_PATH_FALLBACK):  # Backwards compatibility with jrnl 1.x
        config = util.load_config(CONFIG_FILE_PATH_FALLBACK)
        upgrade_config(config)
        save_config(config)
        return config

    def autocomplete(text, state):
        expansions = glob.glob(os.path.expanduser(os.path.expandvars(text)) + '*')
        expansions = [e + "/" if os.path.isdir(e) else e for e in expansions]
        expansions.append(None)
        return expansions[state]
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(autocomplete)

    # Where to create the journal?
    path_query = 'Path to your journal file (leave blank for {}): '.format(JOURNAL_FILE_PATH)
    journal_path = util.py23_input(path_query).strip() or JOURNAL_FILE_PATH
    default_config['journals']['default'] = os.path.expanduser(os.path.expandvars(journal_path))

    # Encrypt it?
    if module_exists("Crypto"):
        password = getpass.getpass("Enter password for journal (leave blank for no encryption): ")
        if password:
            default_config['encrypt'] = True
            if util.yesno("Do you want to store the password in your keychain?", default=True):
                util.set_keychain("default", password)
            else:
                util.set_keychain("default", None)
            print("Journal will be encrypted.")
    else:
        password = None
        print("PyCrypto not found. To encrypt your journal, install the PyCrypto package from http://www.pycrypto.org or with 'pip install pycrypto' and run 'jrnl --encrypt'. For now, your journal will be stored in plain text.")

    path = os.path.split(default_config['journals']['default'])[0]  # If the folder doesn't exist, create it
    try:
        os.makedirs(path)
    except OSError:
        pass

    open(default_config['journals']['default'], 'a').close()  # Touch to make sure it's there

    save_config(config)
    config = default_config
    if password:
        config['password'] = password
    return config
