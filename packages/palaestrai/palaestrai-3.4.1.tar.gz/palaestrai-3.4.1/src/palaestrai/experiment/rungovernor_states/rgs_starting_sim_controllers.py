from __future__ import annotations

import io
import signal
import traceback
from typing import TYPE_CHECKING

import aiomultiprocess
import setproctitle

from ...core import RuntimeConfig
from ...util.spawn import spawn_wrapper
from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from ...experiment import RunGovernor
    from ...simulation import SimulationController


async def _run_simulation_controller(
    simulation_controller: SimulationController,
):
    """Executes the :py:class:`SimulationController` main loop

    This is a wrapper function around :py:func:`SimulationController.run`.
    It takes care of clearing signal handlers, setting the proctitle,
    and generally catching errors in a meaningful in order to report it
    to the RunGovernor without simply dying.

    Parameters
    ----------
    simulation_controller : palaestrai.simulation.SimulationController
        An initialized simulation controller, ready to be run.

    Returns
    -------
    Any
        Whatever the concrete :py:func:`SimulationController.run`
        method returns.
    """
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGABRT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    setproctitle.setproctitle(
        "palaestrAI[SimulationController-%s]" % simulation_controller.uid[-6:]
    )
    try:
        rc = await simulation_controller.run()
        LOG.debug(
            "SimulationController(id=0x%x, uid=%s) exited normally.",
            id(simulation_controller),
            simulation_controller.uid,
        )
        return rc
    except Exception as e:
        LOG.critical(
            "SimulationController(id=0x%x, uid=%s) encountered a fatal "
            "error in run(): %s",
            id(simulation_controller),
            simulation_controller.uid,
            e,
        )
        tb = io.StringIO()
        traceback.print_exc(file=tb)
        LOG.debug(
            "SimulationController(id=0x%x, uid=%s) encountered a fatal "
            "error in run(): %s",
            id(simulation_controller),
            simulation_controller.uid,
            e,
            tb.getvalue(),
        )
        raise e


class RGSStartingSimControllers(RunGovernorState):
    """Represent the STARTING_SIM_CONTROLLERS state of the run
    governor.

    This state is entered after STARTING_SETUP succeeds. During
    this state, processes for all required simulation controllers are
    created (but not started).

    Possible next states are
    * :class:`.RGSStartingEnvConductors in the normal case
    * :class:`.RGSErrorHandlingStarting in the error case.

    Parameters
    ----------
    rgc: :class:`.RunGovernor`
        The run governor instance that provides the context for this
        state.

    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "STARTING_SIM_CONTROLLERS")

    async def run(self):
        self._init_sim_controllers()

    def next_state(self):
        from . import RGSErrorHandlingStarting, RGSStartingEnvConductors

        if len(self.rgc.errors) > 0:
            self.rgc.state = RGSErrorHandlingStarting(self.rgc)
        else:
            self.rgc.state = RGSStartingEnvConductors(self.rgc)

    def _init_sim_controllers(self):
        """Initialize all given simulation controllers as subprocesses.

        All objects of type :py:class:`SimulationController` are
        treated as subprocesses. As long as they run on the same
        machine, they are initialized in this method.

        The processes are not started.
        """
        sim_controllers = list(
            self.rgc.experiment_run.simulation_controllers(
                self.rgc.current_phase
            ).values()
        )
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) initializing %d "
            "simulation controller(s).",
            id(self.rgc),
            self.rgc.uid,
            len(sim_controllers),
        )

        def _make_process(sc):
            sc.experiment_run_id = self.rgc.experiment_run_id
            return aiomultiprocess.Process(
                name=f"SimulationController-{sc.uid}",
                target=spawn_wrapper,
                args=(
                    f"SimulationController-{sc.uid}",
                    RuntimeConfig().to_dict(),
                    _run_simulation_controller,
                    [sc],
                ),
            )

        self.rgc.sim_controllers = {
            sc.uid: _make_process(sc) for sc in sim_controllers
        }
