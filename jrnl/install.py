#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import
import readline
import glob
import getpass
import json
import os
from . import util


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
        "default": os.path.expanduser("~/journal.txt")
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


def upgrade_config(config, config_path=os.path.expanduser("~/.jrnl_conf")):
    """Checks if there are keys missing in a given config dict, and if so, updates the config file accordingly.
    This essentially automatically ports jrnl installations if new config parameters are introduced in later
    versions."""
    missing_keys = set(default_config).difference(config)
    if missing_keys:
        for key in missing_keys:
            config[key] = default_config[key]
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print("[.jrnl_conf updated to newest version]")


def save_config(config=default_config, config_path=os.path.expanduser("~/.jrnl_conf")):
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def install_jrnl(config_path='~/.jrnl_config'):
    def autocomplete(text, state):
        expansions = glob.glob(os.path.expanduser(os.path.expandvars(text))+'*')
        expansions = [e+"/" if os.path.isdir(e) else e for e in expansions]
        expansions.append(None)
        return expansions[state]
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(autocomplete)

    # Where to create the journal?
    path_query = 'Path to your journal file (leave blank for ~/journal.txt): '
    journal_path = util.py23_input(path_query).strip() or os.path.expanduser('~/journal.txt')
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

    # Write config to ~/.jrnl_conf
    with open(config_path, 'w') as f:
        json.dump(default_config, f, indent=2)
    config = default_config
    if password:
        config['password'] = password
    return config
