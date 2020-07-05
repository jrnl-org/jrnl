import os
import shutil

from jrnl.os_compat import on_windows

CWD = os.getcwd()


def clean_all_working_dirs():
    for folder in ("configs", "journals", "cache"):
        working_dir = os.path.join("features", folder)
        if os.path.exists(working_dir):
            shutil.rmtree(working_dir)


def before_feature(context, feature):
    # add "skip" tag
    # https://stackoverflow.com/a/42721605/4276230
    if "skip" in feature.tags:
        feature.skip("")
        return

    if "skip_win" in feature.tags and on_windows:
        feature.skip("Skipping on Windows")
        return


def before_scenario(context, scenario):
    """Before each scenario, backup all config and journal test data."""
    # Clean up in case something went wrong
    clean_all_working_dirs()
    for folder in ("configs", "journals"):
        original = os.path.join("features", "data", folder)
        working_dir = os.path.join("features", folder)
        if not os.path.exists(working_dir):
            os.mkdir(working_dir)
        for filename in os.listdir(original):
            source = os.path.join(original, filename)
            if os.path.isdir(source):
                shutil.copytree(source, os.path.join(working_dir, filename))
            else:
                shutil.copy2(source, working_dir)

    # add "skip" tag
    # https://stackoverflow.com/a/42721605/4276230
    if "skip" in scenario.effective_tags:
        scenario.skip("")
        return

    if "skip_win" in scenario.effective_tags and on_windows:
        scenario.skip("Skipping on Windows")
        return


def after_scenario(context, scenario):
    """After each scenario, restore all test data and remove working_dirs."""
    if os.getcwd() != CWD:
        os.chdir(CWD)
    clean_all_working_dirs()
