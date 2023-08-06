import unittest
from unittest.mock import MagicMock, patch

from palaestrai.agent import (
    RewardInformation,
    ActuatorInformation,
    SensorInformation,
)
from palaestrai.agent.dummy_brain import DummyBrain
from palaestrai.agent.dummy_objective import DummyObjective
from palaestrai.agent.state import State
from palaestrai.core.protocol import MuscleUpdateRequest, MuscleShutdownRequest
from palaestrai.core.serialisation import serialize
from palaestrai.types import Discrete


class TestBrain(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.brain_params = {}
        self.muscle_update_req = MuscleUpdateRequest(
            sensors_available=[SensorInformation(1, Discrete(1), "S1")],
            actuators_available=[ActuatorInformation(1, Discrete(1), "A1")],
            network_input=[1, 1, 1, 1],
            last_network_output=[2, 2, 2, 2],
            reward=[RewardInformation(0.0, Discrete(1), "Test")],
            is_terminal=False,
            additional_data={},
        )
        self.muscle_shutdown_req = MuscleShutdownRequest(
            sender_muscle_id="0",
            experiment_run_id="2",
            agent_id="3",
        )
        self.brain = DummyBrain(
            "test-con",
            list(),
            list(),
            DummyObjective({}),
            "./test123/phase_test/testAgent",
            123,
            layers=2,
        )

    def test_process(self):
        self.brain._state = State.RUNNING
        self.brain._listen = MagicMock()
        self.brain._muscle_updates_socket = MagicMock()
        self.brain._muscle_updates_socket.recv_multipart = MagicMock()
        update_msg = serialize(self.muscle_update_req)
        shutdown_msg = serialize(self.muscle_shutdown_req)
        self.brain._muscle_updates_socket.recv_multipart.side_effect = [
            ["0", update_msg],
            ["0", shutdown_msg],
        ]
        self.brain._receive_updates()

        self.assertEqual(self.brain._muscle_updates_queue.qsize(), 2)
        self.assertFalse(self.brain._receive_updates())
        msg = self.brain._muscle_updates_queue.get()
        self.assertIsInstance(msg[0], MuscleUpdateRequest)
        self.assertEqual(msg[1], "0")

        # TODO: Change to MuscleShutdownRequest as soon as it is merged
        msg = self.brain._muscle_updates_queue.get()
        self.assertIsInstance(msg[0], MuscleShutdownRequest)
        self.assertEqual(msg[1], "0")

    @patch("palaestrai.agent.brain.Thread")
    async def test_run(self, mockthread):
        self.brain._state = State.RUNNING
        self.brain._send = MagicMock()
        self.brain.thinking = MagicMock(return_value=0)
        self.brain._muscle_updates_queue.put([self.muscle_update_req, "0"])
        self.brain._muscle_updates_queue.put([self.muscle_shutdown_req, "0"])

        await self.brain.run()

        mockthread.assert_called_once()
        self.brain.thinking.assert_called_once()
        self.assertEqual(self.brain._send.call_count, 2)
        self.assertNotEqual(self.brain.state, State.RUNNING)


if __name__ == "__main__":
    unittest.main()
