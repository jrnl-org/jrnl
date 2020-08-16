import logging
import sys

import colorama
import yaml

from .color import ERROR_COLOR
from .color import RESET_COLOR
from .output import list_journals


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
            print(
                "[{2}ERROR{3}: {0} set to invalid color: {1}]".format(
                    key, color, ERROR_COLOR, RESET_COLOR
                ),
                file=sys.stderr,
            )
            all_valid_colors = False
    return all_valid_colors


def load_config(config_path):
    """Tries to load a config file from YAML."""
    with open(config_path) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


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
    from . import install

    args.journal_name = install.DEFAULT_JOURNAL_KEY
    if args.text and args.text[0] in config["journals"]:
        args.journal_name = args.text[0]
        args.text = args.text[1:]
    elif install.DEFAULT_JOURNAL_KEY not in config["journals"]:
        print("No default journal configured.", file=sys.stderr)
        print(list_journals(config), file=sys.stderr)
        sys.exit(1)

    logging.debug("Using journal name: %s", args.journal_name)
    return args
