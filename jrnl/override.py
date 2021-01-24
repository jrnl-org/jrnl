# import logging
def apply_overrides(overrides: dict, base_config: dict) -> dict:
    config = base_config.copy()
    for k in overrides:
        nodes = k.split(".")
        config = recursively_apply(config, nodes, overrides[k])
    return config


def recursively_apply(config: dict, nodes: list, override_value) -> dict:
    """Recurse through configuration and apply overrides at the leaf of the config tree

    See: https://stackoverflow.com/a/47276490 for algorithm

    Args:
        config (dict): loaded configuration from YAML
        nodes (list): vector of override keys; the length of the vector indicates tree depth
        override_value (str): runtime override passed from the command-line
    """
    key = nodes[0]
    config[key] = (
        override_value
        if len(nodes) == 1
        else recursively_apply(
            config[key] if key in config else {}, nodes[1:], override_value
        )
    )
    return config
