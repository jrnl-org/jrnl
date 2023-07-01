# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
from .BaseConfigReader import BaseConfigReader
from pathlib import PurePath


class DefaultConfigReader(BaseConfigReader):
    def __init__(self, filename: str):
        logging.debug("start")
        super()
        self.filename: PurePath = PurePath(filename)

    def read(self):
        self._parse_args()
        # do some actual reading

    def _parse_args(self):
        # read self.args
        # update self.cofig somehow
        pass
