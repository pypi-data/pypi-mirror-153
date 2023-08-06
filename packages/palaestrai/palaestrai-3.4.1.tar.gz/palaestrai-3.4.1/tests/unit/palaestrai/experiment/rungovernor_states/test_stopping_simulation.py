import unittest
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

from palaestrai.core.protocol import (
    ExperimentRunShutdownRequest,
    ExperimentRunShutdownResponse,
    NextPhaseRequest,
    NextPhaseResponse,
    SimulationStopResponse,
)
from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSStoppingSimulation,
    RGSStoppingTransceiving,
)


class TestStoppingSimulation(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStoppingSimulation(self.rungov)
        self.rungov.state = self.rgs

    @patch(f"{RGSStoppingSimulation.__module__}.asyncio.wait_for")
    async def test_run(self, mock_wait):
        # self.rgs._is_experiment_running = MagicMock(return_value=False)
        # self.rgs._experiment_start = AsyncMock()
        # request = ExperimentStartRequest(None, None)
        self.rgs._prepare_reply = MagicMock()
        self.rgs._terminate_sim_controllers = MagicMock()

        # self.rungov.last_request.append(request)

        await self.rgs.run()

        self.rgs._prepare_reply.assert_called_once()
        self.rgs._terminate_sim_controllers.assert_called_once()

    def test_next_state(self):
        self.rungov.experiment_run = MagicMock()
        self.rungov.experiment_run.has_next_phase = MagicMock(
            return_value=False
        )
        self.rgs.next_state()
        self.assertIsInstance(self.rungov.state, RGSStoppingTransceiving)

    async def test_terminate_sim_controllers(self):
        self.rungov.experiment_run = MagicMock()
        type(self.rungov.experiment_run).uid = PropertyMock(return_value="uid")
        self.rungov.major_domo_client = MagicMock()
        self.rungov.major_domo_client.send = AsyncMock(
            return_value=SimulationStopResponse("run-1")
        )
        proc = MagicMock()
        proc.terminate = MagicMock()

        self.rungov.sim_controllers["sim-1"] = proc
        sc_terminated = await self.rgs._terminate_sim_controllers()

        proc.terminate.assert_not_called()
        self.assertEqual(0, len(sc_terminated))

    async def test_terminate_sim_controllers_no_response(self):
        self.rungov.experiment_run = MagicMock()
        type(self.rungov.experiment_run).uid = PropertyMock(return_value="uid")

        self.rungov.major_domo_client = MagicMock()
        self.rungov.major_domo_client.send = AsyncMock(return_value=None)
        proc = MagicMock()
        proc.terminate = MagicMock()

        self.rungov.sim_controllers["sim-1"] = proc
        sc_terminated = await self.rgs._terminate_sim_controllers()

        proc.terminate.assert_called_once()
        self.assertEqual(1, len(sc_terminated))

    def test_prepare_reply_shutdown(self):
        self.assertEqual(0, len(self.rungov.next_reply))
        self.rungov.last_request.append(
            ExperimentRunShutdownRequest(
                sender_executor_id="0",
                receiver_run_governor_id="1",
                experiment_run_id="2",
            )
        )
        self.rgs._prepare_reply(list())

        self.assertEqual(1, len(self.rungov.next_reply))
        self.assertIsInstance(
            self.rungov.next_reply[0], ExperimentRunShutdownResponse
        )

    def test_prepare_reply_next_phase(self):
        self.assertEqual(0, len(self.rungov.next_reply))
        self.rungov.last_request.append(
            NextPhaseRequest(
                sender_run_governor_id="1",
                receiver_run_governor_id="1",
                next_phase=1,
            )
        )
        self.rgs._prepare_reply(list())

        self.assertEqual(1, len(self.rungov.next_reply))
        self.assertIsInstance(self.rungov.next_reply[0], NextPhaseResponse)


if __name__ == "__main__":
    unittest.main()
