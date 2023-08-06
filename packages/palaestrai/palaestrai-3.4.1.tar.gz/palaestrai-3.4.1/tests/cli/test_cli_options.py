import unittest
from copy import deepcopy
from tempfile import NamedTemporaryFile

from click.testing import CliRunner
from ruamel.yaml import YAML

from palaestrai.cli.manager import cli
from palaestrai.core.runtime_config import _RuntimeConfig, RuntimeConfig


class CliOptionsTest(unittest.TestCase):
    def test_runtime_config_load_path(self):
        runner = CliRunner()
        pseudo_store_uri = "demo://example.com"
        cfg_hash = deepcopy(_RuntimeConfig.DEFAULT_CONFIG)
        cfg_hash["store_uri"] = pseudo_store_uri

        tmpfile = NamedTemporaryFile(mode="w+")
        yml = YAML(typ="safe")
        yml.dump(cfg_hash, tmpfile)
        tmpfile.flush()
        print(tmpfile.name)
        result = runner.invoke(
            cli, ["-c", tmpfile.name, "runtime-config-show-effective"]
        )
        self.assertEqual(RuntimeConfig().store_uri, pseudo_store_uri)
        tmpfile.close()
