from typing import TYPE_CHECKING

from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSErrorHandlingInitializing(RunGovernorState):
    """Represent the ERROR_HANDLING_INITIALIZING state of the run
    governor.

    This state handles errors that occur during initialization.
    Currently, no errors are expected in the initialization process,
    which makes this class kind of useless. But since this may change,
    we keep the state in existence.

    Possible next states are
    * :class:`.RGSStoppingTransceiving` in the normal case.
    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "ERROR_HANDLING_INITIALIZING")

    async def run(self):
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) encountered errors during "
            "initializing. Handling these errors now.",
            id(self.rgc),
            self.rgc.uid,
        )

    def next_state(self):
        from . import RGSStoppingTransceiving

        self.rgc.state = RGSStoppingTransceiving(self.rgc)
        self.rgc.errors = list()
