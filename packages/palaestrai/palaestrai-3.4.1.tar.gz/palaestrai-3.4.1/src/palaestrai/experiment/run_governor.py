"""This module contains the :class:`.RunGovernor`. """
import io
import logging
import traceback
import uuid
from typing import TYPE_CHECKING, Dict, Union

from palaestrai.core import MajorDomoClient, MajorDomoWorker

from .rungovernor_states.base_state import RunGovernorState
from .rungovernor_states.rgs_pristine import RGSPristine

if TYPE_CHECKING:
    import aiomultiprocess
    from palaestrai.experiment import TerminationCondition
    from palaestrai.experiment.experiment_run import ExperimentRun


LOG = logging.getLogger(__name__)


class RunGovernor:
    """This class implements the Run-Governor.

    Upon receiving requests from the executor, a RunGovernor instance
    handles a single experiment run by starting it, initialize the
    simulation controllers, the environment and the agent conductors,
    and, finally, shutting the experiment run down.

    The RunGovernor is implemented as state machine and this class
    provides the context for the distinct state classes. A freshly
    initialized RunGovernor waits in the state PRISTINE until the run
    method is called by the executor. See the distinct state classes
    for more information.

    Parameters
    ----------
    broker_connection: str
        The URI representing the connection to the broker for
        communication with the executor.
    termination_condition: TerminationCondition
        The condition that tells the RunGovernor when to stop the
        simulation.
    rungov_uid: str
        The UUID for this RunGovernor is provided by the executor.

    Attributes
    ----------
    uid: str
        The UUID of this RunGovernor
    termination_condition: :class:`.TerminationCondition`
        A reference to the TerminationCondition instance.
    run_broker: :class:`.MajorDomoBroker`
        The broker for the communication with the simulation
        controller, the agents, and the environments.
    experiment_run_id: str
        The UUID of the current experiment run.
    tasks: List[aiomultiprocess.Process]
        A list of tasks the RunGovernor has started and that it has
        to shutdown in the end.
    worker: :class:`.MajorDomoWorker`
        The major domo worker for handling incoming requests
    client: :class:`.MajorDomoClient`
        The major domo client for sending requests to other workers.
    shutdown: bool
        The major kill switch of the RunGovernor. Setting this to false
        will stop the RunGovernor after the current state.
    state: :class:`.RunGovernorState`
        Holds the current state instance. The first state is PRISTINE.
    errors: List[Exception]
        A list that is used to collect errors raised in the states.

    """

    def __init__(self, broker_uri: str, uid: str = None):
        # self._binding_uri = "tcp://*:45306"

        self.uid = uid if uid else "RunGovernor-%s" % str(uuid.uuid4())
        self.broker_uri = broker_uri
        self.major_domo_client: MajorDomoClient
        self.major_domo_worker: MajorDomoWorker

        self.termination_condition: TerminationCondition
        self.experiment_run: Union[ExperimentRun, None] = None
        self.experiment_run_id: Union[str, None] = None
        self.current_phase = 0
        self.current_episode = 0
        self.transceive_task = None
        self.signal_monitor_task = None
        self.signal_received = None
        self.agent_conductors: Dict[str, aiomultiprocess.Process] = dict()
        self.env_conductors: Dict[str, aiomultiprocess.Process] = dict()
        self.sim_controllers: Dict[str, aiomultiprocess.Process] = dict()

        # List is a "workaround" to satisfy the type checking ...
        self.last_request: list = list()
        self.next_reply: list = list()
        self.stopping = False
        self.shutdown = False
        self.state: RunGovernorState = RGSPristine(self)
        self.errors: list = list()
        self.dead_children: list = list()
        # self._simulation_controllers: dict = dict()

    async def run(self):
        """Start the main loop of the run governor.

        In each iteration, the run method of the current state is
        called.

        """
        while not self.shutdown:
            LOG.info(
                "RunGovernor(id=0x%x, uid=%s) now processing state %s.",
                id(self),
                self.uid,
                self.state.name,
            )
            try:
                await self.state.run()
                self.state.next_state()
            except Exception as err:
                LOG.critical(
                    "RunGovernor(id=0x%x, uid=%s) died in disgrace!",
                    id(self),
                    self.uid,
                )

                tb = io.StringIO()
                traceback.print_exc(file=tb)
                LOG.critical(
                    "RunGovernor(id=0x%x, uid=%s) has crashed in state "
                    "%s with error %s",
                    id(self),
                    self.uid,
                    self.state.name,
                    tb.getvalue(),
                )
                raise err
        LOG.info(
            "RunGovernor(id=0x%x, uid=%s) has finished.", id(self), self.uid
        )
