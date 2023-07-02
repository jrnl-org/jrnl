# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
from abc import ABC
from abc import abstractmethod
from typing import Any
from rich.pretty import pretty_repr


class BaseConfigReader(ABC):
    def __init__(self):
        logging.debug("start")
        self.config: dict[str, Any] = {}

    def __str__(self):
        return pretty_repr(self.config)

    @abstractmethod
    def read(self):
        """Needs to set self.config"""
        pass

    def get_config(self):
        return self.config
