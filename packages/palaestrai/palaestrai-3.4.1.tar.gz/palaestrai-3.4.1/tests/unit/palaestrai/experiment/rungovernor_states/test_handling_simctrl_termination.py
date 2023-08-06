import asyncio
import unittest
from unittest.mock import MagicMock, AsyncMock

from palaestrai.core.protocol import (
    SimulationControllerTerminationRequest,
    SimulationControllerTerminationResponse,
)
from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSHandlingSimControllerTermination,
    RGSStoppingSimulation,
    RGSTransceiving,
)


class TestHandlingSimControllerTermination(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(
            uid="RunGovernor-0",
            broker_uri="example://none",
        )
        self.rungov.experiment_run_id = "experiment_run-0"
        self.rungov.experiment_run = MagicMock(
            experiment_run_id=self.rungov.experiment_run_id,
            experiment_run_instance_id="experiment_run-0-0",
        )
        self.rgs = RGSHandlingSimControllerTermination(self.rungov)
        self.rungov.state = self.rgs
        self.req = SimulationControllerTerminationRequest(
            sender_simulation_controller_id="SC-0",
            receiver_run_governor_id="RG-0",
            experiment_run_id=self.rungov.experiment_run_id,
            environment_terminated=True,
            additional_results=None,
            last_reward=None,
        )

    async def test_run(self):
        def async_return(result):
            f = asyncio.Future()
            f.set_result(result)
            return f

        self.rungov.last_request.append(self.req)
        self.rgs._handle_termination_request = MagicMock(return_value=False)
        self.rgs._prepare_reply = AsyncMock()
        self.rgs._check_episodes = MagicMock(return_value=False)

        await self.rgs.run()

        self.rgs._handle_termination_request.assert_called_with(
            self.req, False
        )
        self.rgs._prepare_reply.assert_called_with(self.req, False, False)

    def test_next_state(self):
        self.rungov.next_reply.append(
            SimulationControllerTerminationResponse(
                sender_run_governor_id="PseudoRG-0",
                receiver_simulation_controller_id="PseudoSC-0",
                experiment_run_phase=47,
                experiment_run_id="experiment_run-0",
                experiment_run_instance_id="experiment_run-0.0",
                restart=False,
                complete_shutdown=False,
            )
        )
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSTransceiving)

    def test_next_state_complete_shutdown(self):
        self.rungov.next_reply.append(
            SimulationControllerTerminationResponse(
                sender_run_governor_id="PseudoRG-0",
                receiver_simulation_controller_id="PseudoSC-0",
                experiment_run_phase=47,
                experiment_run_id="experiment_run-0",
                experiment_run_instance_id="experiment_run-0.0",
                restart=False,
                complete_shutdown=True,
            )
        )
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStoppingSimulation)

    def test_handle_termination_request(self):
        self.rungov.sim_controllers["sim-1"] = MagicMock()
        self.req.sender_simulation_controller_id = "sim-1"
        self.rungov.termination_condition = MagicMock()
        self.rungov.termination_condition.check_termination = MagicMock(
            return_value=True
        )

        self.rgs._handle_termination_request(self.req, False)

        self.rungov.termination_condition.check_termination.assert_called_with(
            self.req, dict()
        )

    async def test_prepare_reply(self):
        self.req.sender_simulation_controller_id = "sim-1"
        await self.rgs._prepare_reply(self.req, False, False)
        self.assertIsInstance(
            self.rungov.next_reply[0], SimulationControllerTerminationResponse
        )
        self.assertEqual("sim-1", self.rungov.next_reply[0].receiver)

    def test_check_episodes(self):
        self.rungov.experiment_run = MagicMock()
        self.rungov.experiment_run.get_episodes = MagicMock(return_value=2)

        result = self.rgs._check_episodes()

        self.assertTrue(result)

        result = self.rgs._check_episodes()

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
