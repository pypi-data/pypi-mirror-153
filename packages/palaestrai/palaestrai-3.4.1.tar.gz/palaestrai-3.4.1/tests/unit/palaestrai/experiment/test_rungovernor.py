import unittest

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import RunGovernorState


class DummyState(RunGovernorState):
    def __init__(self, rgc, called=0):
        super().__init__(rgc, "TEST")
        self.called = called

    async def run(self):
        self.called += 1

        if self.called >= 3:
            self.rgc.shutdown = True

    def next_state(self):
        if self.called == 2:
            self.rgc.state = DummyState(self.rgc, self.called)


class TestRunGovernor(unittest.IsolatedAsyncioTestCase):
    async def test_run_state_change(self):
        """Test the run method.
        A test state is created, which transitions to another test
        state after being called two times.

        """
        rungov = RunGovernor("test_broker_uri", None)
        test_state = DummyState(rungov)
        rungov.state = test_state

        await rungov.run()

        self.assertEqual(2, test_state.called)
        self.assertEqual(3, rungov.state.called)


if __name__ == "__main__":
    unittest.main()
