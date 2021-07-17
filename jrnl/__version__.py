# This file is managed automatically by the GitHub release flow

import sys

__version__ = "v2.8.1"

# this makes the version available at `jrnl.__version__` without requiring a
# `__init__.py` file in the *jrnl* root directory
sys.modules["jrnl.__version__"] = __version__
