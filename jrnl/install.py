#!/usr/bin/env python
# encoding: utf-8

import readline, glob
import getpass
try: import simplejson as json
except ImportError: import json
import os

def module_exists(module_name):
    """Checks if a module exists and can be imported"""
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

default_config = {
    'journal': os.path.expanduser("~/journal.txt"),
    'editor': "",
    'encrypt': False,
    'password': "",
    'default_hour': 9,
    'default_minute': 0,
    'timeformat': "%Y-%m-%d %H:%M",
    'tagsymbols': '@',
    'highlight': True,
    'linewrap': 80,
}


def install_jrnl(config_path='~/.jrnl_config'):
    def autocomplete(text, state):
        expansions = glob.glob(os.path.expanduser(text)+'*')
        expansions = [e+"/" if os.path.isdir(e) else e for e in expansions]
        expansions.append(None)
        return expansions[state]
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(autocomplete)

    # Where to create the journal?
    path_query = 'Path to your journal file (leave blank for ~/journal.txt): '
    journal_path = raw_input(path_query).strip() or os.path.expanduser('~/journal.txt')
    default_config['journal'] = os.path.expanduser(journal_path)

    # Encrypt it?
    if module_exists("Crypto"):
        password = getpass.getpass("Enter password for journal (leave blank for no encryption): ")
        if password:
            default_config['encrypt'] = True
            print("Journal will be encrypted.")
            print("If you want to, you can store your password in .jrnl_config and will never be bothered about it again.")
    else:
        password = None
        print("PyCrypto not found. To encrypt your journal, install the PyCrypto package from http://www.pycrypto.org and run 'jrnl --encrypt'. For now, your journal will be stored in plain text.")

    # Use highlighting:
    if module_exists("clint"):
        print("clint not found. To turn on highlighting, install clint and set highlight to true in your .jrnl_conf.")
        default_config['highlight'] = False

    open(default_config['journal'], 'a').close() # Touch to make sure it's there

    # Write config to ~/.jrnl_conf
    with open(config_path, 'w') as f:
        json.dump(default_config, f, indent=2)
    config = default_config
    if password:
        config['password'] = password
    return config

    