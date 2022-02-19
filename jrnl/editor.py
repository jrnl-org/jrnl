import logging
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

from jrnl.color import ERROR_COLOR
from jrnl.color import RESET_COLOR
from jrnl.os_compat import on_windows
from jrnl.os_compat import split_args
from jrnl.output import print_msg
from jrnl.output import Message
from jrnl.exception import JrnlException
from jrnl.exception import JrnlExceptionMessage


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
    except FileNotFoundError as e:
        error_msg = f"""
        {ERROR_COLOR}{str(e)}{RESET_COLOR}

        Please check the 'editor' key in your config file for errors:
            {repr(config['editor'])}
        """
        print(textwrap.dedent(error_msg).strip(), file=sys.stderr)
        exit(1)

    with open(tmpfile, "r", encoding="utf-8") as f:
        raw = f.read()
    os.remove(tmpfile)

    if not raw:
        print("[Nothing saved to file]", file=sys.stderr)

    return raw


def get_text_from_stdin():
    _how_to_quit = "Ctrl+z and then Enter" if on_windows() else "Ctrl+d"
    print_msg(
        "Writing Entry",
        f"To finish writing, press {_how_to_quit} on a blank line.",
        msg=Message.NORMAL,
    )
    try:
        raw = sys.stdin.read()
    except KeyboardInterrupt:
        logging.error("Write mode: keyboard interrupt")
        print_msg("\nEntry NOT saved to journal", msg=Message.NORMAL)
        raise JrnlException(JrnlExceptionMessage.KeyboardInterrupt)

    return raw
