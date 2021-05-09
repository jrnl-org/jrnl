import os
import shutil

from jrnl.os_compat import on_windows

try:
    from jrnl.contrib.exporter import testing as testing_exporter
except ImportError:
    testing_exporter = None

CWD = os.getcwd()

# @see https://behave.readthedocs.io/en/latest/tutorial.html#debug-on-error-in-case-of-step-failures
BEHAVE_DEBUG_ON_ERROR = False


def setup_debug_on_error(userdata):
    global BEHAVE_DEBUG_ON_ERROR
    BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")


def before_all(context):
    setup_debug_on_error(context.config.userdata)


# def after_step(context, step):
# if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
# -- ENTER DEBUGGER: Zoom in on failure location.
# NOTE: Use IPython debugger, same for pdb (basic python debugger).
# import ipdb
# ipdb.post_mortem(step.exc_traceback)


def clean_all_working_dirs():
    if os.path.exists("test.txt"):
        os.remove("test.txt")
    for folder in ("configs", "journals", "cache"):
        working_dir = os.path.join("features", folder)
        if os.path.exists(working_dir):
            shutil.rmtree(working_dir)


def before_feature(context, feature):
    # add "skip" tag
    # https://stackoverflow.com/a/42721605/4276230
    if "skip" in feature.tags:
        feature.skip()
        return

    if "skip_win" in feature.tags and on_windows():
        feature.skip("Skipping on Windows")
        return

    if "skip_only_with_external_plugins" in feature.tags and testing_exporter is None:
        feature.skip("Requires test external plugins installed")
        return

    if "skip_no_external_plugins" in feature.tags and testing_exporter:
        feature.skip("Skipping with external plugins installed")
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
        scenario.skip()
        return

    if "skip_win" in scenario.effective_tags and on_windows():
        scenario.skip("Skipping on Windows")
        return

    if (
        "skip_only_with_external_plugins" in scenario.effective_tags
        and testing_exporter is None
    ):
        scenario.skip("Requires test external plugins installed")
        return

    if "skip_no_external_plugins" in scenario.effective_tags and testing_exporter:
        scenario.skip("Skipping with external plugins installed")
        return


def after_scenario(context, scenario):
    """After each scenario, restore all test data and remove working_dirs."""
    if os.getcwd() != CWD:
        os.chdir(CWD)

    # only clean up if debugging is off and the scenario passed
    if BEHAVE_DEBUG_ON_ERROR and scenario.status != "failed":
        clean_all_working_dirs()
    else:
        clean_all_working_dirs()
