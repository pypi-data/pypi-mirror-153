from __future__ import annotations

import inspect
import signal
import typing
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import (
    List,
    Union,
    Sequence,
    Optional,
    Dict,
    Any,
    TYPE_CHECKING,
)

from palaestrai.core import MajorDomoWorker
from palaestrai.core.protocol import (
    EnvironmentResetRequest,
    EnvironmentResetResponse,
    EnvironmentShutdownRequest,
    EnvironmentShutdownResponse,
    EnvironmentStartRequest,
    EnvironmentStartResponse,
    EnvironmentUpdateRequest,
    EnvironmentUpdateResponse,
)
from palaestrai.types import SimTime
from . import LOG
from .environment_baseline import EnvironmentBaseline
from .environment_state import EnvironmentState

if TYPE_CHECKING:
    from ..agent import (
        ActuatorInformation,
        SensorInformation,
        RewardInformation,
    )


class Environment(ABC):
    """Abstract class for environment implementation

    This abstract calls provides all necessary functions needed
    to implement a new environment. The developer only has to
    implement the functions start_environment and update.

    Parameters
    ----------
    uid : str
        Unique identifier to identify an environment
    broker_uri : str
        URI used to connect to the simulation broker
    seed : int
        Seed for recreation
    reward : typing.Callable
        A callable (function object, or a class implementing ``__call__``) that
        returns the reward value for the current state of the environment. The
        reward function is called with the list of all sensors
        (`Set[SensorInformation]`) as the named parameter `state`.
        (Cf. :py:meth:`palaestrai.agent.Reward.__call__()`)

    Attributes
    ----------
    _sensor_ids: List[str]
        A list of sensor IDs including the UID of the environment.
    _actuator_ids: List[str]
        A list of actuator IDs including the UID of the environment.
    """

    def __init__(self, uid: str, broker_uri: str, seed: int):
        self._uid = uid

        self.seed = seed

        self._ctx = None
        self._worker = None
        self._broker_uri = broker_uri

        self.sensors: List[SensorInformation] = []
        self.actuators: List[ActuatorInformation] = []

        # Filter lists for incoming actuators
        self._sensor_ids: List[str] = list()
        self._actuator_ids: List[str] = list()

        self.is_terminal = False

        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) created.",
            self.__class__,
            id(self),
            self.uid,
        )

    @property
    def uid(self) -> str:
        """The unique identifier of the Environment object"""
        return str(self._uid)

    @property
    def worker(self):
        """Return the major domo worker.

        The worker will be created if necessary.
        """
        if self._worker is None:
            self._worker = MajorDomoWorker(
                self._broker_uri,
                self.uid,
            )
        return self._worker

    def _handle_sigintterm(self, signum, frame):
        LOG.info(
            "Environment %s(id=0x%x, uid=%s) interrupted by signal %s in "
            "frame %s.",
            self.__class__,
            id(self),
            self.uid,
            signum,
            frame,
        )
        raise SystemExit()

    def _remove_uid(
        self, actuator_information_list: List[ActuatorInformation]
    ):
        for i in actuator_information_list:
            i.id = i.id.split(".", 1)[1]

    def _prepend_uid(
        self,
        sensor_actuator_information_list: Sequence[
            Union[SensorInformation, ActuatorInformation]
        ],
    ):
        for i in sensor_actuator_information_list:
            i.id = f"{self.uid}.{i.id}"

    async def run(self):
        """Main execution loop for an environment object

        This method takes care of the actual execution. As long as this
        method does not return, the environment is still active.

        The method receives and processes incoming messages. It applies
        changes to itself, i.e., setpoints delivered via
        :class:`~EnvironmentUpdateRequest` objects. It subsequently takes care
        of sending the appropriate update responses (
        :meth:`~EnvironmentUpdateResponse`).

        This method also interpretes :class:`~EnvironmentSetupRequest` and
        :class:`~EnvironmentShutdownRequest` messages.
        """
        reply = None
        signal.signal(signal.SIGINT, self._handle_sigintterm)
        signal.signal(signal.SIGTERM, self._handle_sigintterm)

        LOG.info(
            "Environment %s(id=0x%x, uid=%s) commencing run.",
            self.__class__,
            id(self),
            self.uid,
        )
        while not self.is_terminal:
            try:
                request = await self.worker.transceive(reply)
            except SystemExit:
                LOG.critical(
                    "Environment %s(id=0x%x, uid=%s) "
                    "interrupted in transceive by SIGINT/SIGTERM, "
                    "existing run loop",
                    self.__class__,
                    id(self),
                    self.uid,
                )
                break

            LOG.debug(
                "Environment %s(id=0x%x, uid=%s) received message: %s",
                self.__class__,
                id(self),
                self.uid,
                request,
            )
            if request is None:
                break
            elif isinstance(request, EnvironmentStartRequest):
                reply = self._handle_setup(request)
            elif isinstance(request, EnvironmentUpdateRequest):
                reply = self._handle_update(request)
            elif isinstance(request, EnvironmentResetRequest):
                reply = self._handle_reset(request)
            elif isinstance(request, EnvironmentShutdownRequest):
                reply = self._handle_shutdown(request)

        await self.worker.transceive(reply, skip_recv=True)
        LOG.info(
            "Environment %s(id=0x%x, uid=%s) completed shutdown: "
            "so much fun we had.",
            self.__class__,
            id(self),
            self.uid,
        )

    def _handle_setup(
        self, request: EnvironmentStartRequest
    ) -> EnvironmentStartResponse:
        """Handle an environment start request.

        The :meth:`.start_environment` is called that can be used by
        environments for setup purposes and that should provide the
        available sensors and actuators.

        Finally, an start response is prepared.

        Parameters
        ----------
        request: EnvironmentStartRequest
            The start request from the simulation controller.

        Returns
        -------
        EnvironmentStartResponse
            The answer from the environment, contains the available
            sensors and actuators.

        """
        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) received a %s",
            self.__class__,
            id(self),
            self.uid,
            repr(request),
        )

        # Start environment, return baseline; then,
        # prepend our UID to it to allow a sensor/actuator to be
        # distinguished by its containing environment.

        simtime = (
            inspect.signature(EnvironmentStartResponse)
            .parameters["simtime"]
            .default
        )
        baseline = self.start_environment()
        if isinstance(baseline, tuple):
            sensors, actuators = baseline
        elif isinstance(baseline, EnvironmentBaseline):
            sensors = baseline.sensors_available
            actuators = baseline.actuators_available
            simtime = baseline.simtime
        else:  # Wtf?!
            raise RuntimeError(
                "Unknown return value from environment start: %s "
                % (str(baseline))
            )
        sensors = deepcopy(sensors)
        actuators = deepcopy(actuators)
        self._prepend_uid([*sensors, *actuators])

        self._sensor_ids = [sen.sensor_id for sen in sensors]
        self._actuator_ids = [act.actuator_id for act in actuators]

        msg = EnvironmentStartResponse(
            sender_environment=self.uid,
            receiver_simulation_controller=request.sender,
            experiment_run_id=request.experiment_run_id,
            experiment_run_instance_id=request.experiment_run_instance_id,
            experiment_run_phase=request.experiment_run_phase,
            sensors=sensors,
            actuators=actuators,
            simtime=simtime,
        )
        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) sending %s",
            self.__class__,
            id(self),
            self.uid,
            repr(msg),
        )
        return msg

    def _handle_update(
        self, request: EnvironmentUpdateRequest
    ) -> EnvironmentUpdateResponse:
        """Handle an environment update request.

        The request contains current actuator values and the
        environment receives the actuator values in the update method.
        The environment answers with updated sensor readings, an
        environment reward, and the done flag, whether the
        environment has finished or not.

        Finally, an update response is prepared.

        Parameters
        ----------
        request: EnvironmentUpdateRequest
            The update request from the simulation controller, contains
            the current actuator values from one or more agent.

        Returns
        -------
        EnvironmentUpdateResponse
            The response for the simulation controller, containing the
            updated sensor values, a reward, and the done flag.

        """

        actuators = [
            act
            for act in request.actuators
            if act.actuator_id in self._actuator_ids
        ]
        actuators = deepcopy(actuators)
        self._remove_uid(actuators)

        state = self.update(actuators)

        simtime: Optional[SimTime] = None
        if isinstance(state, tuple):  # Handle old-style updates
            sensors = deepcopy(state[0])
            rewards = state[1]
            done = state[2]
        elif isinstance(state, EnvironmentState):  # new-style updates
            sensors = deepcopy(state.sensor_information)
            rewards = state.rewards
            done = state.done
            simtime = state.simtime
        else:  # Wtf?!
            raise RuntimeError(
                "Unknown return value from environment update: %s "
                % (str(state))
            )
        self._prepend_uid(sensors)

        return EnvironmentUpdateResponse(
            sender_environment_id=self.uid,
            receiver_simulation_controller_id=request.sender,
            experiment_run_id=request.experiment_run_id,
            experiment_run_instance_id=request.experiment_run_instance_id,
            experiment_run_phase=request.experiment_run_phase,
            sensors=sensors,
            rewards=rewards,
            is_terminal=done,
            simtime=simtime,
        )

    def _handle_reset(
        self, request: EnvironmentResetRequest
    ) -> EnvironmentResetResponse:
        """Handle an environment reset request.

        The actual behavior of the restart is delegated to the method
        :meth:`reset`.

        Parameters
        ----------
        request: EnvironmentResetRequest
            The reset request send by the simulation controller.

        Returns
        -------
        EnvironmentResetResponse
            The response for the simulation controller.

        """
        LOG.info(
            "Environment %s(id=0x%x, uid=%s) performing a reset due to "
            "EnvironmentResetRequest(simulation_controller_id=%s, "
            "environment_id=%s).",
            self.__class__,
            id(self),
            self.uid,
            request.sender,
            request.receiver,
        )
        return self.reset(request)

    def _handle_shutdown(
        self, request: EnvironmentShutdownRequest
    ) -> EnvironmentShutdownResponse:
        """Handle an environment shutdown request.

        The :meth:`shutdown` is called that handles the shutdown of the
        environment. Finally, a shutdown response is prepared.

        Parameters
        ----------
        request: EnvironmentShutdownRequest
            The shutdown request from the simulation controller.

        Returns
        -------
        EnvironmentShutdownResponse
            The shutdown response for the simulation controller.

        """
        LOG.info(
            "Environment %s(id=0x%x, uid=%s) now handling shutdown.",
            self.__class__,
            id(self),
            self.uid,
        )
        _ = self.shutdown()
        return EnvironmentShutdownResponse(request.run_id, self.uid, True)

    @abstractmethod
    def start_environment(
        self,
    ) -> Union[
        EnvironmentBaseline,
        typing.Tuple[List[SensorInformation], List[ActuatorInformation]],
    ]:
        """Launches execution of an environment.

        If the environment uses a simulation tool, this function
        can be used to initiate the simulation tool. In addion, this
        function is used to prepare the environment for the simulation.
        It must be able to provide initial sensor information.

        On a reset, this method is called to restart a new environment
        run. Therefore, it also must provide initial values for all
        variables used!

        Returns
        -------
        Union[EnvironmentBaseline,
        typing.Tuple[List[SensorInformation], List[ActuatorInformation]]]
            An :class:`~EnvironmentBaseline` object containing all initial data
            from the environment. For backwards compatibility, it is also
            possible (though deprecated) to return a tuple containing a list
            of available sensors and a list of available actuators.
        """
        pass

    @abstractmethod
    def update(
        self, actuators: List[ActuatorInformation]
    ) -> Union[
        EnvironmentState,
        typing.Tuple[List[SensorInformation], List[RewardInformation], bool],
    ]:
        """Function to update the environment

        This function receives the agent's actions and has to respond
        with new sensor information. This function should create a
        new simulation step.

        Parameters
        ----------
        actuators : List[ActuatorInformation]
            List of actuators with setpoints

        Returns
        -------
        Union[EnvironmentState,
        typing.Tuple[List[SensorInformation], List[RewardInformation], bool]]
            An :class:`~EnvironmentState` object; for backwards compatibility,
            environments can return a tuple containing a list of
            sensor readings (:class:`~SensorInformation`), a list of rewards
            (:class:`~RewardInformation`), and a flag whether the
            environment has terminated. Returning a tuple is considered
            deprecated.
        """
        pass

    def reset(
        self, request: EnvironmentResetRequest
    ) -> EnvironmentResetResponse:
        """Resets the environment in-place.

        The default behavior for a reset comprises:

        * calling shutdown to allow a graceful shutdown of
          environment simulation processes
        * calling :meth:`~.start_environment` again
        * preparing the :class:`EnvironmentResetResponse`

        If an environment requires a more special reset procedure,
        this method can be overwritten.

        Parameters
        ----------
        request : EnvironmentResetRequest
            The reset request send by the simulation controller.

        Returns
        -------
        EnvironmentResetResponse
            The response for the simulation controller.
        """
        # Allow graceful shutdown ...
        self.shutdown(reset=True)
        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) stopped the leftovers "
            "of the previous run. Initiating a new run now.",
            self.__class__,
            id(self),
            self.uid,
        )

        # ... but do not break the main loop
        self.is_terminal = False

        simtime = (
            inspect.signature(EnvironmentResetResponse)
            .parameters["simtime"]
            .default
        )
        baseline = self.start_environment()
        if isinstance(baseline, tuple):
            sensors, actuators = baseline
        elif isinstance(baseline, EnvironmentBaseline):
            sensors = baseline.sensors_available
            actuators = baseline.actuators_available
            simtime = baseline.simtime
        else:  # Wtf?!
            raise RuntimeError(
                "Unknown return value from environment start: %s "
                % (str(baseline))
            )

        sensors = deepcopy(sensors)
        actuators = deepcopy(actuators)
        self._prepend_uid([*sensors, *actuators])

        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) restarted successfully.",
            self.__class__,
            id(self),
            self.uid,
        )

        return EnvironmentResetResponse(
            receiver_simulation_controller_id=request.sender,
            sender_environment_id=self.uid,
            create_new_instance=False,
            sensors=sensors,
            actuators=actuators,
            simtime=simtime,
        )

    def shutdown(self, reset: bool = False) -> bool:
        """Initiate the environment shutdown.

        In this function the :attr:`.is_terminal` is set to True, which
        leads to a break of the main loop in the :meth:`.run` method.

        Parameters
        ----------
        reset: bool, optional
            Is set to True when only a reset is required. A concrete
            environment may distinguish between reset and shutdown.

        Returns
        -------
        bool
            ``True`` if the shutdown was successful, ``False`` otherwise.

        """
        self.is_terminal = not reset
        return True
