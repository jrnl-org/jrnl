from behave import *
import shutil
import os
from jrnl import jrnl
try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO

def before_scenario(context, scenario):
    """Before each scenario, backup all config and journal test data."""
    context.messages = StringIO()
    jrnl.util.STDERR = context.messages
    jrnl.util.TEST = True
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

def after_scenario(context, scenario):
    """After each scenario, restore all test data and remove working_dirs."""
    context.messages.close()
    context.messages = None
    for folder in ("configs", "journals"):
        working_dir = os.path.join("features", folder)
        shutil.rmtree(working_dir)
