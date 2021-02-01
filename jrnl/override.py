# import logging
def apply_overrides(overrides: list, base_config: dict) -> dict:
    """Unpack CLI provided overrides into the configuration tree.

    :param overrides: List of configuration key-value pairs collected from the CLI
    :type overrides: list
    :param base_config: Configuration Loaded from the saved YAML
    :type base_config: dict
    :return: Configuration to be used during runtime with the overrides applied
    :rtype: dict
    """
    config = base_config.copy()
    for pairs in overrides:
        k, v = list(pairs.items())[0]
        nodes = k.split(".")
        config = _recursively_apply(config, nodes, v)
    return config


def _recursively_apply(config: dict, nodes: list, override_value) -> dict:
    """Recurse through configuration and apply overrides at the leaf of the config tree

    Credit to iJames on SO: https://stackoverflow.com/a/47276490 for algorithm

    Args:
        config (dict): Configuration to modify
        nodes (list): Vector of override keys; the length of the vector indicates tree depth
        override_value (str): Runtime override passed from the command-line
    """
    key = nodes[0]
    if len(nodes) == 1:
        config[key] = override_value
    else:
        next_key = nodes[1:]
        _recursively_apply(_get_config_node(config, key), next_key, override_value)

    return config


def _get_config_node(config: dict, key: str):
    if key in config:
        pass
    else:
        config[key] = None
    return config[key]
