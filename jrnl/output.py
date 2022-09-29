# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import textwrap
from typing import Union

from rich.console import Console
from rich.text import Text

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


def journal_list_to_json(journal_list):
    import json

    return json.dumps(journal_list)


def journal_list_to_yaml(journal_list):
    from io import StringIO

    from ruamel.yaml import YAML

    output = StringIO()
    YAML().dump(journal_list, output)
    return output.getvalue()


def journal_list_to_stdout(journal_list):
    result = f"Journals defined in config ({journal_list['config_path']})\n"
    ml = min(max(len(k) for k in journal_list["journals"]), 20)
    for journal, cfg in journal_list["journals"].items():
        result += " * {:{}} -> {}\n".format(
            journal, ml, cfg["journal"] if isinstance(cfg, dict) else cfg
        )
    return result


def list_journals(configuration, format=None):
    from jrnl import config

    """List the journals specified in the configuration file"""

    journal_list = {
        "config_path": config.get_config_path(),
        "journals": configuration["journals"],
    }

    if format == "json":
        return journal_list_to_json(journal_list)
    elif format == "yaml":
        return journal_list_to_yaml(journal_list)
    else:
        return journal_list_to_stdout(journal_list)


def print_msg(msg: Message, **kwargs) -> Union[None, str]:
    """Helper function to print a single message"""
    kwargs["style"] = msg.style
    return print_msgs([msg], **kwargs)


def print_msgs(
    msgs: list[Message],
    delimiter: str = "\n",
    style: MsgStyle = MsgStyle.NORMAL,
    get_input: bool = False,
    hide_input: bool = False,
) -> Union[None, str]:
    # Same as print_msg, but for a list
    text = Text("", end="")
    kwargs = style.decoration.args

    for i, msg in enumerate(msgs):
        kwargs = _add_extra_style_args_if_needed(kwargs, msg=msg)

        m = format_msg_text(msg)

        if i != len(msgs) - 1:
            m.append(delimiter)

        text.append(m)

    if style.append_space:
        text.append(" ")

    decorated_text = style.decoration.callback(text, **kwargs)

    # Always print messages to stderr
    console = _get_console(stderr=True)

    if get_input:
        return str(console.input(prompt=decorated_text, password=hide_input))
    console.print(decorated_text, new_line_start=style.prepend_newline)


def _get_console(stderr: bool = True) -> Console:
    return Console(stderr=stderr)


def _add_extra_style_args_if_needed(args, msg):
    args["border_style"] = msg.style.color
    args["title"] = msg.style.box_title
    return args


def format_msg_text(msg: Message) -> Text:
    text = textwrap.dedent(msg.text.value)
    text = text.format(**msg.params)
    # dedent again in case inserted text needs it
    text = textwrap.dedent(text)
    text = text.strip()
    return Text(text)
