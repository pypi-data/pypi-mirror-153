import unittest
from unittest.mock import AsyncMock, MagicMock

from palaestrai.core.protocol import (
    ExperimentRunStartRequest,
    ExperimentRunStartResponse,
)
from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingStarting,
    RGSStartingSetup,
    RGSStartingSimControllers,
)
from palaestrai.util.exception import ExperimentAlreadyRunningError


class TestStartingSetup(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStartingSetup(self.rungov)
        self.rungov.state = self.rgs
        self.request = ExperimentRunStartRequest(
            sender_executor_id="0",
            receiver_run_governor_id="1",
            experiment_run_id="2",
            experiment_run=None,
        )
        # TODO: Add and test the NextPhaseRequest case.

    async def test_run(self):
        self.rgs._is_experiment_run_running = MagicMock(return_value=False)
        self.rgs._experiment_run_start = AsyncMock()
        self.rungov.last_request.append(self.request)

        await self.rgs.run()

        self.rgs._is_experiment_run_running.assert_called_with(self.request)
        self.rgs._experiment_run_start.assert_called_with(self.request)

    async def test_run_experiment_already_running(self):
        self.rgs._is_experiment_run_running = MagicMock(return_value=True)
        self.rgs._experiment_start = AsyncMock()
        self.rungov.last_request.append(self.request)

        await self.rgs.run()

        self.rgs._is_experiment_run_running.assert_called_with(self.request)
        self.rgs._experiment_start.assert_not_called()

    def test_next_state(self):

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStartingSimControllers)

    def test_next_state_with_errors(self):
        self.rgs.add_error(ValueError())

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSErrorHandlingStarting)

    def test_experiment_run_is_not_running(self):
        self.rungov.experiment_run = None

        res = self.rgs._is_experiment_run_running(self.request)

        self.assertFalse(res)
        self.assertEqual(0, len(self.rungov.errors))

    def test_experiment_is_running(self):
        self.rungov.experiment_run = 1

        res = self.rgs._is_experiment_run_running(self.request)

        self.assertTrue(res)
        self.assertEqual(1, len(self.rungov.errors))
        self.assertIsInstance(
            self.rungov.errors[0][0], ExperimentAlreadyRunningError
        )

    async def test_experiment_run_start(self):
        exp = MagicMock()
        self.request.experiment_run = exp

        await self.rgs._experiment_run_start(self.request)

        self.assertEqual(1, len(self.rungov.next_reply))
        self.assertIsInstance(
            self.rungov.next_reply[0], ExperimentRunStartResponse
        )

    async def test_experiment_start_with_error(self):
        exp = MagicMock()
        exp.setup = MagicMock(side_effect=[])
        self.request.experiment_run = exp

        await self.rgs._experiment_run_start(self.request)

        exp.setup.assert_called_once()
        self.assertEqual(1, len(self.rungov.errors))
        self.assertEqual(1, len(self.rungov.next_reply))
        self.assertIsInstance(
            self.rungov.next_reply[0], ExperimentRunStartResponse
        )
        self.assertFalse(self.rungov.next_reply[0].successful)


if __name__ == "__main__":
    unittest.main()
