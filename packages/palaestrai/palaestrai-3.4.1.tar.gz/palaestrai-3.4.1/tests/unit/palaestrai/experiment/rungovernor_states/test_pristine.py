import unittest
from unittest.mock import patch, MagicMock

from palaestrai.experiment import RunGovernor

from palaestrai.experiment.rungovernor_states import (
    RGSPristine,
    RGSInitializing,
)


class TestPristine(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)

    @patch(f"{RGSPristine.__module__}.os")
    async def test_run(self, mock_os):
        rgs = RGSPristine(self.rungov)
        mock_os.setpgrp = MagicMock()
        mock_os.getpgid = MagicMock()
        mock_os.getpid = MagicMock()

        await rgs.run()

        mock_os.setpgrp.assert_called_once()
        mock_os.getpgid.assert_called_once()
        mock_os.getpid.assert_called_once()

    def test_next_state(self):
        rgs = RGSPristine(self.rungov)

        rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSInitializing)


if __name__ == "__main__":
    unittest.main()
