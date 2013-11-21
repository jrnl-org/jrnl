#!/usr/bin/env python
# encoding: utf-8
import sys
import os
from tzlocal import get_localzone
import getpass as gp
import keyring
import pytz
try: import simplejson as json
except ImportError: import json
import re

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
    return s if PY3 or type(s) is unicode else unicode(s, "unicode_escape")

def prompt(msg):
    """Prints a message to the std err stream defined in util."""
    if not msg.endswith("\n"):
        msg += "\n"
    STDERR.write(u(msg))

def py23_input(msg):
    STDERR.write(u(msg))
    return STDIN.readline().strip()

def yesno(prompt, default=True):
    prompt = prompt.strip() + (" [Y/n]" if default else " [y/N]")
    raw = py23_input(prompt)
    return {'y': True, 'n': False}.get(raw.lower(), default)

def get_local_timezone():
    """Returns the Olson identifier of the local timezone.
    In a happy world, tzlocal.get_localzone would do this, but there's a bug on OS X
    that prevents that right now: https://github.com/regebro/tzlocal/issues/6"""
    global __cached_tz
    if not __cached_tz and "darwin" in sys.platform:
        __cached_tz = os.popen("systemsetup -gettimezone").read().replace("Time Zone: ", "").strip()
        if not __cached_tz or __cached_tz not in pytz.all_timezones_set:
            link = os.readlink("/etc/localtime")
            # This is something like /usr/share/zoneinfo/America/Los_Angeles.
            # Find second / from right and take the substring
            __cached_tz = link[link.rfind('/', 0, link.rfind('/'))+1:]
    elif not __cached_tz:
        __cached_tz = str(get_localzone())
    if not __cached_tz or __cached_tz not in pytz.all_timezones_set:
        __cached_tz = "UTC"
    return __cached_tz

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

