from typing import TYPE_CHECKING

from . import RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSDone(RunGovernorState):
    """Represent the DONE state of the run governor.

    There are no possible next states. The run governor terminates
    after setting shutdown to true.

    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "DONE")

    async def run(self):
        self.rgc.shutdown = True
        self.rgc.errors = list()

    def next_state(self):
        pass
