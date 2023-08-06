from unittest import TestCase

from palaestrai.agent import RewardInformation
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.core.protocol import EnvironmentUpdateResponse
from palaestrai.simulation import VanillaSimControllerTerminationCondition
from palaestrai.types import Discrete


class TestVanillaSimControllerTerminationCondition(TestCase):
    def test_check_termination_true(self):
        term_cond = VanillaSimControllerTerminationCondition()
        self.assertTrue(
            term_cond.check_termination(
                EnvironmentUpdateResponse(
                    sender_environment_id="0",
                    receiver_simulation_controller_id="0",
                    experiment_run_id="0",
                    experiment_run_instance_id="0-0",
                    experiment_run_phase=47,
                    sensors=[SensorInformation(1, Discrete(1), 0)],
                    rewards=[RewardInformation(0.0, Discrete(1), "Test")],
                    is_terminal=True,
                )
            )
        )

    def test_check_termination_False(self):
        term_cond = VanillaSimControllerTerminationCondition()
        self.assertFalse(
            term_cond.check_termination(
                EnvironmentUpdateResponse(
                    sender_environment_id="0",
                    receiver_simulation_controller_id="0",
                    experiment_run_id="0",
                    experiment_run_instance_id="0-0",
                    experiment_run_phase=47,
                    sensors=[SensorInformation(1, Discrete(1), 0)],
                    rewards=[RewardInformation(0.0, Discrete(1), "Test")],
                    is_terminal=False,
                )
            )
        )
