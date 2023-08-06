import unittest
from unittest.mock import MagicMock, PropertyMock

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSHandlingDeadChildren,
    RGSStoppingSimulation,
    RGSStoppingTransceiving,
)
from palaestrai.util.exception import PrematureTaskDeathError


class TestHandlingDeadChildren(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSHandlingDeadChildren(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        sim = MagicMock()
        sim.is_alive = MagicMock(return_value=True)
        type(sim).exit_code = PropertyMock(return_value=0)
        self.rungov.sim_controllers["sim-1"] = sim

        await self.rgs.run()

        sim.is_alive.assert_called_once()

    async def test_run_alive_false(self):
        sim = MagicMock()
        sim.is_alive = MagicMock(return_value=False)
        type(sim).exit_code = PropertyMock(return_value=0)
        self.rungov.sim_controllers["sim-1"] = sim

        await self.rgs.run()

        self.assertEqual(2, sim.is_alive.call_count)
        self.assertEqual(0, len(self.rungov.sim_controllers))

    async def test_run_non_zero_exitcode(self):
        sim = MagicMock()
        sim.is_alive = MagicMock(return_value=False)
        type(sim).exit_code = PropertyMock(return_value=1)
        self.rungov.sim_controllers["sim-1"] = sim

        await self.rgs.run()

        self.assertEqual(2, sim.is_alive.call_count)
        self.assertEqual(0, len(self.rungov.sim_controllers))
        self.assertIsInstance(
            self.rungov.errors[0][0], PrematureTaskDeathError
        )

    def test_next_state(self):

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStoppingSimulation)

    def test_next_state_with_errors(self):
        self.rgs.add_error(ValueError())

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStoppingTransceiving)


if __name__ == "__main__":
    unittest.main()
