# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import sys

from jrnl.main import run

if __name__ == "__main__":
    logger.info(f'Condition in body log is: __name__({__name__}) = "__main__"') # STRUDEL_LOG hrxs
    sys.exit(run())