# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.os_compat import on_windows
from jrnl.os_compat import split_args
from jrnl.output import print_msg


def get_text_from_editor(config, template=""):
    suffix = ".jrnl"
    if config["template"]:
        template_filename = Path(config["template"]).name
        suffix = "-" + template_filename
    filehandle, tmpfile = tempfile.mkstemp(prefix="jrnl", text=True, suffix=suffix)
    os.close(filehandle)

    with open(tmpfile, "w", encoding="utf-8") as f:
        if template:
            f.write(template)

    try:
        subprocess.call(split_args(config["editor"]) + [tmpfile])
    except FileNotFoundError:
        raise JrnlException(
            Message(
                MsgText.EditorMisconfigured,
                MsgStyle.ERROR,
                {"editor_key": config["editor"]},
            )
        )

    with open(tmpfile, "r", encoding="utf-8") as f:
        raw = f.read()
    os.remove(tmpfile)

    if not raw:
        raise JrnlException(Message(MsgText.NoTextReceived, MsgStyle.NORMAL))

    return raw


def get_text_from_stdin():
    print_msg(
        Message(
            MsgText.WritingEntryStart,
            MsgStyle.TITLE,
            {
                "how_to_quit": MsgText.HowToQuitWindows
                if on_windows()
                else MsgText.HowToQuitLinux
            },
        )
    )

    try:
        raw = sys.stdin.read()
    except KeyboardInterrupt:
        logging.error("Write mode: keyboard interrupt")
        raise JrnlException(
            Message(MsgText.KeyboardInterruptMsg, MsgStyle.ERROR_ON_NEW_LINE),
            Message(MsgText.JournalNotSaved, MsgStyle.WARNING),
        )

    return raw
