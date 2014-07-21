#!/usr/bin/env python
# encoding: utf-8
import sys
import os
import getpass as gp
import keyring
import json
if "win32" in sys.platform:
    import colorama
    colorama.init()
import re
import tempfile
import subprocess
import codecs
import unicodedata

PY3 = sys.version_info[0] == 3
PY2 = sys.version_info[0] == 2
STDIN = sys.stdin
STDERR = sys.stderr
STDOUT = sys.stdout
TEST = False
__cached_tz = None


def getpass(prompt="Password: "):
    if not TEST:
        return gp.getpass(prompt)
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
    return keyring.get_password('jrnl', journal_name)

def set_keychain(journal_name, password):
    if password is None:
        try:
            keyring.delete_password('jrnl', journal_name)
        except:
            pass
    elif not TEST:
        keyring.set_password('jrnl', journal_name, password)

def u(s):
    """Mock unicode function for python 2 and 3 compatibility."""
    return s if PY3 or type(s) is unicode else unicode(s.encode('string-escape'), "unicode_escape")

def py2encode(s):
    """Encode in Python 2, but not in python 3."""
    return s.encode("utf-8") if PY2 and type(s) is unicode else s

def prompt(msg):
    """Prints a message to the std err stream defined in util."""
    if not msg.endswith("\n"):
        msg += "\n"
    STDERR.write(u(msg))

def py23_input(msg=""):
    STDERR.write(u(msg))
    return STDIN.readline().strip()

def py23_read(msg=""):
    return STDIN.read()

def yesno(prompt, default=True):
    prompt = prompt.strip() + (" [Y/n]" if default else " [y/N]")
    raw = py23_input(prompt)
    return {'y': True, 'n': False}.get(raw.lower(), default)

def load_and_fix_json(json_path):
    """Tries to load a json object from a file.
    If that fails, tries to fix common errors (no or extra , at end of the line).
    """
    with open(json_path) as f:
        json_str = f.read()
    config = fixed = None
    try:
        return json.loads(json_str)
    except ValueError as e:
        # Attempt to fix extra ,
        json_str = re.sub(r",[ \n]*}", "}", json_str)
        # Attempt to fix missing ,
        json_str = re.sub(r"([^{,]) *\n *(\")", r"\1,\n \2", json_str)
        try:
            config = json.loads(json_str)
            with open(json_path, 'w') as f:
                json.dump(config, f, indent=2)
            prompt("[Some errors in your jrnl config have been fixed for you.]")
            return config
        except ValueError as e:
            prompt("[There seems to be something wrong with your jrnl config at {0}: {1}]".format(json_path, e.message))
            prompt("[Entry was NOT added to your journal]")
            sys.exit(1)

def get_text_from_editor(config, template=""):
    tmpfile = os.path.join(tempfile.mktemp(prefix="jrnl"))
    with codecs.open(tmpfile, 'w', "utf-8") as f:
        if template:
            f.write(template)
    subprocess.call(config['editor'].split() + [tmpfile])
    with codecs.open(tmpfile, "r", "utf-8") as f:
        raw = f.read()
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
