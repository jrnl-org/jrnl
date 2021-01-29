# import logging
def apply_overrides(overrides: dict, base_config: dict) -> dict:
    """Unpack parsed overrides in dot-notation and return the "patched" configuration

    Args:
        overrides (dict): Single-level dict of config fields in dot-notation and their desired values
        base_config (dict): The "saved" configuration, as read from YAML

    Returns:
        dict: Updated configuration with applied overrides, in the format of the loaded configuration
    """
    config = base_config.copy()
    for k in overrides:
        nodes = k.split(".")
        config = _recursively_apply(config, nodes, overrides[k])
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
