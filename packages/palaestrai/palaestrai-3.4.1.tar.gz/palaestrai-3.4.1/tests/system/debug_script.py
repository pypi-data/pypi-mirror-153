import os
import sys

from palaestrai.cli.manager import cli

if __name__ == "__main__":
    sys.path.insert(
        0, os.path.abspath(os.path.join(__file__, "..", "..", ".."))
    )
    from tests.system.test_cli import debug_script_path, runtime_path

    cli(["-c", runtime_path, "experiment-start", debug_script_path])
