import unittest
from unittest.mock import MagicMock

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingStarting,
    RGSStoppingSimulation,
    RGSStoppingTransceiving,
    RGSTransceiving,
)
from palaestrai.util.exception import (
    AgentConductorFailedError,
    EnvConductorFailedError,
    ExperimentAlreadyRunningError,
    ExperimentSetupFailedError,
    InvalidResponseError,
    SimControllerFailedError,
)


class TestHandlingErrorsStarting(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSErrorHandlingStarting(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        logger = f"{RunGovernor.__module__}".rsplit(".", 1)[0]

        self.rgs.add_error(ExperimentAlreadyRunningError())

        with self.assertLogs(logger, level="DEBUG") as cm:
            await self.rgs.run()

        self.assertIn("Handling these errors now.", cm.output[0])

    def test_next_state_running_experiment(self):

        self.rgs.add_error(ExperimentAlreadyRunningError())
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSTransceiving)

    def test_next_state_failed_setup_experiment(self):

        self.rgs.add_error(ExperimentSetupFailedError())
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStoppingTransceiving)

    def test_next_state_simcontroller_failed(self):
        self.rgs.add_error(SimControllerFailedError())
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStoppingSimulation)

    def test_next_state_env_conductor_failed(self):
        self.rgs.add_error(EnvConductorFailedError())
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStoppingSimulation)

    def test_next_state_invalid_response_error(self):
        self.rgs.add_error(
            InvalidResponseError(expected=MagicMock(), got=MagicMock())
        )
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStoppingSimulation)

    def test_next_state_agent_conductor_failed(self):
        self.rgs.add_error(AgentConductorFailedError())
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStoppingSimulation)
