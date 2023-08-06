import unittest
from unittest.mock import AsyncMock

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSStoppingTransceiving,
    RGSStoppingRun,
)


class TestStoppingTransceiving(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStoppingTransceiving(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        self.rungov.major_domo_worker = AsyncMock()
        self.rungov.major_domo_worker.transceive = AsyncMock()

        await self.rgs.run()

        self.rungov.major_domo_worker.transceive.assert_called_once_with(
            None, skip_recv=True
        )

    def test_next_state(self):
        self.rgs.next_state()
        self.assertIsInstance(self.rungov.state, RGSStoppingRun)


if __name__ == "__main__":
    unittest.main()
