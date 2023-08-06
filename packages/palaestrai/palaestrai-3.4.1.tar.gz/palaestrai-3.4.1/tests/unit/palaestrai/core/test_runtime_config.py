import unittest
from copy import deepcopy
from pathlib import Path

from palaestrai.core.runtime_config import RuntimeConfig, _RuntimeConfig


class RuntimeConfigTestCase(unittest.TestCase):
    def test_singleton(self):
        self.assertEqual(id(RuntimeConfig()), id(RuntimeConfig()))

    def test_implicit_load(self):
        c = RuntimeConfig()
        self.assertTrue(c._loaded_configuration)

    def test_load_from_file(self):
        c = RuntimeConfig()
        self.assertTrue(c._config_file_path)
        config_file_path = (
            Path(__file__).parent
            / ".."
            / ".."
            / ".."
            / "fixtures"
            / "palaestrai-runtime-debug.conf.yaml"
        )
        c.load(config_file_path)
        self.assertTrue(c._config_file_path)
        self.assertEqual(c._config_file_path, str(config_file_path))

    def test_load_from_stream(self):
        from io import StringIO

        custom_store_uri = "psql://foo:bar@baz.example.com/meeple"
        stream = StringIO("---\nstore_uri: %s" % custom_store_uri)
        RuntimeConfig().reset()
        RuntimeConfig().load(stream)
        self.assertEqual(RuntimeConfig().store_uri, custom_store_uri)

    def test_modifiable_config_and_immutable_loaded_config(self):
        c = _RuntimeConfig()
        c._loaded_configuration = deepcopy(_RuntimeConfig.DEFAULT_CONFIG)
        self.assertIsNotNone(c.store_uri)
        self.assertEqual(c.store_uri, "sqlite:///palaestrai.db")
        self.assertEqual(
            c.store_uri, _RuntimeConfig.DEFAULT_CONFIG["store_uri"]
        )
        c._loaded_configuration["store_uri"] = None
        self.assertIsNotNone(c.store_uri)
        self.assertEqual(
            c.store_uri, _RuntimeConfig.DEFAULT_CONFIG["store_uri"]
        )

    def test_implicit_default_config(self):
        c = _RuntimeConfig()
        self.assertEqual(
            c._get("executor_bus_port"),
            _RuntimeConfig.DEFAULT_CONFIG["executor_bus_port"],
        )

    def test_load_from_dict(self):
        c = _RuntimeConfig()
        c.load({"store_uri": "Foo"})
        self.assertEqual(c.store_uri, "Foo")
        self.assertEqual(
            c.executor_bus_port,
            _RuntimeConfig.DEFAULT_CONFIG["executor_bus_port"],
        )

    def test_reset_with_dict(self):
        c = _RuntimeConfig()
        c.load({"store_uri": "Foo"})
        self.assertEqual(c.store_uri, "Foo")

        c.reset()
        self.assertIsNone(c._config_file_path)
        self.assertDictEqual(c._loaded_configuration, {})
        self.assertEqual(
            c.store_uri, _RuntimeConfig.DEFAULT_CONFIG["store_uri"]
        )

    def test_reset(self):
        c = _RuntimeConfig()
        self.assertEqual(
            c.store_uri, _RuntimeConfig.DEFAULT_CONFIG["store_uri"]
        )
        c._store_uri = None
        self.assertIsNone(c.store_uri)
        c.reset()
        self.assertEqual(
            c.store_uri, _RuntimeConfig.DEFAULT_CONFIG["store_uri"]
        )

    def test_load_only_more_specific(self):
        custom_store_uri = "example://test"
        c = _RuntimeConfig()
        c.load()
        c.load({"store_uri": custom_store_uri})
        self.assertEqual(c.store_uri, custom_store_uri)
        c.load()
        self.assertEqual(c.store_uri, custom_store_uri)


if __name__ == "__main__":
    unittest.main()
