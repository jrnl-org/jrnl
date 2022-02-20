# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
import sys
import traceback

from .jrnl import run
from .args import parse_args
from .exception import JrnlException
from jrnl.output import print_msg
from jrnl.output import Message


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

        status_code = run(args)

    except JrnlException as e:
        status_code = 1
        print_msg(e.title, e.message, msg=Message.ERROR)

    except KeyboardInterrupt:
        status_code = 1
        print_msg("\nKeyboardInterrupt", "\nAborted by user", msg=Message.ERROR)

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
            print("\n")
            traceback.print_tb(sys.exc_info()[2])

        file_issue = (
            "\n\nThis is probably a bug. Please file an issue at:"
            + "\nhttps://github.com/jrnl-org/jrnl/issues/new/choose"
        )
        print_msg(f"{type(e).__name__}\n", f"{e}{file_issue}", msg=Message.ERROR)

    # This should be the only exit point
    return status_code
