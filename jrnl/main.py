# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
import sys
import traceback

from rich.logging import RichHandler

from jrnl import controller
from jrnl.args import parse_args
from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg


def configure_logger(debug: bool = False) -> None:
    if not debug:
        logging.disable()
        return

    logging.basicConfig(
        level=logging.DEBUG,
        datefmt="[%X]",
        format="%(message)s",
        handlers=[RichHandler()],
    )
    logging.getLogger("parsedatetime").setLevel(logging.INFO)
    logging.getLogger("keyring.backend").setLevel(logging.ERROR)
    logging.debug("Logging start")


def run(manual_args: list[str] | None = None) -> int:
    try:
        if manual_args is None:
            manual_args = sys.argv[1:]

        args = parse_args(manual_args)
        configure_logger(args.debug)
        logging.debug("Parsed args:\n%s", args)

        status_code = controller.run(args)

    except JrnlException as e:
        status_code = 1
        e.print()

    except KeyboardInterrupt:
        status_code = 1

        print_msg(
            Message(
                MsgText.KeyboardInterruptMsg,
                MsgStyle.ERROR_ON_NEW_LINE,
            )
        )

    except Exception as e:
        # uncaught exception
        status_code = 1
        debug = False
        try:
            if args.debug:  # type: ignore
                debug = True
        except NameError:
            # This should only happen when the exception
            # happened before the args were parsed
            if "--debug" in sys.argv:
                debug = True

        if debug:
            from rich.console import Console

            traceback.print_tb(sys.exc_info()[2])
            Console(stderr=True).print_exception(extra_lines=1)

        print_msg(
            Message(
                MsgText.UncaughtException,
                MsgStyle.ERROR,
                {"name": type(e).__name__, "exception": e},
            )
        )

    # This should be the only exit point
    return status_code
