#!/usr/bin/env python

import sys
import os
import getpass as gp
import yaml
if "win32" in sys.platform:
    import colorama
    colorama.init()
import re
import tempfile
import subprocess
import unicodedata
import shlex
import logging

log = logging.getLogger(__name__)

WARNING_COLOR = "\033[33m"
ERROR_COLOR = "\033[31m"
RESET_COLOR = "\033[0m"

# Based on Segtok by Florian Leitner
# https://github.com/fnl/segtok
SENTENCE_SPLITTER = re.compile(r"""
(                       # A sentence ends at one of two sequences:
    [.!?\u203C\u203D\u2047\u2048\u2049\u3002\uFE52\uFE57\uFF01\uFF0E\uFF1F\uFF61]                # Either, a sequence starting with a sentence terminal,
    [\'\u2019\"\u201D]? # an optional right quote,
    [\]\)]*             # optional closing brackets and
    \s+                 # a sequence of required spaces.
|                       # Otherwise,
    \n                  # a sentence also terminates newlines.
)""", re.VERBOSE)


class UserAbort(Exception):
    pass


getpass = gp.getpass


def get_password(validator, keychain=None, max_attempts=3):
    pwd_from_keychain = keychain and get_keychain(keychain)
    password = pwd_from_keychain or getpass()
    result = validator(password)
    # Password is bad:
    if result is None and pwd_from_keychain:
        set_keychain(keychain, None)
    attempt = 1
    while result is None and attempt < max_attempts:
        print("Wrong password, try again.", file=sys.stderr)
        password = gp.getpass()
        result = validator(password)
        attempt += 1
    if result is not None:
        return result
    else:
        print("Extremely wrong password.", file=sys.stderr)
        sys.exit(1)


def get_keychain(journal_name):
    import keyring
    try:
        return keyring.get_password('jrnl', journal_name)
    except RuntimeError:
        return ""


def set_keychain(journal_name, password):
    import keyring
    if password is None:
        try:
            keyring.delete_password('jrnl', journal_name)
        except RuntimeError:
            pass
    else:
        keyring.set_password('jrnl', journal_name, password)


def yesno(prompt, default=True):
    prompt = f"{prompt.strip()} {'[Y/n]' if default else '[y/N]'} "
    response = input(prompt)
    return {"y": True, "n": False}.get(response.lower(), default)


def load_config(config_path):
    """Tries to load a config file from YAML.
    """
    with open(config_path) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def scope_config(config, journal_name):
    if journal_name not in config['journals']:
        return config
    config = config.copy()
    journal_conf = config['journals'].get(journal_name)
    if type(journal_conf) is dict:  # We can override the default config on a by-journal basis
        log.debug('Updating configuration with specific journal overrides %s', journal_conf)
        config.update(journal_conf)
    else:  # But also just give them a string to point to the journal file
        config['journal'] = journal_conf
    config.pop('journals')
    return config


def get_text_from_editor(config, template=""):
    filehandle, tmpfile = tempfile.mkstemp(prefix="jrnl", text=True, suffix=".txt")
    with open(tmpfile, 'w', encoding="utf-8") as f:
        if template:
            f.write(template)
    try:
        subprocess.call(shlex.split(config['editor'], posix="win" not in sys.platform) + [tmpfile])
    except AttributeError:
        subprocess.call(config['editor'] + [tmpfile])
    with open(tmpfile, "r", encoding="utf-8") as f:
        raw = f.read()
    os.close(filehandle)
    os.remove(tmpfile)
    if not raw:
        print('[Nothing saved to file]', file=sys.stderr)
    return raw


def colorize(string):
    """Returns the string wrapped in cyan ANSI escape"""
    return f"\033[36m{string}\033[39m"


def slugify(string):
    """Slugifies a string.
    Based on public domain code from https://github.com/zacharyvoase/slugify
    """
    normalized_string = str(unicodedata.normalize('NFKD', string))
    no_punctuation = re.sub(r'[^\w\s-]', '', normalized_string).strip().lower()
    slug = re.sub(r'[-\s]+', '-', no_punctuation)
    return slug


def split_title(text):
    """Splits the first sentence off from a text."""
    punkt = SENTENCE_SPLITTER.search(text)
    if not punkt:
        return text, ""
    return text[:punkt.end()].strip(), text[punkt.end():].strip()
