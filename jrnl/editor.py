# Copyright © 2012-2023 jrnl contributors
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
from jrnl.path import absolute_path
from jrnl.path import get_templates_path


def get_text_from_editor(config: dict, template: str = "") -> str:
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


def get_text_from_stdin() -> str:
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
        logging.error("Append mode: keyboard interrupt")
        raise JrnlException(
            Message(MsgText.KeyboardInterruptMsg, MsgStyle.ERROR_ON_NEW_LINE),
            Message(MsgText.JournalNotSaved, MsgStyle.WARNING),
        )

    return raw


def read_template_file(template_arg: str, template_path_from_config: str) -> str:
    """
    This function is called when either a template file is passed with --template, or config.template is set.

    The processing logic is:
        If --template was not used: Load the global template file.
        If --template was used:
            * Check $XDG_DATA_HOME/jrnl/templates/template_arg.
            * Check template_arg as an absolute / relative path.

        If a file is found, its contents are returned as a string.
        If not, a JrnlException is raised.
    """
    logging.debug(
        "Append mode: Either a template arg was passed, or the global config is set."
    )

    # If filename is unset, we are in this flow due to a global template being configured
    if not template_arg:
        logging.debug("Append mode: Global template configuration detected.")
        global_template_path = absolute_path(template_path_from_config)
        try:
            with open(global_template_path, encoding="utf-8") as f:
                template_data = f.read()
                return template_data
        except FileNotFoundError:
            raise JrnlException(
                Message(
                    MsgText.CantReadTemplateGlobalConfig,
                    MsgStyle.ERROR,
                    {
                        "global_template_path": global_template_path,
                    },
                )
            )
    else:  # A template CLI arg was passed.
        logging.debug("Trying to load template from $XDG_DATA_HOME/jrnl/templates/")
        jrnl_template_dir = get_templates_path()
        logging.debug(f"Append mode: jrnl templates directory: {jrnl_template_dir}")
        template_path = jrnl_template_dir / template_arg
        try:
            with open(template_path, encoding="utf-8") as f:
                template_data = f.read()
                return template_data
        except FileNotFoundError:
            logging.debug(
                f"Couldn't open {template_path}. Treating --template argument like a local / abs path."
            )
            pass

        normalized_template_arg_filepath = absolute_path(template_arg)
        try:
            with open(normalized_template_arg_filepath, encoding="utf-8") as f:
                template_data = f.read()
                return template_data
        except FileNotFoundError:
            raise JrnlException(
                Message(
                    MsgText.CantReadTemplateCLIArg,
                    MsgStyle.ERROR,
                    {
                        "normalized_template_arg_filepath": normalized_template_arg_filepath,
                        "jrnl_template_dir": template_path,
                    },
                )
            )
