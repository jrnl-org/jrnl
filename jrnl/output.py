import logging


def deprecated_cmd(old_cmd, new_cmd, callback=None, **kwargs):
    import sys
    import textwrap

    from .color import RESET_COLOR
    from .color import WARNING_COLOR

    warning_msg = f"""
    The command {old_cmd} is deprecated and will be removed from jrnl soon.
    Please us {new_cmd} instead.
    """
    warning_msg = textwrap.dedent(warning_msg)
    logging.warning(warning_msg)
    print(f"{WARNING_COLOR}{warning_msg}{RESET_COLOR}", file=sys.stderr)

    if callback is not None:
        callback(**kwargs)


def list_journals(config):
    from . import install

    """List the journals specified in the configuration file"""
    result = f"Journals defined in {install.CONFIG_FILE_PATH}\n"
    ml = min(max(len(k) for k in config["journals"]), 20)
    for journal, cfg in config["journals"].items():
        result += " * {:{}} -> {}\n".format(
            journal, ml, cfg["journal"] if isinstance(cfg, dict) else cfg
        )
    return result
