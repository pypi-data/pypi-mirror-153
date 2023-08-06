import unittest
from unittest.mock import MagicMock, PropertyMock, patch

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingStarting,
    RGSStartingEnvConductors,
    RGSStartingSimControllers,
)


class TestStartingSimControllers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStartingSimControllers(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        self.rgs._init_sim_controllers = MagicMock()

        await self.rgs.run()

        self.rgs._init_sim_controllers.assert_called_once()

    @patch(f"{RGSStartingSimControllers.__module__}.aiomultiprocess.Process")
    def test_init_sim_controllers(self, mock_amp):
        sc = MagicMock()
        type(sc).uid = PropertyMock(return_value="sim-1")

        self.rungov.experiment_run = MagicMock()
        sim_ctrls = MagicMock()
        sim_ctrls.values = MagicMock(return_value=[sc])
        self.rungov.experiment_run.simulation_controllers = MagicMock(
            return_value=sim_ctrls
        )

        self.rgs._init_sim_controllers()

        self.assertEqual(len(self.rungov.sim_controllers), 1)
        self.assertIn("sim-1", self.rungov.sim_controllers)

    def test_next_state(self):

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStartingEnvConductors)

    def test_next_state_with_errors(self):
        self.rgs.add_error(ValueError())

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSErrorHandlingStarting)


if __name__ == "__main__":
    unittest.main()
