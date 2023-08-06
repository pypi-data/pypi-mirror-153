from unittest.mock import MagicMock

from palaestrai.experiment import ExperimentRun

from palaestrai.entrypoints import palaestrai_runner

from ruamel.yaml import YAML

import palaestrai
import tempfile
import os
import unittest
import mock


async def state_is_42(to_be_discarded):
    return 42


@mock.patch("palaestrai.experiment.Executor.execute", state_is_42)
class TestEnvironment(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.dummy_exp_path = os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../../fixtures/dummy_run.yml",
            )
        )
        self.runtime_path = os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../../fixtures/palaestrai-runtime-debug.conf.yaml",
            )
        )

    def test_experiment_run(self):
        exp_run = ExperimentRun.load(self.dummy_exp_path)
        experiment_id, executor_final_state = palaestrai.execute(exp_run)

    def test_text_io(self):
        with open(self.dummy_exp_path) as exp_text_io:
            experiment_id, executor_final_state = palaestrai.execute(
                exp_text_io
            )

    def test_str(self):
        experiment_id, executor_final_state = palaestrai.execute(
            self.dummy_exp_path
        )

    def test_runtime_config_str(self):
        experiment_id, executor_final_state = palaestrai.execute(
            self.dummy_exp_path,
            self.runtime_path,
        )

    def test_runtime_config_text_io(self):
        with open(self.runtime_path, "r") as rt_text_io:
            experiment_id, executor_final_state = palaestrai.execute(
                self.dummy_exp_path, rt_text_io
            )

    def test_runtime_config_dict(self):
        with open(self.runtime_path) as rt_text_io:
            rt_dict = YAML(typ="safe").load(rt_text_io)
        experiment_id, executor_final_state = palaestrai.execute(
            self.dummy_exp_path, rt_dict
        )

    def test_runtime_config_none(self):
        experiment_id, executor_final_state = palaestrai.execute(
            self.dummy_exp_path
        )

    @mock.patch(
        "palaestrai.experiment.ExperimentRun.load",
        MagicMock(return_value=MagicMock()),
    )
    @mock.patch("asyncio.run", MagicMock(return_value=MagicMock()))
    def test_load_from_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "testexperiment.yml"), "w") as _:
                pass
            with open(os.path.join(tmpdir, "testexperiment2.yml"), "w") as _:
                pass
            with open(
                os.path.join(tmpdir, "notatestexperiment.notyml"), "w"
            ) as _:
                pass
            palaestrai.execute(tmpdir)
            self.assertEqual(
                palaestrai_runner.ExperimentRun.load.call_count, 2
            )

    @mock.patch(
        "palaestrai.experiment.ExperimentRun.load",
        MagicMock(return_value=MagicMock()),
    )
    @mock.patch("asyncio.run", MagicMock(return_value=MagicMock()))
    def test_load_from_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "testexperiment.yml")
            with open(path, "w") as _:
                pass
            palaestrai.execute(path)
            palaestrai_runner.ExperimentRun.load.assert_called_once()


if __name__ == "__main__":
    unittest.main()
