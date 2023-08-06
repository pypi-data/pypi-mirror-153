import unittest
from unittest.mock import MagicMock, PropertyMock, patch

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingStarting,
    RGSStartingAgentConductors,
    RGSStartingEnvConductors,
)


class TestStartingSimControllers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStartingEnvConductors(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        self.rgs._init_environment_conductors = MagicMock()

        await self.rgs.run()

        self.rgs._init_environment_conductors.assert_called_once()

    @patch(f"{RGSStartingEnvConductors.__module__}.aiomultiprocess.Process")
    def test_init_env_conductors(self, mock_amp):
        ec = MagicMock()
        type(ec).uid = PropertyMock(return_value="ec-1")

        env_cond = MagicMock()
        env_cond.values = MagicMock(return_value=[ec])
        self.rungov.experiment_run = MagicMock()
        self.rungov.experiment_run.environment_conductors = MagicMock(
            return_value=env_cond
        )

        self.rgs._init_environment_conductors()

        self.assertEqual(len(self.rungov.env_conductors), 1)
        self.assertIn("ec-1", self.rungov.env_conductors)

    def test_next_state(self):

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStartingAgentConductors)

    def test_next_state_with_errors(self):
        self.rgs.add_error(ValueError())

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSErrorHandlingStarting)


if __name__ == "__main__":
    unittest.main()
