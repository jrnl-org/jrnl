# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
from .BaseConfigReader import BaseConfigReader
from jrnl.exception import JrnlConfigException
from jrnl.path import expand_path
from pathlib import PurePath
from ruamel.yaml import YAML
from ruamel.yaml import constructor

YAML_SEPARATOR = ": "
YAML_FILE_ENCODING = "utf-8"

def load_config(config_path: str) -> dict:
    """Tries to load a config file from YAML."""
    try:
        with open(config_path, encoding=YAML_FILE_ENCODING) as f:
            yaml = YAML(typ="safe")
            yaml.allow_duplicate_keys = False
            return yaml.load(f)
    except constructor.DuplicateKeyError as e:
        print_msg(
            Message(
                MsgText.ConfigDoubleKeys,
                MsgStyle.WARNING,
                {
                    "error_message": e,
                },
            )
        )
        with open(config_path, encoding=YAML_FILE_ENCODING) as f:
            yaml = YAML(typ="safe")
            yaml.allow_duplicate_keys = True
            return yaml.load(f)


class FileConfigReader(BaseConfigReader):
    def __init__(self, filename: str):
        logging.debug("start")
        super()
        self.filename: PurePath = PurePath(expand_path(filename))

    def read(self):
        logging.debug(f"start read for {self.filename}")

        try:
            self._raw_config_file = read_file(self.filename)
            # do some tests on config file contents
            # self.config = load_config(expand_path(self.filename))
            
        except FileNotFoundError:
            raise JrnlConfigException("File is missing")
