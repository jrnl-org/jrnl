#!/usr/bin/env python
"""
    jrnl

    license: GPLv3, see LICENSE.md for more details.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import logging
import sys

from . import jrnl
from . import install

from .parse_args import parse_args
from .config import scope_config
from .exception import UserAbort
from .Journal import open_journal
from .config import get_journal_name


def configure_logger(debug=False):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.ERROR,
        format="%(levelname)-8s %(name)-12s %(message)s",
    )
    logging.getLogger("parsedatetime").setLevel(logging.INFO)
    logging.getLogger("keyring.backend").setLevel(logging.ERROR)


def run(manual_args=None):
    """
    Flow:
    1. Parse cli arguments
    2. Run standalone command if it doesn't require config (help, version, etc), then exit
    3. Load config
    4. Run standalone command if it does require config (encrypt, decrypt, etc), then exit
    5. Load specified journal
    6. Start write mode, or search mode
    7. Profit
    """
    if manual_args is None:
        manual_args = sys.argv[1:]

    args = parse_args(manual_args)
    configure_logger(args.debug)
    logging.debug("Parsed args: %s", args)

    # Run command if possible before config is available
    if callable(args.preconfig_cmd):
        args.preconfig_cmd(args)
        sys.exit(0)

    # Load the config, and extract journal name
    try:
        config = install.load_or_install_jrnl()
        original_config = config.copy()
        args = get_journal_name(args, config)
        config = scope_config(config, args.journal_name)
    except UserAbort as err:
        print(f"\n{err}", file=sys.stderr)
        sys.exit(1)

    # Run post-config command now that config is ready
    if callable(args.postconfig_cmd):
        args.postconfig_cmd(args=args, config=config, original_config=original_config)
        sys.exit(0)

    # --- All the standalone commands are now done --- #

    # Get the journal we're going to be working with
    journal = open_journal(args.journal_name, config)

    kwargs = {
        "args": args,
        "config": config,
        "journal": journal,
    }

    if jrnl._is_write_mode(**kwargs):
        jrnl.write_mode(**kwargs)
    else:
        jrnl.search_mode(**kwargs)

    # All done!
