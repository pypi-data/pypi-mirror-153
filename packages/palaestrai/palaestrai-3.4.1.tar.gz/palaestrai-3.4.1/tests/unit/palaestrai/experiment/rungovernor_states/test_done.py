import unittest

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import RGSDone


class TestDone(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSDone(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):

        await self.rgs.run()

        self.assertTrue(self.rungov.shutdown)
        self.assertEqual(0, len(self.rungov.errors))

    def test_next_state(self):

        # Nothing to test here
        self.rgs.next_state()


if __name__ == "__main__":
    unittest.main()
