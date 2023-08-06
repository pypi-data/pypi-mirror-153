import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from palaestrai.core import MajorDomoClient, MajorDomoWorker
from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingInitializing,
    RGSInitializing,
    RGSTransceiving,
)


class TestInitializing(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSInitializing(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        self.rgs._init_signal_handler = MagicMock()
        self.rgs._init_signal_monitor = MagicMock()
        self.rgs._init_communication = MagicMock()

        await self.rgs.run()

        self.rgs._init_signal_handler.assert_called_once()
        self.rgs._init_signal_monitor.assert_called_once()
        self.rgs._init_communication.assert_called_once()

    def test_next_state_success(self):

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSTransceiving)

    def test_next_state_failure(self):

        self.rgs.add_error(ValueError())
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSErrorHandlingInitializing)

    @patch(f"{RGSInitializing.__module__}.asyncio")
    def test_init_signal_handler(self, mock_asyncio):
        mock_loop = MagicMock()
        mock_loop.add_signal_handler = MagicMock()
        mock_asyncio.get_running_loop = MagicMock(return_value=mock_loop)

        self.rgs._init_signal_handler()

        self.assertEqual(3, mock_loop.add_signal_handler.call_count)

    def test_handle_signal_termination(self):
        signum = 0

        logger = f"{RunGovernor.__module__}".rsplit(".", 1)[0]

        with self.assertLogs(logger, level="INFO") as cm:
            self.rgs._handle_signal_termination(signum)

        self.assertEqual(signum, self.rungov.signal_received)
        self.assertIn("interrupted", cm.output[0])

    def test_handle_signal_interrupt(self):
        logger = f"{RunGovernor.__module__}".rsplit(".", 1)[0]

        with self.assertLogs(logger, level="DEBUG") as cm:
            self.rgs._handle_signal_interrupt()

        self.assertIn("SIGINT", cm.output[0])

    @patch(f"{RGSInitializing.__module__}.asyncio")
    def test_init_signal_monitor(self, mock_asyncio):
        mock_create = MagicMock(return_value=0)
        mock_asyncio.create_task = mock_create
        self.rgs._monitor_signal = MagicMock()

        self.rgs._init_signal_monitor()

        mock_create.assert_called_once()
        self.rgs._monitor_signal.assert_called_once()

    @patch(f"{RGSInitializing.__module__}.asyncio")
    async def test_monitor_signal(self, mock_asyncio):
        self.rungov.signal_received = 0

        mock_asyncio.sleep = AsyncMock()
        logger = f"{RunGovernor.__module__}".rsplit(".", 1)[0]
        with self.assertLogs(logger, level="DEBUG") as cm:
            await self.rgs._monitor_signal()

        self.assertIn("received signal", cm.output[0])
        self.assertIsNone(self.rungov.signal_received)

    def test_init_communication(self):

        self.rgs._init_communication()
        self.assertIsInstance(self.rungov.major_domo_worker, MajorDomoWorker)
        self.assertIsInstance(self.rungov.major_domo_client, MajorDomoClient)


if __name__ == "__main__":
    unittest.main()
