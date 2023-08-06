import io
import os.path
import sys
import unittest
import uuid
from unittest.mock import MagicMock, patch
from palaestrai.util.exception import EnvironmentHasNoUIDError

import pkg_resources

from palaestrai.experiment.experiment_run import ExperimentRun


class _UidentifiableMock(MagicMock):
    def __init__(self, id=None):
        super().__init__()
        self.uid = id if id else str(uuid.uuid4())


def load_with_params_side_effect(*args, **kwargs):
    return _UidentifiableMock()


@patch(
    "palaestrai.experiment.experiment_run.AgentConductor",
    MagicMock(side_effect=load_with_params_side_effect),
)
@patch(
    "palaestrai.experiment.experiment_run.load_with_params",
    MagicMock(side_effect=load_with_params_side_effect),
)
class TestExperimentRun(unittest.TestCase):
    def setUp(self):
        self.version = pkg_resources.require("palaestrai")[0].version
        self.dummy_exp_path = os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../../fixtures/dummy_run.yml",
            )
        )
        self.invalid_exp_path = os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../../fixtures/invalid_run.yml",
            )
        )
        self.schedule = [
            {
                "phase_0": {
                    "environments": [
                        {
                            "environment": {
                                "name": "",
                                "uid": "myenv",
                                "params": dict(),
                            },
                            # "reward": {"name": "", "params": dict()},
                        }
                    ],
                    "agents": [
                        {
                            "name": "defender",
                            "brain": {"name": "", "params": dict()},
                            "muscle": {"name": "", "params": dict()},
                            "objective": {"name": "", "params": dict()},
                            "sensors": list(),
                            "actuators": list(),
                        },
                        {
                            "name": "attacker",
                            "brain": {"name": "", "params": dict()},
                            "muscle": {"name": "", "params": dict()},
                            "objective": {"name": "", "params": dict()},
                            "sensors": list(),
                            "actuators": list(),
                        },
                    ],
                    "simulation": {
                        "name": "",
                        "params": dict(),
                        "conditions": list(),
                    },
                    "phase_config": {"mode": "train", "worker": 1},
                }
            }
        ]
        self.run_config = {
            "condition": {
                "name": (
                    "palaestrai.experiment:"
                    "VanillaRunGovernorTerminationCondition",
                ),
                "params": dict(),
            }
        }

        self.schedule_p2 = {
            "phase_1": {
                "environments": [
                    {
                        "environment": {
                            "name": "",
                            "uid": "myenv",
                            "params": dict(),
                        },
                        # "reward": {"name": "", "params": dict()},
                    }
                ],
                "agents": [
                    {
                        "name": "defender",
                        "brain": {"name": "", "params": dict()},
                        "muscle": {"name": "", "params": dict()},
                        "objective": {"name": "", "params": dict()},
                        "sensors": list(),
                        "actuators": list(),
                    },
                ],
                "simulation": {
                    "name": "",
                    "params": dict(),
                    "conditions": list(),
                },
                "phase_config": {"mode": "test", "worker": 1},
            }
        }
        self.schedule_p3 = {
            "phase_1": {
                "environments": [
                    {
                        "environment": {
                            "name": "",
                            "uid": "myenv",
                            "params": dict(),
                        },
                        # "reward": {"name": "", "params": dict()},
                    }
                ],
                "agents": [
                    {
                        "name": "attacker",
                        "brain": {"name": "", "params": dict()},
                        "muscle": {"name": "", "params": dict()},
                        "objective": {"name": "", "params": dict()},
                        "sensors": list(),
                        "actuators": list(),
                    },
                ],
                "simulation": {
                    "name": "",
                    "params": dict(),
                    "conditions": list(),
                },
                "phase_config": {"mode": "train", "worker": 3},
            }
        }

    def test_properties(self):
        """Assert Not Empty list"""
        exp = ExperimentRun(
            uid="test_properties",
            seed=123,
            version=self.version,
            schedule=self.schedule,
            run_config=self.run_config,
        )

        self.assertFalse(hasattr(exp, "schedule"))

    def test_setup_one_phase(self):
        """Assert setup"""
        exp = ExperimentRun(
            uid="test_setup",
            seed=123,
            version=self.version,
            schedule=self.schedule,
            run_config=self.run_config,
        )
        exp.setup(broker_uri=None)
        self.assertEqual(len(exp.schedule_config), len(exp.schedule))
        self.assertEqual(1, len(exp.environment_conductors(0)))
        self.assertEqual(2, len(exp.agent_conductors(0)))
        self.assertEqual(1, len(exp.simulation_controllers(0)))

    def test_setup_three_phase(self):
        self.schedule.append(self.schedule_p2)
        self.schedule.append(self.schedule_p3)
        exp = ExperimentRun(
            uid="test_setup",
            seed=123,
            version=self.version,
            schedule=self.schedule,
            run_config=self.run_config,
        )
        exp.setup(broker_uri=None)
        self.assertEqual(len(exp.schedule_config), len(exp.schedule))
        self.assertEqual(1, len(exp.environment_conductors(0)))
        self.assertEqual(2, len(exp.agent_conductors(0)))
        self.assertEqual(1, len(exp.simulation_controllers(0)))
        self.assertEqual(1, len(exp.environment_conductors(1)))

        # One agent was removed in phase 2
        self.assertEqual(1, len(exp.agent_conductors(1)))
        self.assertEqual(1, len(exp.simulation_controllers(1)))
        self.assertEqual(1, len(exp.environment_conductors(2)))
        self.assertEqual(1, len(exp.agent_conductors(2)))

        # Now we have three workers
        self.assertEqual(3, len(exp.simulation_controllers(2)))

    def test_single_env_has_no_uid_tc1(self):
        """This functions tests the behavior when a single environment
        has no UID.

        TestCase 1
        ----------
        A single environment that is used in two phases. The
        environment re-uses the definition from the first phase.

        Expected outcome
        ----------------
        Setup should fail.

        """
        s2p_single_env_p1_no_uid = [
            {
                "phase_0": {
                    "environments": [
                        {
                            "environment": {
                                "name": "",
                                "params": dict(),
                            },
                            # "reward": {"name": "", "params": dict()},
                        }
                    ],
                    "agents": [
                        {
                            "name": "defender",
                            "brain": {"name": "", "params": dict()},
                            "muscle": {"name": "", "params": dict()},
                            "objective": {"name": "", "params": dict()},
                            "sensors": list(),
                            "actuators": list(),
                        },
                        {
                            "name": "attacker",
                            "brain": {"name": "", "params": dict()},
                            "muscle": {"name": "", "params": dict()},
                            "objective": {"name": "", "params": dict()},
                            "sensors": list(),
                            "actuators": list(),
                        },
                    ],
                    "simulation": {
                        "name": "",
                        "params": dict(),
                        "conditions": list(),
                    },
                    "phase_config": {"mode": "train", "worker": 1},
                }
            },
            {
                "phase_1": {
                    "phase_config": {"mode": "test", "worker": 1},
                }
            },
        ]
        exp = ExperimentRun(
            uid="test_setup",
            seed=123,
            version=self.version,
            schedule=s2p_single_env_p1_no_uid,
            run_config=self.run_config,
        )
        self.assertRaises(EnvironmentHasNoUIDError, exp.setup, broker_uri=None)

        # We are happy if no exception is raised and don't need an
        # assert here.

    def test_single_env_has_no_uid_tc2(self):
        """This functions tests the behavior when a single environment
        has no UID.

        TestCase 2
        ----------
        A single environment that is used in two phases. However, in
        the definition of the second phase, the UID is missing.

        Expected outcome
        ----------------
        Setup should fail. The connection between the environment in
        the first phase and the environment in the second phase is
        purely on a semantical level. PalaestrAI can't know that those
        are identically (they're probably not, why else is there a
        second definition?).

        """
        s2p_single_env_p1_uid_p2_no_uid = [
            {
                "phase_0": {
                    "environments": [
                        {
                            "environment": {
                                "name": "",
                                "uid": "myenv",
                                "params": dict(),
                            },
                            # "reward": {"name": "", "params": dict()},
                        }
                    ],
                    "agents": [
                        {
                            "name": "defender",
                            "brain": {"name": "", "params": dict()},
                            "muscle": {"name": "", "params": dict()},
                            "objective": {"name": "", "params": dict()},
                            "sensors": list(),
                            "actuators": list(),
                        },
                        {
                            "name": "attacker",
                            "brain": {"name": "", "params": dict()},
                            "muscle": {"name": "", "params": dict()},
                            "objective": {"name": "", "params": dict()},
                            "sensors": list(),
                            "actuators": list(),
                        },
                    ],
                    "simulation": {
                        "name": "",
                        "params": dict(),
                        "conditions": list(),
                    },
                    "phase_config": {"mode": "train", "worker": 1},
                }
            },
            {
                "phase_1": {
                    "environments": [
                        {"environment": {"name": "", "params": dict()}}
                    ]
                }
            },
        ]
        exp = ExperimentRun(
            uid="test_setup",
            seed=123,
            version=self.version,
            schedule=s2p_single_env_p1_uid_p2_no_uid,
            run_config=self.run_config,
        )
        self.assertRaises(EnvironmentHasNoUIDError, exp.setup, broker_uri=None)

    def test_multi_env_has_no_uid(self):
        pass

    def test_load_from_file(self):
        exp = ExperimentRun.load(self.dummy_exp_path)
        self.assertFalse(hasattr(exp, "schedule"))

    def test_load_from_stream(self):
        with open(self.dummy_exp_path, "r") as stream_:
            exp = ExperimentRun.load(stream_)

        self.assertFalse(hasattr(exp, "schedule"))

    def test_subseeds_are_reproducible(self):
        exp1 = ExperimentRun(
            uid="test_properties",
            seed=123,
            version=self.version,
            schedule=self.schedule,
            run_config=self.run_config,
        )
        exp2 = ExperimentRun(
            uid="test_properties",
            seed=123,
            version=self.version,
            schedule=self.schedule,
            run_config=self.run_config,
        )

        for i in range(10):
            sub_seed1 = exp1.create_subseed()
            sub_seed2 = exp2.create_subseed()
            self.assertEqual(sub_seed1, sub_seed2)

    def test_subseeds_from_None_not_equal(self):
        exp1 = ExperimentRun(
            uid="test_properties",
            seed=None,
            version=self.version,
            schedule=self.schedule,
            run_config=self.run_config,
        )
        exp2 = ExperimentRun(
            uid="test_properties",
            seed=None,
            version=self.version,
            schedule=self.schedule,
            run_config=self.run_config,
        )
        list1 = []
        list2 = []
        for i in range(10):
            sub_seed1 = exp1.create_subseed()
            list1.append(sub_seed1)
            sub_seed2 = exp2.create_subseed()
            list2.append(sub_seed2)
        self.assertFalse(set(list1) == set(list2))

    def test_subseeds_from_None(self):
        exp1 = ExperimentRun(
            uid="test_properties",
            seed=None,
            version=self.version,
            schedule=self.schedule,
            run_config=self.run_config,
        )
        list1 = []
        for i in range(10):
            sub_seed1 = exp1.create_subseed()
            list1.append(sub_seed1)
        self.assertTrue(len(list1) == 10)

    def test_load_from_stringio(self):
        with open(self.dummy_exp_path, "r") as stream_:
            experiment_run_document = stream_.read()
        sio = io.StringIO(experiment_run_document)
        try:
            exp = ExperimentRun.load(sio)
        except Exception as e:
            self.fail("ExperimentRun.load(StringIO) raised: %s" % e)
        self.assertIsNotNone(exp)

    def test_valid_syntax_check(self):
        syntax_check = ExperimentRun.check_syntax(self.dummy_exp_path)
        self.assertEqual(syntax_check.is_valid, True)

    def test_invalid_syntax_check(self):
        syntax_check = ExperimentRun.check_syntax(self.invalid_exp_path)
        self.assertEqual(syntax_check.is_valid, False)


class TestExperimentRunDump(unittest.TestCase):
    """Needed a separate test to get rid of the patches."""

    def test_dump(self):
        from io import StringIO

        import ruamel.yaml as yml
        from palaestrai.experiment import ExperimentRun

        dummy_exp_path = os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../../fixtures/dummy_run.yml",
            )
        )
        sio = StringIO()
        yaml = yml.YAML(typ="safe")
        yaml.register_class(ExperimentRun)
        exp = ExperimentRun.load(dummy_exp_path)
        yaml.dump(exp, sio)

        exp_loaded = yaml.load(sio.getvalue())
        self.assertEqual(sys.getsizeof(exp), sys.getsizeof(exp_loaded))


if __name__ == "__main__":
    unittest.main()
