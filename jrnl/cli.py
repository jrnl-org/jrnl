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

        return run(args)

    except JrnlException as e:
        print_msg(e.title, e.message, msg=Message.ERROR)
        return 1

    except KeyboardInterrupt:
        print_msg("KeyboardInterrupt", "Aborted by user", msg=Message.ERROR)
        return 1

    except Exception as e:
        # uncaught exception
        if args.debug:
            print("\n")
            traceback.print_tb(sys.exc_info()[2])
            return 1

        print_msg(f"{type(e).__name__}\n", str(e), msg=Message.ERROR)
        return 1
