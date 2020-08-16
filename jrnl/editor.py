import logging
import os
import shlex
import subprocess
import sys
import tempfile
import textwrap

from .color import ERROR_COLOR
from .color import RESET_COLOR
from .os_compat import on_windows


def get_text_from_editor(config, template=""):
    filehandle, tmpfile = tempfile.mkstemp(prefix="jrnl", text=True, suffix=".txt")
    os.close(filehandle)

    with open(tmpfile, "w", encoding="utf-8") as f:
        if template:
            f.write(template)

    try:
        subprocess.call(shlex.split(config["editor"], posix=on_windows) + [tmpfile])
    except Exception as e:
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
    _how_to_quit = "Ctrl+z and then Enter" if on_windows else "Ctrl+d"
    print(
        f"[Writing Entry; on a blank line, press {_how_to_quit} to finish writing]\n",
        file=sys.stderr,
    )
    try:
        raw = sys.stdin.read()
    except KeyboardInterrupt:
        logging.error("Write mode: keyboard interrupt")
        print("[Entry NOT saved to journal]", file=sys.stderr)
        sys.exit(0)

    return raw
