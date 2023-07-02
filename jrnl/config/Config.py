# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
from jrnl.exception import JrnlConfigException
from jrnl.exception import JrnlException
from jrnl.config.BaseConfigReader import BaseConfigReader


class Config():
    def __init__(self):
        self.configs: list[dict[str, list[BaseConfigReader] | bool]] = []

    def add_config(self, readers: list[BaseConfigReader], required: bool = False):
        self.configs.append({
            "readers" : readers,
            "required": required,
        })

    def read(self):
        for config in self.configs:
            found = False
            for reader in config["readers"]:
                keep_going = False

                try:
                    reader.read()
                    found = True
                except JrnlConfigException as e:
                    print(e)
                    keep_going = True

                if not keep_going:
                    break

            logging.debug(f"config read: {reader}")
            if config["required"] and not found:
                raise JrnlException
