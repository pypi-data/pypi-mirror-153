"""This module contains the abstract class :class:`Muscle` that
is used to implement the acting part of an agent.

"""
import logging
import signal
import uuid
from abc import ABC, abstractmethod

import setproctitle
import zmq
import zmq.asyncio

from palaestrai.core import MajorDomoWorker
from palaestrai.core.protocol import (
    AgentShutdownRequest,
    AgentShutdownResponse,
    AgentUpdateRequest,
    AgentUpdateResponse,
    EnvironmentResetNotificationRequest,
    EnvironmentResetNotificationResponse,
    MuscleShutdownRequest,
    MuscleUpdateRequest,
    MuscleUpdateResponse,
)
from palaestrai.core.serialisation import deserialize, serialize
from ..types.mode import Mode
from ..util.exception import UnknownModeError

LOG = logging.getLogger(__name__)


class Muscle(ABC):
    """An acting entity in an environment.

    Each Muscle is an acting entity in an environment: Given a sensor input,
    it proposes actions. Thus, Muscles implement input-to-action mappings.
    A muscle does, however, not learn by itself; for that, it needs a
    :class:`~Brain`. Every time a muscle acts, it sends the following inputs
    to a Brain:

    * Sensor inputs it received
    * actuator set points it provided
    * reward received from the proposed action.

    When implementing an algorithm, you have to derive from the Muscle ABC and
    provide the following methods:

    1. :func:`~propose_actions`, which implements the input-to-action mapping
    2. :func:`~update`, which handles how updates from the :class:`~Brain` are
       incorporated into the muscle.

    Parameters
    ----------
    broker_uri : str
        the URI which is used to connect to the simulation broker. It is
        used to communicate with the simulation controller.
    brain_uri : str
        URI for communication with the brain.
    uid : uuid4
        a universal id, that is either provided or assigned here.
    brain_id: str
        the ID of the brain this muscle belongs to.

    """

    def __init__(self, broker_uri, brain_uri, uid, brain_id, path):
        self._brain_uri = brain_uri
        self._broker_uri = broker_uri
        self._load_path = path
        self._ctx = None
        self._sync_ctx = None
        self._dealer_socket = None
        self.uid = uid or uuid.uuid4()
        self.brain_id = brain_id
        self._worker = None
        self.run_id = None
        self._last_inputs = None
        self._last_actions = None
        self._additional_data = None
        self._mode = Mode.TRAIN

    @property
    def context(self):
        """Return the asynchronous zmq context.

        The context will be created if necessary.
        """
        if self._ctx is None:
            self._ctx = zmq.asyncio.Context()
        return self._ctx

    @property
    def sync_context(self):
        """Return the synchronous zmq context.

        The context will be created if necessary.
        """

        if self._sync_ctx is None:
            self._sync_ctx = zmq.Context()
        return self._sync_ctx

    @property
    def worker(self):
        """Return the major domo worker.

        The worker will be created if necessary.
        """

        if self._worker is None:
            self._worker = MajorDomoWorker(self._broker_uri, self.uid)
        return self._worker

    @property
    def dealer_socket(self):
        """Return the zmq dealer socket.

        The socket will be created if necessary.
        """

        if self._dealer_socket is None:
            self._dealer_socket = self.sync_context.socket(zmq.DEALER)
            self._dealer_socket.identity = str(self.uid).encode("ascii")
            self._dealer_socket.connect(self._brain_uri)
        return self._dealer_socket

    def _handle_sigintterm(self, signum, frame):
        LOG.info(
            "Muscle %s(id=0x%x, uid=%s) interrupted by signal %s in frame %s.",
            self.__class__,
            id(self),
            self.uid,
            signum,
            frame,
        )
        raise SystemExit()

    def send_to_brain(self, message, flags=0):
        """
        This method is used for communication with the brain. It is
        needed to update the muscle.

        Parameters
        ----------
        message : MuscleUpdateRequest
            The message to be sent to the brain
        flags : int, optional
            Flags for the socket's send method.

        Returns
        -------
        MuscleUpdateResponse
            Response received from the brain.

        """
        z = serialize(message)
        self.dealer_socket.send(z, flags=flags)
        z = self.dealer_socket.recv_multipart(flags=flags)
        response = deserialize(z)
        return response

    async def run(self):
        """Start the main loop of the muscle.

        This method is handling incoming messages and calls the
        corresponding method.

        If an ´AgentUpdateRequest´ is received, it's processed to a
        ´MuscleUpdateRequest´, which triggers a reaction from the
        ´brain´ module (i.e. ´MuscleUpdateResponse´) and finally an
        ´AgentUpdateResponse´ with the action proposals is sent.

        If an ´AgentShutdownRequest´ is received it's processed to a
        ´MuscleUpdateRequest´ and an ´AgentShutdownResponse´ to initiate
        termination of the agent.

        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGABRT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        setproctitle.setproctitle("palaestrAI[Muscle-%s]" % self.uid[-6:])

        signal.signal(signal.SIGINT, self._handle_sigintterm)
        signal.signal(signal.SIGTERM, self._handle_sigintterm)

        terminal = False
        reply = None
        LOG.info(
            "Muscle %s(id=0x%x, uid=%s) started: Ready for a power workout.",
            self.__class__,
            id(self),
            self.uid,
        )
        while not terminal:
            request = await self.worker.transceive(reply)

            if request is None:
                raise TypeError
            elif isinstance(request, AgentUpdateRequest):
                reply = self._handle_agent_update(request)
            elif isinstance(request, EnvironmentResetNotificationRequest):
                reply = self.handle_environment_reset_notification(request)
            elif isinstance(request, AgentShutdownRequest):
                reply = self._handle_agent_shutdown(request)
                terminal = True

        await self.worker.transceive(reply, skip_recv=True)

        LOG.info(
            "Muscle %s(id=0x%x, uid=%s) completed shutdown: Now I am sore.",
            self.__class__,
            id(self),
            self.uid,
        )

    def _handle_agent_update(
        self, request: AgentUpdateRequest
    ) -> AgentUpdateResponse:
        """Handle an agent update.

        Every update request to the muscle is forwarded to the brain.
        The brain answers with information that the muscle can use to
        update itself.

        Finally, an update response is prepared.

        Parameters
        ----------
        request : AgentUpdateRequest
            The update request from the simulation controller.
            Contains, among other information, the current sensor
            readings and the reward of the previous actions.

        Returns
        -------
        AgentUpdateResponse
            The update response with the agent's actions.

        """
        LOG.debug(
            "Muscle %s(id=0x%x, uid=%s) received %s.",
            self.__class__,
            id(self),
            self.uid,
            request,
        )
        self.run_id = request.experiment_run_id
        self._mode = request.mode
        if self._mode == Mode.TRAIN:
            msg = MuscleUpdateRequest(
                sensors_available=request.sensors,
                actuators_available=request.actuators,
                network_input=self._last_inputs,
                last_network_output=self._last_actions,
                reward=request.rewards,
                is_terminal=request.is_terminal,
                additional_data=self._additional_data,
            )
            LOG.debug(
                "Muscle(id=0x%x, uid=%s) sending %s to brain.",
                id(self),
                self.uid,
                msg,
            )
            response = self.send_to_brain(msg)
            LOG.debug(
                "Muscle(id=0x%x, uid=%s) received %s from brain",
                id(self),
                self.uid,
                response,
            )
            if not isinstance(response, MuscleUpdateResponse):
                LOG.critical(
                    "Muscle(id=0x%x, uid=%s) ",
                    "expected a MuscleUpdateResponse from brain, but got %s "
                    "instead: Ignoring, but it might spasm in strange ways.",
                    id(self),
                    self.uid,
                    response,
                )
            elif response.is_updated:
                self.update(response.updates)
        elif self._mode == Mode.TEST:
            self.prepare_model()
        else:
            raise UnknownModeError()

        if not request.is_terminal:
            (
                env_actions,
                self._last_actions,
                self._last_inputs,
                self._additional_data,
            ) = self.propose_actions(request.sensors, request.actuators, False)
            return AgentUpdateResponse(
                sender_agent_id=self.uid,
                receiver_simulation_controller_id=request.sender,
                experiment_run_id=request.experiment_run_id,
                experiment_run_instance_id=request.experiment_run_instance_id,
                experiment_run_phase=request.experiment_run_phase,
                actuator_information=env_actions,
                sensor_information=request.sensors,
            )
        else:
            return AgentUpdateResponse(
                sender_agent_id=self.uid,
                receiver_simulation_controller_id=request.sender,
                experiment_run_id=request.experiment_run_id,
                experiment_run_instance_id=request.experiment_run_instance_id,
                experiment_run_phase=request.experiment_run_phase,
                actuator_information=[],
                sensor_information=[],
            )

    def handle_environment_reset_notification(
        self, request: EnvironmentResetNotificationRequest
    ) -> EnvironmentResetNotificationResponse:
        """Handle notification about environment reset.

        Whenever an environment has finished and a new episode is
        started, a notification is send to the agents. Normally,
        they just acknowledge the reset and go on as usual.

        If the agent should, somehow, react to the reset, this method
        can be overwritten to define that reaction.

        Parameters
        ----------
        request: EnvironmentResetNotificationRequest
            The notification request from the simulation controller.

        Returns
        -------
        EnvironmentResetNotificationResponse
            The response for the simulation controller.

        """
        LOG.info(
            "Muscle %s(id=0x%x, uid=%s) acknowledged environment reset.",
            self.__class__,
            id(self),
            self.uid,
        )
        return EnvironmentResetNotificationResponse(
            receiver_simulation_controller_id=request.sender,
            sender_agent_id=self.uid,
        )

    def _handle_agent_shutdown(
        self, request: AgentShutdownRequest
    ) -> AgentShutdownResponse:
        """Handle agent shutdown.

        The muscle sends a final update request to the brain. The
        response from the brain is ignored.
        Finally, a shutdown response is preprared

        Parameters
        ----------
        request : AgentShutdownRequest
            The shutdown request from the simulation controller. This
            message has no further information that need to be
            processed.

        Returns
        -------
        AgentShutdownResponse
            The shutdown response that confirms the shutdown of the
            muscle.

        """
        LOG.info(
            "Muscle %s(id=0x%x, uid=%s) received AgentShutdownRequest.",
            self.__class__,
            id(self),
            self.uid,
        )
        msg = MuscleShutdownRequest(
            sender_muscle_id=self.uid,
            agent_id=request.agent_id,
            experiment_run_id=request.experiment_run_id,
        )
        _ = self.send_to_brain(msg)

        return AgentShutdownResponse(request.experiment_run_id, self.uid, True)

    @abstractmethod
    def setup(self, *args, **kwargs):
        pass

    @abstractmethod
    def propose_actions(
        self, sensors, actuators_available, is_terminal=False
    ) -> tuple:
        """Process new sensor information and produce actuator
        setpoints.

        This is the abstract method which needs to be implemented.
        It works together with a brain and must be tuned to it
        accordingly.

        This method takes a list of :class:sensor_information and has
        to return a list of actuators (this information is given by the
        actuators_available parameter). How the actuator setpoints are
        produced and how the sensor information are processed is up to
        the developer.

        Mainly it is used for reinforcement learning agents. In this
        case, the muscle has a "finished" model and uses it to generate
        the actuator_information. All deep learning tasks are done by
        the brain. The muscle uses the model exclusively and does not
        make any changes itself.

        Parameters
        ----------
        sensors : list[SensorInformation]
            List of new SensorInformation for all available sensors
        actuators_available : list[ActuatorInformation]
            List of all actuators for which a new setpoint is required.
        is_terminal : bool
            Indicator if the simulation run has terminated

        Returns
        -------
        tuple[list, list, list, dict]
            A tuple of three lists, the first one will be send to the
            environment and needs to be properly scaled, the second and third
            one will be send to the brain. The second contains the NN outputs
            the third one the scaled/transformed NN inputs.
            Also returing dict with additional_information for the brain
        """
        pass

    @abstractmethod
    def update(self, update):
        """Update the muscle.

        This method is called if the brain sends an update. What is to
        be updated is up to the specific implementation. However, this
        method should update all necessary components.

        """
        pass

    def store_model(self):
        """Store a model persistently.

        This method can be used if the muscle does not use a brain that
        takes care of storing the model.

        """
        pass

    @abstractmethod
    def prepare_model(self):
        """Loading a trained model for testing

        If palaestrai is used to test a trained model it has to load
        the trained model, either from a Database or from a file.
        Loading from a file should be always implemented so it can be
        used as a fallback solution. Also it could/should be checked
        if the model is already initialized, to reduce execution time.

        """
        pass

    @abstractmethod
    def __repr__(self):
        pass
