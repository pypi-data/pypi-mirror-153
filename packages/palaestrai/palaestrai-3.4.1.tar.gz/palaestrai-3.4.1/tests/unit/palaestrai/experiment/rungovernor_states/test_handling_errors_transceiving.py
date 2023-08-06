import unittest
from unittest.mock import MagicMock

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingTransceiving,
    RGSHandlingDeadChildren,
    RGSStoppingSimulation,
    RGSTransceiving,
)
from palaestrai.util.exception import (
    DeadChildrenRisingAsZombiesError,
    InvalidRequestError,
    RequestIsNoneError,
    SignalInterruptError,
    TasksNotFinishedError,
)


class TestHandlingErrorsStarting(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSErrorHandlingTransceiving(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        logger = f"{RunGovernor.__module__}".rsplit(".", 1)[0]

        self.rgs.add_error(TasksNotFinishedError())

        with self.assertLogs(logger, level="DEBUG") as cm:
            await self.rgs.run()

        self.assertIn("Handling these errors now.", cm.output[0])

    def test_next_state_invalid_request(self):

        self.rgs.add_error(InvalidRequestError(MagicMock(), MagicMock()))
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSTransceiving)

    def test_next_state_task_not_finished(self):

        self.rgs.add_error(TasksNotFinishedError())
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSTransceiving)

    def test_next_state_signal_interrupt_error(self):
        self.rgs.add_error(SignalInterruptError())
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStoppingSimulation)

    def test_next_state_dead_children(self):

        self.rgs.add_error(DeadChildrenRisingAsZombiesError())
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSHandlingDeadChildren)

    def test_next_state_request_is_none(self):

        self.rgs.add_error(RequestIsNoneError())
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSTransceiving)
