# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging

from .BaseConfigReader import BaseConfigReader


class DefaultConfigReader(BaseConfigReader):
    def __init__(self, *args, **kwargs):
        logging.debug("start")
        super().__init__(*args, **kwargs)

    def read(self):
        logging.debug("start read")
        self.config = {
            # TODO: Uncomment these lines

            # "version": __version__,
            # "journals": {"default": {"journal": get_default_journal_path()}},
            # "editor": os.getenv("VISUAL") or os.getenv("EDITOR") or "",
            "encrypt": False,
            "template": False,
            "default_hour": 9,
            "default_minute": 0,
            "timeformat": "%F %r",
            "tagsymbols": "#@",
            "highlight": True,
            "linewrap": 79,
            "indent_character": "|",
            "colors": {
                "body": "none",
                "date": "none",
                "tags": "none",
                "title": "none",
            },
        }
