# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
import sys
import traceback

from jrnl.jrnl import run
from jrnl.args import parse_args
from jrnl.output import print_msg
from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgText
from jrnl.messages import MsgType


def configure_logger(debug=False):
    if not debug:
        logging.disable()
        return

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)-8s %(name)-12s %(message)s",
    )
    logging.getLogger("parsedatetime").setLevel(logging.INFO)
    logging.getLogger("keyring.backend").setLevel(logging.ERROR)


def cli(manual_args=None):
    try:
        if manual_args is None:
            manual_args = sys.argv[1:]

        args = parse_args(manual_args)
        configure_logger(args.debug)
        logging.debug("Parsed args: %s", args)

        return run(args)

    except JrnlException as e:
        e.print()
        return 1

    except KeyboardInterrupt:
        print_msg(Message(MsgText.KeyboardInterruptMsg, MsgType.WARNING))
        return 1

    except Exception as e:
        try:
            is_debug = args.debug  # type: ignore
        except NameError:
            # error happened before args were parsed
            is_debug = "--debug" in sys.argv[1:]

        if is_debug:
            traceback.print_tb(sys.exc_info()[2])

        print_msg(Message(MsgText.UncaughtException, MsgType.ERROR, {"exception": e}))
        return 1
