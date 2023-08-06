import unittest

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingInitializing,
    RGSStoppingTransceiving,
)


class TestHandlingErrorsInitializing(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSErrorHandlingInitializing(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        logger = f"{RunGovernor.__module__}".rsplit(".", 1)[0]

        with self.assertLogs(logger, level="DEBUG") as cm:
            await self.rgs.run()

        self.assertIn("Handling these errors now.", cm.output[0])

    def test_next_state_success(self):

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStoppingTransceiving)
