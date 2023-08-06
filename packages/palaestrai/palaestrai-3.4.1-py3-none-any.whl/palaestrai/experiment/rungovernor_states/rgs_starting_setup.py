import io
import traceback
from typing import TYPE_CHECKING, Union

from palaestrai.core.protocol import (
    ExperimentRunStartRequest,
    ExperimentRunStartResponse,
    NextPhaseRequest,
    NextPhaseResponse,
)

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor

from palaestrai.util.exception import (
    ExperimentAlreadyRunningError,
    ExperimentSetupFailedError,
    InvalidRequestError,
)

from . import LOG, RunGovernorState


class RGSStartingSetup(RunGovernorState):
    """Represent the STARTING_RUN_SETUP state of the run governor.

    This state is entered if an ExperimentStartRequest was received in
    the TRANSCEIVING state or after on run phase to initiate the next
    phase. During this state, the ExperimentStartRequest is checked
    against a possibly already running experiment. If no experiment is
    running, the setup of the experiment is executed.

    In any case, an ExperimentStartResponse is prepared and stored as
    next_reply in the run governor.

    Possible next states are
    * :class:`.RGSStartinSimControllers in the normal case.
    * :class:`.RGSErrorHandlingStarting in the error case.

    Parameters
    ----------
    rgc: :class:`.RunGovernor`
        The run governor instance that provides the context for this
        state.

    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "STARTING_RUN_SETUP")

    async def run(self):

        try:
            request = self.rgc.last_request[0]
        except IndexError:
            # Is raised on signal interrupt because the last request
            # is none.
            return

        if isinstance(request, ExperimentRunStartRequest):
            if self._is_experiment_run_running(request):
                return

        await self._experiment_run_start(request)

    def next_state(self):
        from . import RGSErrorHandlingStarting, RGSStartingSimControllers

        if len(self.rgc.errors) > 0:
            self.rgc.state = RGSErrorHandlingStarting(self.rgc)
        else:
            self.rgc.state = RGSStartingSimControllers(self.rgc)

    def _is_experiment_run_running(
        self, request: ExperimentRunStartRequest
    ) -> bool:
        """Check if an experiment run is already being executed.

        Adds an ExperimentAlreadyRunningError to the run governor error
        stack if an experiment run is already being executed.

        Returns
        -------
        bool
            True, if an experiment run is already being executed,
            False otherwise.

        """
        if self.rgc.experiment_run is not None:
            LOG.warning(
                "RunGovernor(id=0x%x, uid=%s) received request to start "
                "ExperimentRun(run_id=%s), but this is recorded as already "
                "running.",
                id(self.rgc),
                self.rgc.uid,
                request.experiment_run_id,
            )
            self.rgc.next_reply.append(
                ExperimentRunStartResponse(
                    sender_run_governor_id=self.rgc.uid,
                    receiver_executor_id=request.sender,
                    experiment_run_id=str(self.rgc.experiment_run_id),
                    successful=False,
                    error=ExperimentAlreadyRunningError(
                        "Experiment is already active."
                    ),
                    experiment_run=self.rgc.experiment_run,
                )
            )
            self.add_error(ExperimentAlreadyRunningError())
            return True
        return False

    async def _experiment_run_start(
        self, request: Union[ExperimentRunStartRequest, NextPhaseRequest]
    ):
        """Start an experiment run.

        This function starts the experiment run by receiving an
        ExperimentRunStartRequest. Adds an ExperimentSetupFailedError
        if an error occured during setup(). If the request is of
        type NextPhaseRequest, the phase counter is increased and
        some cleanup is performed.

        Parameters
        ----------
        request: Union[ExperimentStartRequest, NextPhaseRequest]
            The instance of the start request with information about
            the experiment run to start or the information about
            the next phase.

        """
        successful = True
        msg: Union[Exception, None] = None
        if isinstance(request, ExperimentRunStartRequest):
            self.rgc.experiment_run = request.experiment_run
            self.rgc.experiment_run_id = request.experiment_run_id
            try:
                self.rgc.experiment_run.setup(self.rgc.broker_uri)
            except Exception as e:
                tb = io.StringIO()
                traceback.print_exc(file=tb)
                self.add_error(ExperimentSetupFailedError(tb.getvalue()))
                msg = e
                successful = False

            self.rgc.termination_condition = (
                self.rgc.experiment_run.run_governor_termination_condition
            )

            self.rgc.next_reply.append(
                ExperimentRunStartResponse(
                    sender_run_governor_id=self.rgc.uid,
                    receiver_executor_id=request.sender,
                    experiment_run_id=self.rgc.experiment_run_id,
                    successful=successful,
                    error=msg,
                    experiment_run=self.rgc.experiment_run,
                )
            )
        elif isinstance(request, NextPhaseRequest):
            LOG.info(
                "RunGovernor(id=0x%x, uid=%s) initializing next phase %d",
                id(self.rgc),
                self.rgc.uid,
                request.next_phase,
            )
            self.rgc.current_phase = request.next_phase
            self.rgc.sim_controllers = dict()
            self.rgc.agent_conductors = dict()
            self.rgc.env_conductors = dict()
            self.rgc.current_episode = 0
            if len(self.rgc.next_reply) == 0:
                self.rgc.next_reply.append(
                    NextPhaseResponse(
                        sender_run_governor_id=self.rgc.uid,
                        receiver_run_governor_id=self.rgc.uid,
                        has_next_phase=True,
                    )
                )

        else:
            # That case shouldn't be able to occur. But you never know ...
            LOG.error(
                "RunGovernor(id=0x%x, uid=%s) got invalid request "
                "during experiment run setup: %s.",
                id(self.rgc),
                self.rgc.uid,
                request,
            )
            self.rgc.add_error(
                InvalidRequestError(
                    [ExperimentRunStartRequest, NextPhaseRequest], request
                )
            )
