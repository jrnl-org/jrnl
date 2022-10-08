# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
import os

import colorama
import xdg.BaseDirectory
from ruamel.yaml import YAML
from ruamel.yaml import constructor

from jrnl import __version__
from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import list_journals
from jrnl.output import print_msg
from jrnl.path import home_dir

# Constants
DEFAULT_CONFIG_NAME = "jrnl.yaml"
XDG_RESOURCE = "jrnl"

DEFAULT_JOURNAL_NAME = "journal.txt"
DEFAULT_JOURNAL_KEY = "default"

YAML_SEPARATOR = ": "
YAML_FILE_ENCODING = "utf-8"


def make_yaml_valid_dict(input: list) -> dict:

    """

    Convert a two-element list of configuration key-value pair into a flat dict.

    The dict is created through the yaml loader, with the assumption that
    "input[0]: input[1]" is valid yaml.

    :param input: list of configuration keys in dot-notation and their respective values.
    :type input: list
    :return: A single level dict of the configuration keys in dot-notation and their respective desired values
    :rtype: dict
    """

    assert len(input) == 2

    # yaml compatible strings are of the form Key:Value
    yamlstr = YAML_SEPARATOR.join(input)

    runtime_modifications = YAML(typ="safe").load(yamlstr)

    return runtime_modifications


def save_config(config, alt_config_path=None):
    """Supply alt_config_path if using an alternate config through --config-file."""
    config["version"] = __version__

    yaml = YAML(typ="safe")
    yaml.default_flow_style = False  # prevents collapsing of tree structure

    with open(
        alt_config_path if alt_config_path else get_config_path(),
        "w",
        encoding=YAML_FILE_ENCODING,
    ) as f:
        yaml.dump(config, f)


def get_config_path():
    try:
        config_directory_path = xdg.BaseDirectory.save_config_path(XDG_RESOURCE)
    except FileExistsError:
        raise JrnlException(
            Message(
                MsgText.ConfigDirectoryIsFile,
                MsgStyle.ERROR,
                {
                    "config_directory_path": os.path.join(
                        xdg.BaseDirectory.xdg_config_home, XDG_RESOURCE
                    )
                },
            ),
        )

    return os.path.join(config_directory_path or home_dir(), DEFAULT_CONFIG_NAME)


def get_default_config():
    return {
        "version": __version__,
        "journals": {"default": {"journal": get_default_journal_path()}},
        "editor": os.getenv("VISUAL") or os.getenv("EDITOR") or "",
        "encrypt": False,
        "template": False,
        "default_hour": 9,
        "default_minute": 0,
        "timeformat": "%F %r",
        "tagsymbols": "#@",
        "highlight": True,
        "linewrap": 79,
        "indent_character": "|",
        "colors": {
            "date": "none",
            "title": "none",
            "body": "none",
            "tags": "none",
        },
    }


def get_default_journal_path():
    journal_data_path = xdg.BaseDirectory.save_data_path(XDG_RESOURCE) or home_dir()
    return os.path.join(journal_data_path, DEFAULT_JOURNAL_NAME)


def scope_config(config, journal_name):
    if journal_name not in config["journals"]:
        return config
    config = config.copy()
    journal_conf = config["journals"].get(journal_name)
    if type(journal_conf) is dict:
        # We can override the default config on a by-journal basis
        logging.debug(
            "Updating configuration with specific journal overrides %s", journal_conf
        )
        config.update(journal_conf)
    else:
        # But also just give them a string to point to the journal file
        config["journal"] = journal_conf
    return config


def verify_config_colors(config):
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
            print_msg(
                Message(
                    MsgText.InvalidColor,
                    MsgStyle.NORMAL,
                    {
                        "key": key,
                        "color": color,
                    },
                )
            )
            all_valid_colors = False
    return all_valid_colors


def load_config(config_path):
    """Tries to load a config file from YAML."""
    try:
        with open(config_path, encoding=YAML_FILE_ENCODING) as f:
            yaml = YAML(typ="safe")
            yaml.allow_duplicate_keys = False
            return yaml.load(f)
    except constructor.DuplicateKeyError as e:
        print_msg(
            Message(
                MsgText.ConfigDoubleKeys,
                MsgStyle.WARNING,
                {
                    "error_message": e,
                },
            )
        )
        with open(config_path, encoding=YAML_FILE_ENCODING) as f:
            yaml = YAML(typ="safe")
            yaml.allow_duplicate_keys = True
            return yaml.load(f)


def is_config_json(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        config_file = f.read()
    return config_file.strip().startswith("{")


def update_config(config, new_config, scope, force_local=False):
    """Updates a config dict with new values - either global if scope is None
    or config['journals'][scope] is just a string pointing to a journal file,
    or within the scope"""
    if scope and type(config["journals"][scope]) is dict:  # Update to journal specific
        config["journals"][scope].update(new_config)
    elif scope and force_local:  # Convert to dict
        config["journals"][scope] = {"journal": config["journals"][scope]}
        config["journals"][scope].update(new_config)
    else:
        config.update(new_config)


def get_journal_name(args, config):
    args.journal_name = DEFAULT_JOURNAL_KEY

    # The first arg might be a journal name
    if args.text:
        potential_journal_name = args.text[0]
        if potential_journal_name[-1] == ":":
            potential_journal_name = potential_journal_name[0:-1]

        if potential_journal_name in config["journals"]:
            args.journal_name = potential_journal_name
            args.text = args.text[1:]

    if args.journal_name not in config["journals"]:
        raise JrnlException(
            Message(
                MsgText.NoDefaultJournal,
                MsgStyle.ERROR,
                {"journals": list_journals(config)},
            ),
        )

    logging.debug("Using journal name: %s", args.journal_name)
    return args
