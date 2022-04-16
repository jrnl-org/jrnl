# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
import sys
import textwrap
from typing import Tuple

from rich import print
import rich
from rich.panel import Panel
from rich.padding import Padding
from rich.text import Text
from rich.measure import Measurement
from rich.console import Group
from rich import box

from jrnl.color import colorize
from jrnl.color import RESET_COLOR
from jrnl.color import WARNING_COLOR
from jrnl.messages import Message
from jrnl.messages import MsgType
from jrnl.messages import MsgText


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
    result = f"Journals defined in config ({config.get_config_path()})\n"
    ml = min(max(len(k) for k in configuration["journals"]), 20)
    for journal, cfg in configuration["journals"].items():
        result += " * {:{}} -> {}\n".format(
            journal, ml, cfg["journal"] if isinstance(cfg, dict) else cfg
        )
    return result


def print_msg(msg: Message) -> None:
    print_msgs([msg])


def print_msgs(msgs: list[Message], delimiter: str = "\n") -> None:
    # Same as print_msg, but for a list
    text = Text("")

    kwargs = {
        "expand": False,
        "border_style": None,
        "padding": (0,2),
        "title_align": "left",
        "box": box.HEAVY
    }

    for msg in msgs:
        kwargs["border_style"] = msg.type.color
        if msg.type == MsgType.ERROR:
            kwargs["title"] = "Error"

        if is_keyboard_int(msg):
            print()

        m = format_msg(msg)
        m.append(delimiter)
        text.append(m)

    text.rstrip()
    print(Panel(text, **kwargs))


def is_keyboard_int(msg: Message) -> bool:
    return msg.text == MsgText.KeyboardInterruptMsg

def format_msg(msg: Message) -> Text:
    text = (
        textwrap.dedent(msg.text.value.format(**msg.params))
        .strip()
        # .splitlines(keepends=True)
    )
    result = Text(text)
    # result = Text(text[0])
    # result.stylize(msg.type.color)
    # result.append("".join(text[1:]))
    return result
