import logging
import sys
import unittest
from unittest.mock import patch

from palaestrai.agent import SensorInformation, ActuatorInformation
from palaestrai.simulation.simulation_controller import (
    SimulationController,
    SimulationSetupError,
)
from palaestrai.types import Discrete
from palaestrai.types.mode import Mode


class SimulationControllerTest(unittest.IsolatedAsyncioTestCase):
    @patch.multiple(SimulationController, __abstractmethods__=set())
    def test__unassigned_sensors_actuators(self):
        sc = SimulationController(
            rungov_connection="none",
            sim_connection="none",
            termination_conditions=[],
            environment_conductor_ids=[],
            agent_conductor_ids=["ac1", "ac2", "ac3"],
            agents_config={
                "ac1": {  # All sensors/actuators: Ok.
                    "sensors": [
                        "myenv.0",
                        "myenv.1",
                        "myenv.2",
                        "myenv.3",
                        "myenv.4",
                    ],
                    "actuators": [
                        "myenv.0",
                        "myenv.1",
                        "myenv.2",
                        "myenv.3",
                        "myenv.4",
                    ],
                },
                "ac2": {
                    "sensors": [
                        "myenv.0",  # Ok
                        "1sensor_without_envid",  # No env ID
                        "myenv.snesor_with_typo",  # Typo in sensor
                    ],
                    "actuators": [
                        "myemv.4",  # Typo in env
                        "myenv.6",  # Does not exist.
                    ],
                },
                "ac3": {  # Only a subset of available sensors/actuators, ok.
                    "sensors": ["myenv.0", "myenv.4"],
                    "actuators": ["myenv.0", "myenv.1", "myenv.4"],
                },
            },
            mode=Mode.TEST,  # Pun intended.
        )
        sc._sensors = [
            SensorInformation(0, Discrete(1), f"myenv.{i}") for i in range(5)
        ]
        sc._actuators = [
            ActuatorInformation(0, Discrete(1), f"myenv.{i}") for i in range(5)
        ]

        self.assertDictEqual(
            sc._unassigned_sensors_actuators(),
            {
                "ac2": (
                    {"1sensor_without_envid", "myenv.snesor_with_typo"},
                    {"myemv.4", "myenv.6"},
                )
            },
        )

    @patch.multiple(SimulationController, __abstractmethods__=set())
    @patch(
        "palaestrai.simulation.SimulationController.access_list",
        lambda x, y: (x, y),
    )
    async def test_sc_bails_on_unassigned_sensors_or_actuators(self):
        sc = SimulationController(
            rungov_connection="none",
            sim_connection="none",
            termination_conditions=[],
            environment_conductor_ids=["hurr durr ima sheep"],
            agent_conductor_ids=["ac1", "ac2", "ac3"],
            agents_config={
                "ac1": {  # All sensors/actuators: Ok.
                    "sensors": [
                        "myenv.0",
                        "myenv.1",
                        "myenv.2",
                        "myenv.3",
                        "myenv.4",
                    ],
                    "actuators": [
                        "myenv.0",
                        "myenv.1",
                        "myenv.2",
                        "myenv.3",
                        "myenv.4",
                    ],
                },
                "ac2": {
                    "sensors": [
                        "myenv.0",  # Ok
                        "1sensor_without_envid",  # No env ID
                        "myenv.snesor_with_typo",  # Typo in sensor
                    ],
                    "actuators": [
                        "myemv.4",  # Typo in env
                        "myenv.6",  # Does not exist.
                    ],
                },
                "ac3": {  # Only a subset of available sensors/actuators, ok.
                    "sensors": ["myenv.0", "myenv.4"],
                    "actuators": ["myenv.0", "myenv.1", "myenv.4"],
                },
            },
            mode=Mode.TEST,  # Pun intended.
        )

        sc_sensors = [
            SensorInformation(0, Discrete(1), f"myenv.{i}") for i in range(5)
        ]
        sc_actuators = [
            ActuatorInformation(0, Discrete(1), f"myenv.{i}") for i in range(5)
        ]

        async def _return_dummy_answer(_, req):
            from palaestrai.core.protocol import (
                EnvironmentSetupRequest,
                EnvironmentSetupResponse,
                EnvironmentStartRequest,
                EnvironmentStartResponse,
            )

            if isinstance(req, EnvironmentSetupRequest):
                return EnvironmentSetupResponse(
                    environment_id="myenv",
                    experiment_run_id="dontcare",
                    sender_environment_conductor="dontcare",
                    receiver_simulation_controller="dontcare",
                    environment_type="DummyEnvironment",
                    environment_parameters={},
                )
            if isinstance(req, EnvironmentStartRequest):
                return EnvironmentStartResponse(
                    run_id="dontcare",
                    environment_id="myenv",
                    sensors=sc_sensors,
                    actuators=sc_actuators,
                )
            return "I don't know how to handle %s" % req

        sc._client = unittest.mock.AsyncMock(side_effect=_return_dummy_answer)
        with self.assertRaises(SimulationSetupError):
            await sc._init_simulation()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    unittest.main()
