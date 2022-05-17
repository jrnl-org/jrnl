# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
import textwrap

from typing import Union
from rich.text import Text
from rich.console import Console

from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText


def deprecated_cmd(old_cmd, new_cmd, callback=None, **kwargs):
    print_msg(
        Message(
            MsgText.DeprecatedCommand,
            MsgStyle.WARNING,
            {"old_cmd": old_cmd, "new_cmd": new_cmd},
        )
    )

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


def print_msg(msg: Message, is_prompt: bool = False) -> Union[None, str]:
    return print_msgs([msg], style=msg.style, is_prompt=is_prompt)


def print_msgs(
    msgs: list[Message],
    delimiter: str = "\n",
    style: MsgStyle = MsgStyle.NORMAL,
    is_prompt: bool = False,
) -> Union[None, str]:
    # Same as print_msg, but for a list
    text = Text("")
    decoration_callback = style.decoration.callback
    args = style.decoration.args
    prepend_newline = False
    append_space = False

    for msg in msgs:
        args = _add_extra_style_args_if_needed(args, msg=msg)

        if _needs_prepended_newline(msg):
            prepend_newline = True

        if _needs_appended_space(msg):
            append_space = True

        m = format_msg_text(msg)
        m.append(delimiter)

        text.append(m)

    text.rstrip()

    if append_space:
        text.append(" ")

    # Always print messages to stderr
    console = Console(stderr=True)
    decorated_text = decoration_callback(text, **args)

    if is_prompt:
        return str(console.input(prompt=decorated_text))
    else:
        console.print(decorated_text, new_line_start=prepend_newline)


def _add_extra_style_args_if_needed(args, msg):
    args["border_style"] = msg.style.color
    args["title"] = "Error" if msg.style == MsgStyle.ERROR else None
    return args


def _needs_prepended_newline(msg: Message) -> bool:
    return is_keyboard_int(msg)


def _needs_appended_space(msg: Message) -> bool:
    return is_prompt(msg)


def is_prompt(msg: Message) -> bool:
    return msg.style == MsgStyle.PROMPT


def is_keyboard_int(msg: Message) -> bool:
    return msg.text == MsgText.KeyboardInterruptMsg


def format_msg_text(msg: Message) -> Text:
    text = textwrap.dedent(msg.text.value.format(**msg.params)).strip()
    return Text(text)
