import unittest
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSFinalizing,
    RGSStoppingRun,
)


class TestStoppingRun(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStoppingRun(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        self.rgs._stop_processes = AsyncMock()
        # self.rungov.major_domo_worker.transceive = AsyncMock()

        await self.rgs.run()

        self.rgs._stop_processes.assert_called_once()

    def test_next_state(self):
        self.rungov.experiment_run = MagicMock()
        self.rungov.experiment_run.has_next_phase = MagicMock(
            return_value=False
        )
        self.rgs.next_state()
        self.assertIsInstance(self.rungov.state, RGSFinalizing)

    @patch(f"{RGSStoppingRun.__module__}.asyncio.wait")
    @patch(f"{RGSStoppingRun.__module__}.asyncio.create_task")
    async def test_stop_processes(self, mock_wait, mock_create):
        self.rgs._join_process = MagicMock()
        self.rungov.sim_controllers["sim-1"] = 0
        await self.rgs._stop_processes()

        mock_wait.assert_called_once()
        mock_create.assert_called_once()
        self.rgs._join_process.assert_called_once()

    @patch(f"{RGSStoppingRun.__module__}.asyncio")
    async def test_join_process(self, mock_asyncio):
        proc = MagicMock()
        proc.name.return_value = "proc-1"
        proc.is_alive = MagicMock(return_value=True)
        type(proc).exitcode = PropertyMock(side_effect=[None, 1, 1, 1])
        mock_asyncio.sleep = AsyncMock()

        await self.rgs._join_process(proc)

        mock_asyncio.sleep.assert_called_once()
        self.assertEqual(2, proc.is_alive.call_count)


if __name__ == "__main__":
    unittest.main()
