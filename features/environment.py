import shutil
import os
import sys


def before_feature(context, feature):
    # add "skip" tag
    # https://stackoverflow.com/a/42721605/4276230
    if "skip" in feature.tags:
        feature.skip("Marked with @skip")
        return

    if "skip_win" in feature.tags and "win32" in sys.platform:
        feature.skip("Skipping on Windows")
        return


def before_scenario(context, scenario):
    """Before each scenario, backup all config and journal test data."""
    # Clean up in case something went wrong
    for folder in ("configs", "journals", "cache"):
        working_dir = os.path.join("features", folder)
        if os.path.exists(working_dir):
            shutil.rmtree(working_dir)

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
        scenario.skip("Marked with @skip")
        return

    if "skip_win" in scenario.effective_tags and "win32" in sys.platform:
        scenario.skip("Skipping on Windows")
        return


def after_scenario(context, scenario):
    """After each scenario, restore all test data and remove working_dirs."""
    for folder in ("configs", "journals", "cache"):
        working_dir = os.path.join("features", folder)
        if os.path.exists(working_dir):
            shutil.rmtree(working_dir)
