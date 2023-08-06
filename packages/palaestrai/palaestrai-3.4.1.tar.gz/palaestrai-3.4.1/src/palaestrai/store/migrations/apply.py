#!/usr/bin/env python3

import os
import alembic.config
from palaestrai.core import RuntimeConfig


def main():
    config = RuntimeConfig()
    try:
        config.load()
        if not config.store_uri:
            raise KeyError()
    except KeyError:
        print(
            "Please create a runtime config (one of %s), "
            "and set the 'store_uri' options.\n"
            "My configuration, loaded from %s, does not contain it."
            % (config.CONFIG_FILE_PATHS, config._config_file_path)
        )
        exit(1)
    except FileNotFoundError as e:
        print(
            "Please create a runtime config " "and set the 'store_uri' option."
        )
        print("%s." % e)
        exit(1)
    here = os.path.dirname(os.path.abspath(__file__))
    alembic_args = ["-c", os.path.join(here, "alembic.ini"), "upgrade", "head"]
    alembic.config.main(argv=alembic_args)
