# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
import sys
import textwrap

from jrnl.color import colorize
from jrnl.color import RESET_COLOR
from jrnl.color import WARNING_COLOR
from jrnl.messages import Message


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


def print_msg(msg: Message):
    msg_text = textwrap.dedent(msg.text.value.format(**msg.params)).strip().split("\n")

    longest_string = len(max(msg_text, key=len))
    msg_text = [f"[ {line:<{longest_string}} ]" for line in msg_text]

    # colorize can't be called until after the lines are padded,
    # because python gets confused by the ansi color codes
    msg_text[0] = f"[{colorize(msg_text[0][1:-1], msg.type.color)}]"

    print("\n".join(msg_text), file=sys.stderr)
