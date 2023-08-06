from typing import TYPE_CHECKING

from palaestrai.util.exception import (
    DeadChildrenRisingAsZombiesError,
    InvalidRequestError,
    RequestIsNoneError,
    SignalInterruptError,
    TasksNotFinishedError,
)

from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSErrorHandlingTransceiving(RunGovernorState):
    """Represent the ERROR_HANDLING_TRANSCEIVING state of the run
    governor.

    Expected errors:
    * InvalidRequestError
    * TasksNotFinishedError
    * SignalInterruptError
    * DeadChildrenRisingAsZombiesError
    * RequestIsNoneError

     Possible next states are
    * :class:`.RGSTransceiving` in the InvalidRequestError, TasksNotFinishedError, RequestIsNoneError case.
    * :class:`.RGSStoppingSimulation` in the SignalInterruptError case.
    * :class:`.RGSHandlingDeadChildren` in the DeadChildrenRisingAsZombiesError case.

    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "ERROR_HANDLING_TRANSCEIVING")

    async def run(self):
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) encountered errors during "
            "transceiving. Handling these errors now.",
            id(self.rgc),
            self.rgc.uid,
        )
        for (error, state) in self.rgc.errors:
            LOG.debug(
                "RunGovernor(id=0x%x, uid=%s) encountered %s during "
                "state %s",
                id(self.rgc),
                self.rgc.uid,
                error.__class__,
                state,
            )

        assert len(self.rgc.errors) == 1

    def next_state(self):
        from . import (
            RGSHandlingDeadChildren,
            RGSStoppingSimulation,
            RGSTransceiving,
        )

        dispatcher = {
            InvalidRequestError: RGSTransceiving,
            TasksNotFinishedError: RGSTransceiving,
            SignalInterruptError: RGSStoppingSimulation,
            DeadChildrenRisingAsZombiesError: RGSHandlingDeadChildren,
            RequestIsNoneError: RGSTransceiving,
        }

        self.rgc.state = dispatcher[self.rgc.errors[0][0].__class__](self.rgc)
        self.rgc.errors = list()
