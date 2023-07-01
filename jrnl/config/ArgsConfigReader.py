# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
from .BaseConfigReader import BaseConfigReader


class ArgsConfigReader(BaseConfigReader):
    def __init__(self, args):
        logging.debug("start")
        super()
        self.args = args

    def read(self):
        self._parse_args()
        # do some actual reading

    def _parse_args(self):
        # read self.args
        # update self.cofig somehow
        pass
