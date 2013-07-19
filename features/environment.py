from behave import *
import shutil
import os

def before_scenario(context, scenario):
    """Before each scenario, backup all config and journal test data."""
    for folder in ("configs", "journals"):
        original = os.path.join("features", folder)
        backup = os.path.join("features", folder+"_backup")
        if not os.path.exists(backup):
            os.mkdir(backup)
        for filename in os.listdir(original):
            shutil.copy2(os.path.join(original, filename), backup)

def after_scenario(context, scenario):
    """After each scenario, restore all test data and remove backups."""
    for folder in ("configs", "journals"):
        original = os.path.join("features", folder)
        backup = os.path.join("features", folder+"_backup")
        for filename in os.listdir(backup):
            shutil.copy2(os.path.join(backup, filename), original)
        shutil.rmtree(backup)
