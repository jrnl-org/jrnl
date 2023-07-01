# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from .Config import Config
from .BaseConfigReader import BaseConfigReader
from .DefaultConfigReader import DefaultConfigReader
from .FileConfigReader import FileConfigReader
from .ArgsConfigReader import ArgsConfigReader


def get_config(args):
    config = Config()

    try:
        # these are in ascending priority (last one has most priority)
        config.add_config([
            DefaultConfigReader(),
        ])

        config.add_config([
            FileConfigReader(args.config_file),
            FileConfigReader(config.get_config_path()),
            FileConfigReader(jrnlV1Path),
        ], required=True)

        config.add_config([
            ArgsConfigReader(args.config_override),
        ])

        # config.add_config(EnvConfigReader(env.whatever))
        config.validate()

    except e:
        # TODO: catch warnings instead of fatal exceptions

    return config
