# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from argparse import Namespace

from jrnl.config import make_yaml_valid_dict
from jrnl.config import update_config


# import logging
def apply_overrides(args: Namespace, base_config: dict) -> dict:
    """Unpack CLI provided overrides into the configuration tree.

    :param overrides: List of configuration key-value pairs collected from the CLI
    :type overrides: list
    :param base_config: Configuration Loaded from the saved YAML
    :type base_config: dict
    :return: Configuration to be used during runtime with the overrides applied
    :rtype: dict
    """
    overrides = vars(args).get("config_override", None)
    if not overrides:
        return base_config

    cfg_with_overrides = base_config.copy()
    for pairs in overrides:

        pairs = make_yaml_valid_dict(pairs)
        key_as_dots, override_value = _get_key_and_value_from_pair(pairs)
        keys = _convert_dots_to_list(key_as_dots)
        cfg_with_overrides = _recursively_apply(
            cfg_with_overrides, keys, override_value
        )

    update_config(base_config, cfg_with_overrides, None)
    return base_config


def _get_key_and_value_from_pair(pairs):
    key_as_dots, override_value = list(pairs.items())[0]
    return key_as_dots, override_value


def _convert_dots_to_list(key_as_dots):
    keys = key_as_dots.split(".")
    keys = [k for k in keys if k != ""]  # remove empty elements
    return keys


def _recursively_apply(tree: dict, nodes: list, override_value) -> dict:
    """Recurse through configuration and apply overrides at the leaf of the config tree

    Credit to iJames on SO: https://stackoverflow.com/a/47276490 for algorithm

    Args:
        config (dict): Configuration to modify
        nodes (list): Vector of override keys; the length of the vector indicates tree depth
        override_value (str): Runtime override passed from the command-line
    """
    key = nodes[0]
    if len(nodes) == 1:
        tree[key] = override_value
    else:
        next_key = nodes[1:]
        next_node = _get_config_node(tree, key)
        _recursively_apply(next_node, next_key, override_value)

    return tree


def _get_config_node(config: dict, key: str):
    if key in config:
        pass
    else:
        config[key] = None
    return config[key]
