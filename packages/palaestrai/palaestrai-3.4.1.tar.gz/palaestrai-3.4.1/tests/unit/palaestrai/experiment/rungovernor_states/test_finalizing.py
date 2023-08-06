import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSFinalizing,
    RGSDone,
)


class TestStoppingRun(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSFinalizing(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        self.rgs._shutdown_tasks = AsyncMock()
        # self.rungov.major_domo_worker.transceive = AsyncMock()

        logger = f"{RunGovernor.__module__}".rsplit(".", 1)[0]
        with self.assertLogs(logger, level="DEBUG") as cm:
            await self.rgs.run()

        self.rgs._shutdown_tasks.assert_called_once()
        self.assertIn("completed shutdown", cm.output[0])

    def test_next_state(self):
        self.rgs.next_state()
        self.assertIsInstance(self.rungov.state, RGSDone)

    @patch(f"{RGSFinalizing.__module__}.os")
    async def test_shutdown_tasks(self, mock_os):
        self.rungov.sim_controllers["sim-1"] = 0
        mock_os.killpg = MagicMock()
        RGSFinalizing._reap_process = AsyncMock()
        await self.rgs._shutdown_tasks()

        mock_os.killpg.assert_called_once()
        RGSFinalizing._reap_process.assert_called_once()

    async def test_reap_process(self):
        def raise_timeout():
            raise asyncio.TimeoutError()

        proc = MagicMock()
        proc.is_alive = MagicMock(side_effect=[True, True])
        proc.terminate = MagicMock()
        proc.kill = MagicMock()
        proc.join = AsyncMock(side_effect=lambda timeout: raise_timeout())

        await self.rgs._reap_process(proc)

        proc.terminate.assert_called_once()
        proc.join.assert_called_once()
        proc.kill.assert_called_once()
        self.assertEqual(2, proc.is_alive.call_count)


if __name__ == "__main__":
    unittest.main()
