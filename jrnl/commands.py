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


def postconfig_list(config, **kwargs):
    from .util import list_journals

    print(list_journals(config))
