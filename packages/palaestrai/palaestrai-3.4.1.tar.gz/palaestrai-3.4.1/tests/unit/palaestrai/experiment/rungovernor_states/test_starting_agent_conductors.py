import unittest
from unittest.mock import MagicMock, PropertyMock, patch

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingStarting,
    RGSStartingAgentConductors,
    RGSStartingRun,
)


class TestStartingSimControllers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStartingAgentConductors(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        self.rgs._init_agent_conductors = MagicMock()

        await self.rgs.run()

        self.rgs._init_agent_conductors.assert_called_once()

    @patch(f"{RGSStartingAgentConductors.__module__}.aiomultiprocess.Process")
    def test_init_agent_conductors(self, mock_amp):
        ac = MagicMock()
        type(ac).uid = PropertyMock(return_value="ac-1")

        agent_cond = MagicMock()
        agent_cond.values = MagicMock(return_value=[ac])
        self.rungov.experiment_run = MagicMock()
        self.rungov.experiment_run.agent_conductors = MagicMock(
            return_value=agent_cond
        )

        self.rgs._init_agent_conductors()

        self.assertEqual(len(self.rungov.agent_conductors), 1)
        self.assertIn("ac-1", self.rungov.agent_conductors)

    def test_next_state(self):

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStartingRun)

    def test_next_state_with_errors(self):
        self.rgs.add_error(ValueError())

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSErrorHandlingStarting)


if __name__ == "__main__":
    unittest.main()
