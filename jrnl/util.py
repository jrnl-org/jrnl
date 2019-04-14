#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

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
import codecs
import unicodedata
import shlex
import logging

log = logging.getLogger(__name__)


PY3 = sys.version_info[0] == 3
PY2 = sys.version_info[0] == 2
STDIN = sys.stdin
STDERR = sys.stderr
STDOUT = sys.stdout
TEST = False
__cached_tz = None

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
)""", re.UNICODE | re.VERBOSE)


def getpass(prompt="Password: "):
    if not TEST:
        return gp.getpass(bytes(prompt))
    else:
        return py23_input(prompt)


def get_password(validator, keychain=None, max_attempts=3):
    pwd_from_keychain = keychain and get_keychain(keychain)
    password = pwd_from_keychain or getpass()
    result = validator(password)
    # Password is bad:
    if result is None and pwd_from_keychain:
        set_keychain(keychain, None)
    attempt = 1
    while result is None and attempt < max_attempts:
        prompt("Wrong password, try again.")
        password = getpass()
        result = validator(password)
        attempt += 1
    if result is not None:
        return result
    else:
        prompt("Extremely wrong password.")
        sys.exit(1)


def get_keychain(journal_name):
    import keyring
    return keyring.get_password('jrnl', journal_name)


def set_keychain(journal_name, password):
    import keyring
    if password is None:
        try:
            keyring.delete_password('jrnl', journal_name)
        except:
            pass
    elif not TEST:
        keyring.set_password('jrnl', journal_name, password)


def u(s):
    """Mock unicode function for python 2 and 3 compatibility."""
    if not isinstance(s, str):
        s = str(s)
    return s if PY3 or type(s) is unicode else s.decode("utf-8")


def py2encode(s):
    """Encodes to UTF-8 in Python 2 but not in Python 3."""
    return s.encode("utf-8") if PY2 and type(s) is unicode else s


def bytes(s):
    """Returns bytes, no matter what."""
    if PY3:
        return s.encode("utf-8") if type(s) is not bytes else s
    return s.encode("utf-8") if type(s) is unicode else s


def prnt(s):
    """Encode and print a string"""
    STDOUT.write(u(s + "\n"))


def prompt(msg):
    """Prints a message to the std err stream defined in util."""
    if not msg.endswith("\n"):
        msg += "\n"
    STDERR.write(u(msg))


def py23_input(msg=""):
    prompt(msg)
    return STDIN.readline().strip()


def py23_read(msg=""):
    print(msg)
    return STDIN.read()


def yesno(prompt, default=True):
    prompt = prompt.strip() + (" [Y/n]" if default else " [y/N]")
    raw = py23_input(prompt)
    return {'y': True, 'n': False}.get(raw.lower(), default)


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
    with codecs.open(tmpfile, 'w', "utf-8") as f:
        if template:
            f.write(template)
    try:
        subprocess.call(shlex.split(config['editor'], posix="win" not in sys.platform) + [tmpfile])
    except AttributeError:
        subprocess.call(config['editor'] + [tmpfile])
    with codecs.open(tmpfile, "r", "utf-8") as f:
        raw = f.read()
    os.close(filehandle)
    os.remove(tmpfile)
    if not raw:
        prompt('[Nothing saved to file]')
    return raw


def colorize(string):
    """Returns the string wrapped in cyan ANSI escape"""
    return u"\033[36m{}\033[39m".format(string)


def slugify(string):
    """Slugifies a string.
    Based on public domain code from https://github.com/zacharyvoase/slugify
    and ported to deal with all kinds of python 2 and 3 strings
    """
    string = u(string)
    ascii_string = str(unicodedata.normalize('NFKD', string).encode('ascii', 'ignore'))
    if PY3:
        ascii_string = ascii_string[1:]     # removed the leading 'b'
    no_punctuation = re.sub(r'[^\w\s-]', '', ascii_string).strip().lower()
    slug = re.sub(r'[-\s]+', '-', no_punctuation)
    return u(slug)


def int2byte(i):
    """Converts an integer to a byte.
    This is equivalent to chr() in Python 2 and bytes((i,)) in Python 3."""
    return chr(i) if PY2 else bytes((i,))


def byte2int(b):
    """Converts a byte to an integer.
    This is equivalent to ord(bs[0]) on Python 2 and bs[0] on Python 3."""
    return ord(b)if PY2 else b


def split_title(text):
    """Splits the first sentence off from a text."""
    punkt = SENTENCE_SPLITTER.search(text)
    if not punkt:
        return text, ""
    return text[:punkt.end()].strip(), text[punkt.end():].strip()
