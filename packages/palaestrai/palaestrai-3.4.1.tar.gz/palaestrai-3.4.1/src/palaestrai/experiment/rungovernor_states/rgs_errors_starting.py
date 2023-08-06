from typing import TYPE_CHECKING

from palaestrai.util.exception import (
    AgentConductorFailedError,
    EnvConductorFailedError,
    ExperimentAlreadyRunningError,
    ExperimentSetupFailedError,
    InvalidResponseError,
    SimControllerFailedError,
)

from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSErrorHandlingStarting(RunGovernorState):
    """Represent the ERROR_HANDLING_STARTING state of the run
    governor.

    Expected errors:
    * ExperimentAlreadyRunningError during STARTING_EXPERIMENT
    * ExperimentSetupFailedError during STARTING_EXPERIMENT
    * SimControllerFailedError during STARTING_SIM_CONTROLLERS (?)
    * EnvConductorFailedError during STARTING_ENV_CONDUCTORS (?)
    * AgentConductorFailedError during STARTING_AGENT_CONDUCTORS (?)
    * InvalidResponseError during STARTING_RUN

    Possible next states are
    * :class:`.RGSTransceiving` in the ExperimentAlreadyRunningError
    case.
    * :class:`.RGSStoppingTransceiving` in the
    ExperimentSetupFailedError case.
    * :class:`.RGSStoppingSimulation`  in the cases
    SimControllerFailedError, EnvConductorFailedError,
    AgentConductorFailedError, InvalidResponseError.

    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "ERROR_HANDLING_STARTING")

    async def run(self):
        LOG.info(
            "RunGovernor(id=0x%x, uid=%s) encountered errors during "
            "experiment starting. Handling these errors now.",
            id(self.rgc),
            self.rgc.uid,
        )
        for (error, state) in self.rgc.errors:
            LOG.info(
                "RunGovernor(id=0x%x, uid=%s) encountered %s during "
                "state %s",
                id(self.rgc),
                self.rgc.uid,
                error.__class__,
                state,
            )
            LOG.debug(
                "RunGovernor(id=0x%x, uid=%s) message of the error: %s",
                id(self.rgc),
                self.rgc.uid,
                error,
            )

        assert len(self.rgc.errors) == 1

    def next_state(self):
        from . import (
            RGSStoppingSimulation,
            RGSStoppingTransceiving,
            RGSTransceiving,
        )

        dispatcher = {
            ExperimentAlreadyRunningError: RGSTransceiving,
            ExperimentSetupFailedError: RGSStoppingTransceiving,
            SimControllerFailedError: RGSStoppingSimulation,
            EnvConductorFailedError: RGSStoppingSimulation,
            AgentConductorFailedError: RGSStoppingSimulation,
            InvalidResponseError: RGSStoppingSimulation,
        }

        self.rgc.state = dispatcher[self.rgc.errors[0][0].__class__](self.rgc)
        self.rgc.errors = list()
