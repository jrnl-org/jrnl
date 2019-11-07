#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import sys
import os
import getpass as gp
import yaml
import colorama
if "win32" in sys.platform:
    colorama.init()
import re
import tempfile
import subprocess
import codecs
import unicodedata
import shlex
from string import punctuation
import logging

log = logging.getLogger(__name__)


PY3 = sys.version_info[0] == 3
PY2 = sys.version_info[0] == 2
STDIN = sys.stdin
STDERR = sys.stderr
STDOUT = sys.stdout
TEST = False
__cached_tz = None

WARNING_COLOR = colorama.Fore.YELLOW
ERROR_COLOR = colorama.Fore.RED
RESET_COLOR = colorama.Fore.RESET

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


class UserAbort(Exception):
    pass


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


def verify_config(config):
    """
    Ensures the keys set for colors are valid colorama.Fore attributes, or "None"
    :return: True if all keys are set correctly, False otherwise
    """
    all_valid_colors = True
    for key, color in config["colors"].items():
        upper_color = color.upper()
        if upper_color == "NONE":
            continue
        if not getattr(colorama.Fore, upper_color, None):
            print("[{2}ERROR{3}: {0} set to invalid color: {1}]".format(key, color, ERROR_COLOR, RESET_COLOR), file=sys.stderr)
            all_valid_colors = False
    return all_valid_colors


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


def colorize(string, color, bold=False):
    """Returns the string colored with colorama.Fore.color. If the color set by
    the user is "NONE" or the color doesn't exist in the colorama.Fore attributes,
    it returns the string without any modification."""
    color_escape = getattr(colorama.Fore, color.upper(), None)
    if not color_escape:
        return string

    if not bold:
        return color_escape + string + colorama.Fore.RESET
    else:
        return colorama.Style.BRIGHT + color_escape + string + colorama.Style.RESET_ALL


def highlight_tags_with_background_color(entry, text, color, bold=False):
    """
    Takes a string and colorizes the tags in it based upon the config value for
    color.tags, while colorizing the rest of the text based on `color`.
    :param entry: Entry object, for access to journal config
    :param text: Text to be colorized
    :param color: Color for non-tag text, passed to colorize()
    :param bold: Bold flag text, passed to colorize()
    :return: Colorized str
    """
    def colorized_text_generator(fragments):
        """Efficiently generate colorized tags / text from text fragments.
        Taken from @shobrook. Thanks, buddy :)
        :param fragments: List of strings representing parts of entry (tag or word).
        :rtype: List of tuples
        :returns [(colorized_str, original_str)]"""
        for fragment in fragments:
            for part in fragment.strip().split(" "):
                part = part.strip()
                if part and part[0] not in config['tagsymbols']:
                    yield (colorize(part, color, bold), part)
                elif part:
                    yield (colorize(part, config['colors']['tags'], not bold), part)

    config = entry.journal.config
    if config['highlight']:  # highlight tags
        if entry.journal.search_tags:
            text_fragments = []
            for tag in entry.search_tags:
                text_fragments.append(re.split(re.compile(re.escape(tag), re.IGNORECASE),
                                               text,
                                               flags=re.UNICODE))
        else:
            text_fragments = re.split(entry.tag_regex(config['tagsymbols']), text)

        final_text = ""
        previous_piece = ""
        for colorized_piece, piece in colorized_text_generator(text_fragments):
            if piece in punctuation and previous_piece[0] not in config['tagsymbols']:
                final_text = final_text.strip() + colorized_piece
            else:
                final_text += colorized_piece + " "

            previous_piece = piece

        return final_text
    else:
        return text


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
