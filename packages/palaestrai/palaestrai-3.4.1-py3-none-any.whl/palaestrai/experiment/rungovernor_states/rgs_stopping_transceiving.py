from typing import TYPE_CHECKING

from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSStoppingTransceiving(RunGovernorState):
    """Represents the STOPPING_TRANSCEIVING state.

    Possible next states are
    * :class:`.RGSStoppingRun in the normal case.

    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "STOPPING_TRANSCEIVING")

    async def run(self):
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) about to shut down worker.",
            id(self.rgc),
            self.rgc.uid,
        )
        try:
            msg = self.rgc.next_reply.pop()
        except IndexError:
            msg = None

        _ = await self.rgc.major_domo_worker.transceive(msg, skip_recv=True)

    def next_state(self):
        from . import RGSStoppingRun

        self.rgc.state = RGSStoppingRun(self.rgc)
