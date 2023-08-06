from typing import TYPE_CHECKING

from palaestrai.core.protocol import (
    NextPhaseRequest,
    SimulationControllerTerminationRequest,
    SimulationControllerTerminationResponse,
)
from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor, ExperimentRun


class RGSHandlingSimControllerTermination(RunGovernorState):
    """Represents the HANDLING_SIM_CONTROLLER_TERMINATION state.

    This state is entered either after the run governor received a
    SimControllerTerminationRequest during the EXPERIMENT_RUNNING
    state.


    Possible next states are:
    * :class:`.RGSStoppingTransceiving` in the case of a complete shutdown.
    * :class:`.RGSTransceiving` in the default case.

    Parameters
    ----------
    ctx: :class:`.RunGovernor`
        The run governor instance that provides the context for this
        state.
    request: :class:`.SimControllerTerminationRequest`
        The sim controller termination request that leads to this
        state.

    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "HANDLING_SIM_CONTROLLER_TERMINATION")

    async def run(self):
        request = self.rgc.last_request.pop()
        restart = self._check_episodes()
        is_terminal = self._handle_termination_request(request, restart)

        await self._prepare_reply(request, is_terminal, restart)

    def next_state(self):
        from . import RGSStoppingSimulation, RGSTransceiving

        reply = self.rgc.next_reply[0]

        if isinstance(reply, SimulationControllerTerminationResponse):
            if self.rgc.next_reply[0].complete_shutdown:
                self.rgc.next_reply.pop()
                self.rgc.state = RGSStoppingSimulation(self.rgc)
            else:
                self.rgc.state = RGSTransceiving(self.rgc)
        else:
            self.rgc.next_reply.pop()
            self.rgc.state = RGSStoppingSimulation(self.rgc)

    def _check_episodes(self):

        self.rgc.current_episode += 1
        episodes = self.rgc.experiment_run.get_episodes(self.rgc.current_phase)
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) checking episodes: %d/%d.",
            id(self.rgc),
            self.rgc.uid,
            self.rgc.current_episode,
            episodes,
        )
        return self.rgc.current_episode < episodes

    def _handle_termination_request(
        self, request: SimulationControllerTerminationRequest, restart: bool
    ) -> bool:
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) handling "
            "SimulationControllerTerminationRequest: %s.",
            id(self.rgc),
            self.rgc.uid,
            request,
        )

        active_sim_controllers = self.rgc.sim_controllers.copy()
        if not restart:
            del active_sim_controllers[request.sender]

        return self.rgc.termination_condition.check_termination(
            request, active_sim_controllers
        )

    async def _prepare_reply(
        self,
        request: SimulationControllerTerminationRequest,
        is_terminal: bool,
        restart: bool,
    ):
        assert self.rgc.experiment_run is not None
        assert self.rgc.experiment_run_id is not None
        self.rgc.next_reply.append(
            SimulationControllerTerminationResponse(
                sender_run_governor_id=self.rgc.uid,
                receiver_simulation_controller_id=request.sender,
                experiment_run_id=self.rgc.experiment_run_id,
                experiment_run_instance_id=self.rgc.experiment_run.instance_uid,
                experiment_run_phase=self.rgc.current_phase,
                restart=restart,
                complete_shutdown=is_terminal,
            )
        )
        if is_terminal:
            # All simulation controllers finished
            if self.rgc.experiment_run is None:
                # Should NEVER happen, but mypy goes enrage otherwise
                return

            run: ExperimentRun = self.rgc.experiment_run

            next_phase = self.rgc.current_phase + 1
            if run.has_next_phase(self.rgc.current_phase):
                LOG.info(
                    "RunGovernor(id=0x%x, uid=%s) finished phase %d/%d. "
                    "Shutting down current phase and continue with the "
                    "next phase.",
                    id(self.rgc),
                    self.rgc.uid,
                    next_phase,
                    run.num_phases,
                )
                self.rgc.last_request.append(
                    NextPhaseRequest(
                        sender_run_governor_id=self.rgc.uid,
                        receiver_run_governor_id=self.rgc.uid,
                        next_phase=next_phase,
                    )
                )
            else:
                LOG.info(
                    "RunGovernor(id=0x%x, uid=%s) finished phase %d/%d. "
                    "Reached a complete shutdown.",
                    id(self.rgc),
                    self.rgc.uid,
                    next_phase,
                    run.num_phases,
                )
            await self.rgc.major_domo_worker.transceive(
                self.rgc.next_reply[0],
                True,
            )
