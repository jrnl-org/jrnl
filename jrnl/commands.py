def deprecated_cmd(old_cmd, new_cmd, callback, **kwargs):
    import sys
    from .util import RESET_COLOR, WARNING_COLOR

    print(
        WARNING_COLOR,
        f"\nThe command {old_cmd} is deprecated and will be removed from jrnl soon.\n"
        f"Please use {new_cmd} instead.\n",
        RESET_COLOR,
        file=sys.stderr,
    )
    callback(**kwargs)


def preconfig_diagnostic(_):
    import platform
    import sys
    import jrnl

    print(
        f"jrnl: {jrnl.__version__}\n"
        f"Python: {sys.version}\n"
        f"OS: {platform.system()} {platform.release()}"
    )


def preconfig_version(_):
    import jrnl

    version_str = f"{jrnl.__title__} version {jrnl.__version__}"
    print(version_str)


def preconfig_command(args):
    print("this is a pre-config command")


def postconfig_list(config, **kwargs):
    print(list_journals(config))


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
