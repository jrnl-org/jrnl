# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from enum import Enum
import logging
import sys
from collections import namedtuple
import textwrap

from jrnl.color import colorize
from jrnl.color import RESET_COLOR
from jrnl.color import WARNING_COLOR


def deprecated_cmd(old_cmd, new_cmd, callback=None, **kwargs):

    warning_msg = f"""
    The command {old_cmd} is deprecated and will be removed from jrnl soon.
    Please use {new_cmd} instead.
    """
    warning_msg = textwrap.dedent(warning_msg)
    logging.warning(warning_msg)
    print(f"{WARNING_COLOR}{warning_msg}{RESET_COLOR}", file=sys.stderr)

    if callback is not None:
        callback(**kwargs)


def list_journals(configuration):
    from . import config

    """List the journals specified in the configuration file"""
    result = f"Journals defined in {config.get_config_path()}\n"
    ml = min(max(len(k) for k in configuration["journals"]), 20)
    for journal, cfg in configuration["journals"].items():
        result += " * {:{}} -> {}\n".format(
            journal, ml, cfg["journal"] if isinstance(cfg, dict) else cfg
        )
    return result


MessageProps = namedtuple("MessageProps", ["value", "color", "pipe"])


class Message(Enum):
    NORMAL = MessageProps(0, "cyan", sys.stderr)
    WARNING = MessageProps(1, "yellow", sys.stderr)
    ERROR = MessageProps(2, "red", sys.stderr)

    @property
    def color(self):
        return self.value.color

    @property
    def pipe(self):
        return self.value.pipe


def print_msg(title: str, body: str = "", msg: Message = Message.NORMAL):

    # @todo Add some polish around colorization of multi-line messages
    result = colorize(title, msg.color)

    if body:
        result += f"\n{body}"

    print(result, file=msg.pipe)
