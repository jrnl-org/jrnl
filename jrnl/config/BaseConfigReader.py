# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
from abc import ABC
from abc import abstractmethod


class BaseConfigReader(ABC):
    def __init__(self):
        logging.debug("start")
        self.config: dict = {}

    @abstractmethod
    def read(self):
        pass

    def get_config(self):
        return self.config
