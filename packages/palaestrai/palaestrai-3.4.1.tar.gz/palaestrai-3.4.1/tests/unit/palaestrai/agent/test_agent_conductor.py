import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from palaestrai.agent.actuator_information import ActuatorInformation
from palaestrai.agent.agent_conductor import AgentConductor
from palaestrai.agent.dummy_brain import DummyBrain
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.core.protocol import (
    AgentSetupRequest,
    AgentSetupResponse,
    ShutdownRequest,
)


class TestAgentConductor(unittest.IsolatedAsyncioTestCase):
    def setUp(self):

        self.agent_params = {
            "name": "defender",
            "brain": {
                "name": "palaestrai.agent.dummy_brain:DummyBrain",
                "params": {},
            },
            "muscle": {
                "name": "palaestrai.agent.dummy_muscle:DummyMuscle",
                "params": {},
            },
            "objective": {
                "name": "palaestrai.agent.dummy_objective:DummyObjective",
                "params": {"params": 1},
            },
            "sensors": [SensorInformation(0, MagicMock(), "TestSensor-1")],
            "actuators": [
                ActuatorInformation(0, MagicMock(), "TestActuator-1")
            ],
        }

        self.ac = AgentConductor(
            "test_conn", self.agent_params, 0, str(uuid4())
        )
        self.setup_req = AgentSetupRequest(
            receiver_agent_conductor=self.ac.uid,
            sender_simulation_controller="0",
            experiment_run_id="1",
            experiment_run_instance_id="SomeInstance",
            experiment_run_phase=42,
            configuration=self.agent_params,
            agent_id="2",
            sensors=[
                SensorInformation(0, MagicMock(), "TestSensor-1"),
                SensorInformation(0, MagicMock(), "TestSensor-2"),
            ],
            actuators=[
                ActuatorInformation(0, MagicMock(), "TestActuator-1"),
                ActuatorInformation(0, MagicMock(), "TestActuator-2"),
            ],
            agent_name="TestAgent",
        )
        self.setup_req_empty = AgentSetupRequest(
            receiver_agent_conductor=self.ac.uid,
            sender_simulation_controller="0",
            experiment_run_instance_id="SomeExperimentRunInstance",
            experiment_run_phase=47,
            configuration=self.agent_params,
            experiment_run_id="1",
            agent_id="2",
            sensors=list(),
            actuators=list(),
            agent_name="TestAgent",
        )
        self.shutdown_req = ShutdownRequest("1")

    @patch("palaestrai.agent.agent_conductor.aiomultiprocess.Process")
    def test_init_brain(self, mockaio):
        self.ac._init_brain(self.setup_req.sensors, self.setup_req.actuators)

        self.assertEqual(mockaio.call_count, 1)
        self.assertIsInstance(self.ac._brain, DummyBrain)
        self.assertEqual(len(self.ac._brain.sensors), 2)
        self.assertEqual(len(self.ac._brain.actuators), 2)

    @patch("palaestrai.agent.agent_conductor.aiomultiprocess.Process")
    def test_init_muscle(self, mockaio):
        self.ac._init_muscle(uuid4(), "tcp://127.0.0.1:424242")

        self.assertEqual(mockaio.call_count, 1)
        self.assertEqual(len(self.ac.agents), 1)
        self.assertEqual(len(self.ac.tasks), 1)

    @patch("palaestrai.agent.agent_conductor.aiomultiprocess.Process")
    def test_handle_agent_setup(self, mockaio):
        self.ac._init_brain = MagicMock()
        self.ac._init_muscle = MagicMock()

        rsp = self.ac._handle_agent_setup(self.setup_req)
        self.ac._init_brain.assert_called_once()
        self.ac._init_muscle.assert_called()
        self.assertIsInstance(rsp, AgentSetupResponse)

    @patch("palaestrai.agent.agent_conductor.aiomultiprocess.Process")
    async def test_handle_shutdown(self, mockaio):
        self.ac._brain_process = AsyncMock()
        self.ac.tasks.append(AsyncMock())
        await self.ac._handle_shutdown(self.shutdown_req)

        for task in self.ac.tasks:
            self.assertEqual(task.join.call_count, 1)
        self.assertEqual(self.ac._brain_process.join.call_count, 1)

    @patch(f"{AgentConductor.__module__}.asyncio")
    async def test_housekeeping_setup(self, mock_asyncio):
        mock_transceive_task = AsyncMock()
        mock_transceive_task.result = MagicMock(
            return_value=AgentSetupRequest(
                sender_simulation_controller="sim-1",
                receiver_agent_conductor="ac-1",
                experiment_run_id="run-1",
                experiment_run_instance_id="run-1-instance",
                experiment_run_phase=47,
                agent_id="ag-1",
                sensors=list(),
                actuators=list(),
                configuration=dict(),
                agent_name="agent",
            )
        )

        mock_asyncio.wait = AsyncMock(
            return_value=([mock_transceive_task], list())
        )
        mock_asyncio.create_task = MagicMock(return_value=mock_transceive_task)
        self.ac._worker = MagicMock()

        request = await self.ac._housekeeping(None)

        self.assertIsInstance(request, AgentSetupRequest)
        mock_asyncio.create_task.assert_called_once()
        mock_asyncio.wait.assert_called_once()

    @patch(f"{AgentConductor.__module__}.asyncio")
    async def test_housekeeping_shutdown(self, mock_asyncio):
        mock_transceive_task = AsyncMock()
        mock_transceive_task.result = MagicMock(
            return_value=ShutdownRequest("run-1")
        )
        mock_muscle_task = AsyncMock()
        mock_muscle_task.join = MagicMock()
        mock_muscle_task.exitcode.return_value = 0
        mock_muscle_task.is_alive = MagicMock(return_value=True)
        mock_brain_task = AsyncMock()
        mock_brain_task.join = MagicMock()
        mock_brain_task.exitcode.return_value = 0
        mock_brain_task.is_alive = MagicMock(return_value=True)

        self.ac.tasks.append(mock_muscle_task)
        self.ac._brain_process = mock_brain_task

        mock_asyncio.wait = AsyncMock(
            return_value=([mock_transceive_task], list())
        )
        mock_asyncio.create_task = MagicMock(return_value=mock_transceive_task)
        self.ac._worker = MagicMock()

        request = await self.ac._housekeeping(None)

        self.assertIsInstance(request, ShutdownRequest)
        self.assertEqual(3, mock_asyncio.create_task.call_count)
        mock_asyncio.wait.assert_called_once()

    @patch(f"{AgentConductor.__module__}.asyncio")
    async def test_housekeeping_ungraceful_death(self, mock_asyncio):
        mock_transceive_task = AsyncMock()
        mock_transceive_task.result = MagicMock(
            return_value=ShutdownRequest("run-1")
        )
        mock_muscle_task = AsyncMock()
        mock_muscle_task.join = MagicMock()
        mock_muscle_task.exitcode.return_value = 1
        mock_muscle_task.is_alive = MagicMock(return_value=False)
        mock_brain_task = AsyncMock()
        mock_brain_task.join = MagicMock()
        mock_brain_task.exitcode.return_value = 0
        mock_brain_task.is_alive = MagicMock(return_value=True)

        self.ac.tasks.append(mock_muscle_task)
        self.ac._brain_process = mock_brain_task

        mock_asyncio.wait = AsyncMock(
            return_value=([mock_transceive_task], list())
        )
        mock_asyncio.create_task = MagicMock(return_value=mock_transceive_task)
        self.ac._worker = MagicMock()

        with self.assertRaises(RuntimeError):
            await self.ac._housekeeping(None)

        # self.assertIsInstance(request, ShutdownRequest)
        self.assertEqual(3, mock_asyncio.create_task.call_count)
        mock_asyncio.wait.assert_called_once()

    @patch(f"{AgentConductor.__module__}.asyncio")
    async def test_housekeeping_signal_received(self, mock_asyncio):
        def raise_system_exit():
            raise SystemExit()

        mock_transceive_task = AsyncMock()
        mock_transceive_task.result = MagicMock(
            return_value=ShutdownRequest("run-1")
        )
        mock_muscle_task = AsyncMock()
        mock_muscle_task.join = MagicMock()
        mock_muscle_task.exitcode.return_value = 0
        mock_muscle_task.is_alive = MagicMock(return_value=True)
        mock_brain_task = AsyncMock()
        mock_brain_task.join = MagicMock()
        mock_brain_task.exitcode.return_value = 0
        mock_brain_task.is_alive = MagicMock(return_value=True)

        self.ac.tasks.append(mock_muscle_task)
        self.ac._brain_process = mock_brain_task

        mock_asyncio.wait = AsyncMock(
            side_effect=lambda x, return_when: raise_system_exit()
        )
        mock_asyncio.create_task = MagicMock(return_value=mock_transceive_task)
        self.ac._worker = MagicMock()

        with self.assertRaises(SystemExit):
            await self.ac._housekeeping(None)

        self.assertEqual(3, mock_asyncio.create_task.call_count)
        mock_asyncio.wait.assert_called_once()

    @patch("palaestrai.agent.agent_conductor.aiomultiprocess.Process")
    async def test_run(self, mockaio):
        self.ac._worker = AsyncMock()
        setup_msg = self.setup_req_empty
        shutdown_msg = self.shutdown_req
        self.ac._housekeeping = AsyncMock(
            side_effect=[setup_msg, shutdown_msg, shutdown_msg]
        )

        self.ac._handle_shutdown = AsyncMock()
        await self.ac.run()

        self.assertEqual(2, self.ac._housekeeping.call_count)


if __name__ == "__main__":
    unittest.main()
