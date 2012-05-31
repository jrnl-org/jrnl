#!/usr/bin/env python
# encoding: utf-8

"""
    jrnl

    license: MIT, see LICENSE for more details.
"""

import Journal
from install import *
import os
import tempfile
import subprocess
import argparse
import sys
try: import simplejson as json
except ImportError: import json


__title__ = 'jrnl'
__version__ = '0.3.0'
__author__ = 'Manuel Ebert, Stephan Gabler'
__license__ = 'MIT'

CONFIG_PATH = os.path.expanduser('~/.jrnl_config')
PYCRYPTO = module_exists("Crypto")

def update_config(config):
    """Checks if there are keys missing in a given config dict, and if so, updates the config file accordingly.
    This essentially automatically ports jrnl installations if new config parameters are  introduced in later
    versions."""
    missing_keys = set(default_config).difference(config)
    if missing_keys:
        for key in missing_keys:
            config[key] = default_config[key]
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)

def parse_args():
    parser = argparse.ArgumentParser()
    composing = parser.add_argument_group('Composing', 'Will make an entry out of whatever follows as arguments')
    composing.add_argument('-date', dest='date', help='Date, e.g. "yesterday at 5pm"')
    composing.add_argument('text', metavar='text', nargs="*",  help='Log entry (or tags by which to filter in viewing mode)')

    reading = parser.add_argument_group('Reading', 'Specifying either of these parameters will display posts of your journal')
    reading.add_argument('-from', dest='start_date', metavar="DATE", help='View entries after this date')
    reading.add_argument('-to', dest='end_date', metavar="DATE", help='View entries before this date')
    reading.add_argument('-and', dest='strict', action="store_true", help='Filter by tags using AND (default: OR)')
    reading.add_argument('-n', dest='limit', default=None, metavar="N", help='Shows the last n entries matching the filter', nargs="?", type=int)
    reading.add_argument('-short', dest='short', action="store_true", help='Show only titles or line containing the search tags')

    exporting = parser.add_argument_group('Export / Import', 'Options for transmogrifying your journal')
    exporting.add_argument('--tags', dest='tags', action="store_true", help='Returns a list of all tags and number of occurences')
    exporting.add_argument('--json', dest='json', action="store_true", help='Returns a JSON-encoded version of the Journal')
    exporting.add_argument('--markdown', dest='markdown', action="store_true", help='Returns a Markdown-formated version of the Journal')
    exporting.add_argument('--encrypt',  metavar='FILENAME', dest='encrypt', help='Encrypts your existing journal with a new password', nargs='?', default=False, const=None)
    exporting.add_argument('--decrypt',  metavar='FILENAME', dest='decrypt', help='Decrypts your journal and stores it in plain text', nargs='?', default=False, const=None)

    return parser.parse_args()

def guess_mode(args, config):
    """Guesses the mode (compose, read or export) from the given arguments"""
    compose = True
    export = False
    if args.json or args.decrypt is not False or args.encrypt is not False or args.markdown or args.tags:
        compose = False
        export = True
    elif args.start_date or args.end_date or args.limit or args.strict or args.short:
        # Any sign of displaying stuff?
        compose = False
    elif not args.date and args.text and all(word[0] in config['tagsymbols'] for word in args.text):
        # No date and only tags?
        compose = False

    return compose, export

def get_text_from_editor(config):
    tmpfile = os.path.join(tempfile.gettempdir(), "jrnl")
    subprocess.call(config['editor'].split() + [tmpfile])
    if os.path.exists(tmpfile):
        with open(tmpfile) as f:
            raw = f.read()
        os.remove(tmpfile)
    else:
        print('nothing saved to file')
        raw = ''

    return raw


def encrypt(journal, filename=None):
    """ Encrypt into new file. If filename is not set, we encrypt the journal file itself. """
    journal.make_key(prompt="Enter new password:")
    journal.config['encrypt'] = True
    journal.config['password'] = ""
    if not filename:
        journal.write()
        journal.save_config(CONFIG_PATH)
        print("Journal encrypted to %s." % journal.config['journal'])
    else:
        journal.write(filename)
        print("Journal encrypted to %s." % os.path.realpath(filename))       

def decrypt(journal, filename=None):
    """ Decrypts into new file. If filename is not set, we encrypt the journal file itself. """
    journal.config['encrypt'] = False
    journal.config['password'] = ""
    if not filename:
        journal.write()
        journal.save_config()
        print("Journal decrypted to %s." % journal.config['journal'])
    else:
        journal.write(filename)
        print("Journal encrypted to %s." % os.path.realpath(filename))       

def print_tags(journal):
        """Prints a list of all tags and the number of occurances."""
        # Astute reader: should the following line leave you as puzzled as me the first time
        # I came across this construction, worry not and embrace the ensuing moment of enlightment.
        tags = [tag
            for entry in journal.entries
            for tag in set(entry.tags)
        ]
        # To be read: [for entry in journal.entries: for tag in set(entry.tags): tag]
        tag_counts = {(tags.count(tag), tag) for tag in tags}
        for n, tag in sorted(tag_counts, reverse=True):
            print("{:20} : {}".format(tag, n))

def cli():
    if not os.path.exists(CONFIG_PATH):
        config = install_jrnl(CONFIG_PATH)
    else:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        update_config(config)

    # check if the configuration is supported by available modules
    if config['encrypt'] and not PYCRYPTO:
        print("According to your jrnl_conf, your journal is encrypted, however PyCrypto was not found. To open your journal, install the PyCrypto package from http://www.pycrypto.org.")
        sys.exit(-1)

    args = parse_args()
    mode_compose, mode_export = guess_mode(args, config)

    # open journal file
    journal = Journal.Journal(config=config)

    if mode_compose and not args.text:
        if config['editor']:
            raw = get_text_from_editor(config)
        else:
            raw = raw_input("Compose Entry: ")
        if raw:
            args.text = [raw]
        else:
            mode_compose = False

    # Writing mode
    if mode_compose:
        raw = " ".join(args.text).strip()
        journal.new_entry(raw, args.date)
        print("Entry added.")
        journal.write()

    # Reading mode
    elif not mode_export:
        journal.filter(tags=args.text,
                       start_date=args.start_date, end_date=args.end_date,
                       strict=args.strict,
                       short=args.short)
        journal.limit(args.limit)
        print(journal)

    # Various export modes
    elif args.tags: 
        print_tags(journal)

    elif args.json: # export to json
        print(journal.to_json())

    elif args.markdown: # export to json
        print(journal.to_md())

    elif (args.encrypt is not False or args.decrypt is not False) and not PYCRYPTO:
        print("PyCrypto not found. To encrypt or decrypt your journal, install the PyCrypto package from http://www.pycrypto.org.")

    elif args.encrypt is not False:
        encrypt(journal, filename=args.encrypt)

    elif args.decrypt is not False:
        decrypt(journal, filename=args.decrypt)


if __name__ == "__main__":
    cli()

 