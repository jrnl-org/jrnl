import logging 
def apply_overrides(overrides: dict, base_config: dict) -> dict:
    config = base_config.copy() 
    for k in overrides:
        logging.debug("Overriding %s from %s to %s" % (k, config[k], overrides[k]))
        config[k] = overrides[k]

    return config 