import unittest
from unittest.mock import MagicMock, PropertyMock, AsyncMock, patch
from uuid import uuid4

from palaestrai.agent import (
    ActuatorInformation,
    SensorInformation,
    RewardInformation,
)
from palaestrai.agent.dummy_muscle import DummyMuscle
from palaestrai.core.protocol import (
    AgentUpdateRequest,
    AgentUpdateResponse,
    EnvironmentResetNotificationRequest,
    EnvironmentResetNotificationResponse,
    MuscleUpdateRequest,
    MuscleUpdateResponse,
    AgentShutdownRequest,
    AgentShutdownResponse,
)
from palaestrai.core.serialisation import serialize
from palaestrai.types import Discrete
from palaestrai.types.mode import Mode


class TestMuscle(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.uid = str(uuid4())
        agent_id = "agent"
        experiment_run_id = "exp_42"

        patch(
            "palaestrai.agent.dummy_muscle.Muscle.dealer_socket",
            new_callable=PropertyMock,
        ).start()
        patch("palaestrai.agent.dummy_muscle.DummyMuscle.update").start()
        patch(
            "palaestrai.agent.dummy_muscle.DummyMuscle.propose_actions",
            return_value=[
                ActuatorInformation(0.237, Discrete(1), 0),
                ActuatorInformation(0.237, Discrete(1), 0),
                [0, 1, 2],
                {},
            ],
        ).start()
        patch("palaestrai.agent.muscle.signal", spec=True).start()
        self.addCleanup(patch.stopall)

        self.test_muscle = DummyMuscle(
            broker_uri="broker",
            brain_uri="brain",
            uid=self.uid,
            brain_id="0",
            path=".",
        )

        self.msg_agent_update_req = AgentUpdateRequest(
            sender_simulation_controller_id="0815",
            receiver_agent_id=agent_id,
            experiment_run_id=experiment_run_id,
            experiment_run_instance_id="TotallyRandomUUIDString",
            experiment_run_phase=47,
            actuators=[ActuatorInformation(0, Discrete(1), 0)],
            sensors=[SensorInformation(1, Discrete(1), 0)],
            rewards=[RewardInformation(0.897, Discrete(1), "Test")],
            is_terminal=False,
            mode=Mode.TRAIN,
        )

        self.msg_muscle_update_res = MuscleUpdateResponse(
            is_updated=True, updates=[0, 0, 0]
        )

        self.msg_agent_shutdown_req = AgentShutdownRequest(
            run_id=experiment_run_id,
            agent_id=agent_id,
            complete_shutdown=True,
        )

    def test_send_to_brain(self):
        muscle_update_req = MuscleUpdateRequest(
            sensors_available=[SensorInformation(1, Discrete(1), "S1")],
            actuators_available=[ActuatorInformation(1, Discrete(1), "A1")],
            network_input=[1, 1, 1, 1],
            last_network_output=[2, 2, 2, 2],
            reward=[RewardInformation(0.0, Discrete(1), "Test")],
            is_terminal=False,
            additional_data={},
        )

        self.test_muscle.dealer_socket.recv_multipart = MagicMock(
            return_value=[serialize(self.msg_muscle_update_res)]
        )
        response = self.test_muscle.send_to_brain(muscle_update_req)
        self.test_muscle.dealer_socket.send.assert_called_with(
            serialize(muscle_update_req), flags=0
        )
        self.assertEqual(response.is_updated, True)

    async def test_run(self):
        self.test_muscle.worker.transceive = AsyncMock(
            side_effect=[
                self.msg_agent_update_req,
                self.msg_agent_shutdown_req,
                None,
            ]
        )
        self.test_muscle._handle_agent_update = MagicMock(return_value=None)
        self.test_muscle._handle_agent_shutdown = MagicMock(return_value=None)

        await self.test_muscle.run()

        self.assertEqual(3, self.test_muscle.worker.transceive.call_count)
        self.test_muscle._handle_agent_update.assert_called_once()
        self.test_muscle._handle_agent_shutdown.assert_called_once()
        self.test_muscle.worker.transceive.assert_awaited()

    async def test_handle_agent_update(self):
        self.test_muscle.send_to_brain = MagicMock(
            return_value=self.msg_muscle_update_res
        )
        response = self.test_muscle._handle_agent_update(
            self.msg_agent_update_req
        )

        self.assertEqual("exp_42", self.test_muscle.run_id)
        self.assertIsInstance(response, AgentUpdateResponse)

    def test_handle_environment_reset_notification(self):
        result = self.test_muscle.handle_environment_reset_notification(
            EnvironmentResetNotificationRequest("0", "1")
        )
        self.assertIsInstance(result, EnvironmentResetNotificationResponse)

    async def test_handle_agent_shutdown(self):
        self.test_muscle.send_to_brain = MagicMock(return_value=None)
        response = self.test_muscle._handle_agent_shutdown(
            self.msg_agent_shutdown_req
        )
        self.assertIsInstance(response, AgentShutdownResponse)


if __name__ == "__main__":
    unittest.main()
