#!/usr/bin/env python

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
import unicodedata
import shlex
from string import punctuation, whitespace
import logging
from typing import Optional, Callable

log = logging.getLogger(__name__)

WARNING_COLOR = colorama.Fore.YELLOW
ERROR_COLOR = colorama.Fore.RED
RESET_COLOR = colorama.Fore.RESET

# Based on Segtok by Florian Leitner
# https://github.com/fnl/segtok
SENTENCE_SPLITTER = re.compile(
    r"""
(                       # A sentence ends at one of two sequences:
    [.!?\u203C\u203D\u2047\u2048\u2049\u3002\uFE52\uFE57\uFF01\uFF0E\uFF1F\uFF61]                # Either, a sequence starting with a sentence terminal,
    [\'\u2019\"\u201D]? # an optional right quote,
    [\]\)]*             # optional closing brackets and
    \s+                 # a sequence of required spaces.
|                       # Otherwise,
    \n                  # a sentence also terminates newlines.
)""",
    re.VERBOSE,
)


class UserAbort(Exception):
    pass


def create_password(
    journal_name: str, prompt: str = "Enter password for new journal: "
) -> str:
    while True:
        pw = gp.getpass(prompt)
        if not pw:
            print("Password can't be an empty string!", file=sys.stderr)
            continue
        elif pw == gp.getpass("Enter password again: "):
            break

        print("Passwords did not match, please try again", file=sys.stderr)

    if yesno("Do you want to store the password in your keychain?", default=True):
        set_keychain(journal_name, pw)
    else:
        set_keychain(journal_name, None)

    return pw


def decrypt_content(
    decrypt_func: Callable[[str], Optional[str]],
    keychain: str = None,
    max_attempts: int = 3,
) -> str:
    pwd_from_keychain = keychain and get_keychain(keychain)
    password = pwd_from_keychain or gp.getpass()
    result = decrypt_func(password)
    # Password is bad:
    if result is None and pwd_from_keychain:
        set_keychain(keychain, None)
    attempt = 1
    while result is None and attempt < max_attempts:
        print("Wrong password, try again.", file=sys.stderr)
        password = gp.getpass()
        result = decrypt_func(password)
        attempt += 1
    if result is not None:
        return result
    else:
        print("Extremely wrong password.", file=sys.stderr)
        sys.exit(1)


def get_keychain(journal_name):
    import keyring

    try:
        return keyring.get_password("jrnl", journal_name)
    except RuntimeError:
        return ""


def set_keychain(journal_name, password):
    import keyring

    if password is None:
        try:
            keyring.delete_password("jrnl", journal_name)
        except keyring.errors.PasswordDeleteError:
            pass
    else:
        keyring.set_password("jrnl", journal_name, password)


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
    if journal_name not in config["journals"]:
        return config
    config = config.copy()
    journal_conf = config["journals"].get(journal_name)
    if (
        type(journal_conf) is dict
    ):  # We can override the default config on a by-journal basis
        log.debug(
            "Updating configuration with specific journal overrides %s", journal_conf
        )
        config.update(journal_conf)
    else:  # But also just give them a string to point to the journal file
        config["journal"] = journal_conf
    config.pop("journals")
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
            print(
                "[{2}ERROR{3}: {0} set to invalid color: {1}]".format(
                    key, color, ERROR_COLOR, RESET_COLOR
                ),
                file=sys.stderr,
            )
            all_valid_colors = False
    return all_valid_colors


def get_text_from_editor(config, template=""):
    filehandle, tmpfile = tempfile.mkstemp(prefix="jrnl", text=True, suffix=".txt")
    os.close(filehandle)

    with open(tmpfile, "w", encoding="utf-8") as f:
        if template:
            f.write(template)

    try:
        subprocess.call(
            shlex.split(config["editor"], posix="win" not in sys.platform) + [tmpfile]
        )
    except AttributeError:
        subprocess.call(config["editor"] + [tmpfile])

    with open(tmpfile, "r", encoding="utf-8") as f:
        raw = f.read()
    os.remove(tmpfile)

    if not raw:
        print("[Nothing saved to file]", file=sys.stderr)

    return raw


def colorize(string, color, bold=False):
    """Returns the string colored with colorama.Fore.color. If the color set by
    the user is "NONE" or the color doesn't exist in the colorama.Fore attributes,
    it returns the string without any modification."""
    color_escape = getattr(colorama.Fore, color.upper(), None)
    if not color_escape:
        return string
    elif not bold:
        return color_escape + string + colorama.Fore.RESET
    else:
        return colorama.Style.BRIGHT + color_escape + string + colorama.Style.RESET_ALL


def highlight_tags_with_background_color(entry, text, color, is_title=False):
    """
    Takes a string and colorizes the tags in it based upon the config value for
    color.tags, while colorizing the rest of the text based on `color`.
    :param entry: Entry object, for access to journal config
    :param text: Text to be colorized
    :param color: Color for non-tag text, passed to colorize()
    :param is_title: Boolean flag indicating if the text is a title or not
    :return: Colorized str
    """

    def colorized_text_generator(fragments):
        """Efficiently generate colorized tags / text from text fragments.
        Taken from @shobrook. Thanks, buddy :)
        :param fragments: List of strings representing parts of entry (tag or word).
        :rtype: List of tuples
        :returns [(colorized_str, original_str)]"""
        for part in fragments:
            if part and part[0] not in config["tagsymbols"]:
                yield (colorize(part, color, bold=is_title), part)
            elif part:
                yield (colorize(part, config["colors"]["tags"], bold=True), part)

    config = entry.journal.config
    if config["highlight"]:  # highlight tags
        if entry.journal.search_tags:
            text_fragments = []
            for tag in entry.journal.search_tags:
                text_fragments.extend(
                    re.split(re.compile(re.escape(tag), re.IGNORECASE), text)
                )
        else:
            text_fragments = re.split(entry.tag_regex(config["tagsymbols"]), text)

        # Colorizing tags inside of other blocks of text
        final_text = ""
        previous_piece = ""
        for colorized_piece, piece in colorized_text_generator(text_fragments):
            # If this piece is entirely punctuation or whitespace or the start
            # of a line or the previous piece was a tag or this piece is a tag,
            # then add it to the final text without a leading space.
            if (
                all(char in punctuation + whitespace for char in piece)
                or previous_piece.endswith("\n")
                or (previous_piece and previous_piece[0] in config["tagsymbols"])
                or piece[0] in config["tagsymbols"]
            ):
                final_text += colorized_piece
            else:
                # Otherwise add a leading space and then append the piece.
                final_text += " " + colorized_piece

            previous_piece = piece
        return final_text.lstrip()
    else:
        return text


def slugify(string):
    """Slugifies a string.
    Based on public domain code from https://github.com/zacharyvoase/slugify
    """
    normalized_string = str(unicodedata.normalize("NFKD", string))
    no_punctuation = re.sub(r"[^\w\s-]", "", normalized_string).strip().lower()
    slug = re.sub(r"[-\s]+", "-", no_punctuation)
    return slug


def split_title(text):
    """Splits the first sentence off from a text."""
    punkt = SENTENCE_SPLITTER.search(text)
    if not punkt:
        return text, ""
    return text[: punkt.end()].strip(), text[punkt.end() :].strip()
