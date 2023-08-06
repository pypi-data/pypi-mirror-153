import itertools
from typing import TYPE_CHECKING

from palaestrai.util.exception import PrematureTaskDeathError

from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSHandlingDeadChildren(RunGovernorState):
    """Represent the HANDLING_DEAD_CHILDREN state of the run governor.

    Possible next states are:
    * :class:`.RGSStoppingTransceiving` in the case of errors.
    * :class:`.RGSStoppingSimulation` in the default case.

    Parameters
    ----------
    rgc: :class:`.RunGovernor`
        The run governor instance that provides the context for this
        state.


    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "HANDLING_DEAD_CHILDREN")

    async def run(self):
        all_processes = [
            proc
            for proc in itertools.chain(
                self.rgc.sim_controllers.values(),
                self.rgc.env_conductors.values(),
                self.rgc.agent_conductors.values(),
            )
        ]
        dead_children = [proc for proc in all_processes if not proc.is_alive()]

        # Clean up: Either we have processes that ended normally, then
        # we just free ressources and reap the children. If some
        # process died from a premature error, we have to shut down
        # the whole experiment, as it will doubtedly have any value to
        # continue it.

        if dead_children:

            def _clean(d: dict):
                return {
                    uid: proc for uid, proc in d.items() if proc.is_alive()
                }

            self.rgc.agent_conductors = _clean(self.rgc.agent_conductors)
            self.rgc.env_conductors = _clean(self.rgc.env_conductors)
            self.rgc.sim_controllers = _clean(self.rgc.sim_controllers)

        premature_deaths = [
            proc for proc in dead_children if proc.exitcode != 0
        ]
        if premature_deaths:
            LOG.critical(
                "RunGovernor(id=0x%x, uid=%s) "
                "has suffered from premature task death: %s.",
                id(self.rgc),
                self.rgc.uid,
                premature_deaths,
            )
            self.add_error(PrematureTaskDeathError())

    def next_state(self):
        from . import RGSStoppingSimulation, RGSStoppingTransceiving

        if len(self.rgc.errors) > 0:
            self.rgc.state = RGSStoppingTransceiving(self.rgc)
        else:
            self.rgc.state = RGSStoppingSimulation(self.rgc)
