import itertools
from typing import TYPE_CHECKING

from palaestrai.core.protocol import (
    SimulationStartRequest,
    SimulationStartResponse,
)
from palaestrai.util.exception import InvalidResponseError
from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSStartingRun(RunGovernorState):
    """Represent the STARTING_RUN state of the run governor.

    This state is entered after STARTING_AGENT_CONDUCTORS succeeds.
    During this state, all previously created processes will be
    started, which marks the begin of the experiment run.

    Possible next states are
    * :class:`.RGSTransceiving in the normal case
    * :class:`.RGSErrorHandlingStarting in the error case

    Parameters
    ----------
    rgc: :class:`.RunGovernor`
        The run governor instance that provides the context for this
        state.

    """

    def __init__(self, ctx: "RunGovernor"):
        super().__init__(ctx, "STARTING_RUN")

    async def run(self):
        self._start_processes()
        await self._send_start_request()
        self._check_reply()
        LOG.info(
            "RunGovernor(id=0x%x, uid=%s) started execution of phase "
            "%d: '%s'.",
            id(self.rgc),
            self.rgc.uid,
            self.rgc.current_phase,
            self.rgc.experiment_run.get_phase_name(self.rgc.current_phase),
        )

    def next_state(self):
        from . import RGSErrorHandlingStarting, RGSTransceiving

        if len(self.rgc.errors) > 0:
            self.rgc.state = RGSErrorHandlingStarting(self.rgc)
        else:
            self.rgc.state = RGSTransceiving(self.rgc)

    def _start_processes(self):
        for proc in itertools.chain(
            self.rgc.sim_controllers.values(),
            self.rgc.env_conductors.values(),
            self.rgc.agent_conductors.values(),
        ):
            proc.start()

    async def _send_start_request(self):
        for sc_uid in self.rgc.sim_controllers.keys():
            LOG.debug(
                "RunGovernor(id=0x%x, uid=%s) requesting start of "
                "SimulationController(uid=%s).",
                id(self.rgc),
                self.rgc.uid,
                sc_uid,
            )
            msg = SimulationStartRequest(
                sender_run_governor_id=self.rgc.uid,
                receiver_simulation_controller_id=sc_uid,
                experiment_run_id=self.rgc.experiment_run_id,
                experiment_run_instance_id=self.rgc.experiment_run.instance_uid,
                experiment_run_phase=self.rgc.current_phase,
                experiment_run_phase_id=self.rgc.experiment_run.get_phase_name(
                    self.rgc.current_phase
                ),
                experiment_run_phase_configuration=self.rgc.experiment_run.phase_configuration(
                    self.rgc.current_phase
                ),
            )
            response = await self.rgc.major_domo_client.send(sc_uid, msg)
            if not isinstance(response, SimulationStartResponse):
                self.add_error(
                    InvalidResponseError(
                        SimulationStartResponse.__class__, response.__class__
                    )
                )
            else:
                LOG.debug(
                    "RunGovernor(id=0x%x, uid=%s) received "
                    "SimulationStartResponse(sc_uid=%s).",
                    id(self.rgc),
                    self.rgc.uid,
                    sc_uid,
                )

    def _check_reply(self):
        request = self.rgc.last_request.pop()
        LOG.debug("Last request is %s", request)
