"""This module contains the class :class:`AgentConductor` that
stores all information the agents need about an actuator.

"""
from __future__ import annotations

import asyncio
import logging
import signal
import socket
import uuid
from copy import deepcopy
from typing import Union, List, Optional
from uuid import uuid4

import aiomultiprocess
import setproctitle

from palaestrai.core import MajorDomoWorker, RuntimeConfig
from palaestrai.core.protocol import (
    AgentSetupRequest,
    AgentSetupResponse,
    ShutdownRequest,
    ShutdownResponse,
)
from palaestrai.util import spawn_wrapper
from palaestrai.util.dynaloader import load_with_params
from palaestrai.util.exception import TasksNotFinishedError
from .brain import Brain
from .muscle import Muscle

LOG = logging.getLogger(__name__)


async def _run_brain(agent_conductor_uid: str, brain: Brain):
    """Executes the Brain main loop, handling signals and errors

    This method wraps :py:func:`Brain.run`. It takes care of proper
    installment of signal handlers, setting of the proctitle, and most
    importantly, error handling. This method should be wrapped in the
    :py:func:`palaestrai.util.spawn_wrapper` function, which, in turn, is the
    target of an :py:func:`aiomultiprocess.Process.run` call.

    Parameters
    ----------
    agent_conductor_uid : str
        UID of the governing ::`~AgentConductor`
    brain : Brain
        The ::`~Brain` instance that should be run.

    Returns
    -------
    Any
        Whatever the ::`~Brain.run` method returns.
    """
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGABRT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    setproctitle.setproctitle(
        "palaestrAI[Brain-%s]" % agent_conductor_uid[-6:]
    )
    try:
        return await brain.run()
    except Exception as e:
        LOG.critical(
            "Brain(id=0x%x, agent_conductor_uid=%s) died from a fatal wound "
            "to the head: %s",
            id(brain),
            agent_conductor_uid,
            e,
        )
        raise


async def _run_muscle(muscle: Muscle):
    """Executes the ::`~Muscle` main loop, handling signals and errors

    This method wraps :py:func:`Muscle.run`. It takes care of proper
    installment of signal handlers, setting of the proctitle, and most
    importantly, error handling. This method should be wrapped in the
    :py:func:`palaestrai.util.spawn_wrapper` function, which, in turn, is the
    target of an :py:func:`aiomultiprocess.Process.run` call.

    Parameters
    ----------
    muscle : Muscle
        The  ::`~Muscle` instance that runs

    Returns
    -------
    Any
        Whatever ::`~Muscle.run` returns
    """
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGABRT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    setproctitle.setproctitle("palaestrAI[Muscle-%s]" % muscle.uid[-6:])
    try:
        return await muscle.run()
    except Exception as e:
        LOG.critical(
            "Muscle(id=0x%x, uid=%s) suffers from dystrophy: %s",
            id(muscle),
            muscle.uid,
            e,
        )
        raise


class AgentConductor:
    """This creates a new agent conductor (AC).

    The AC receives an agent config, which contains all information for
    the brain and the muscle. Additional information, like the current
    run ID, are part of the AgentSetupRequest.

    Parameters
    ----------
    broker_uri: str
        Connection information, should be in the format
        protocol://ip-address:port, e.g., "tcp://127.0.0.1:45310"
    agent_config: dict
        A *dict* containing information, how to instantiate brain and
        muscle.
    seed: int
        The random seed for this agent conductor.
    phase_name: str
        Name of the phase the experiment is currently in.
    experiment_run_id: str
        The ID of the overall experiment of which this brain is part of.
    uid: str
        The uid for this agent conductor object.

    Attributes
    ----------
    agents: List[str]
        A list containing the uids of all the muscles.
    brain: :class:`palaestrai.agent.Brain`:
        A reference to the brain instance of this agent conductor.
    brain_process: :class:`aiomultiprocess.Process`
        A reference to the brain's process.
    objective: :class:`.Objective`
        A reference to the objective instance of this agent conductor.
    tasks: List[aiomultiprocess.Process]
        A list with references to the muscle's tasks.
    """

    def __init__(
        self,
        broker_uri: str,
        agent_config: dict,
        seed: int,
        phase_name: str,
        experiment_run_id: str = None,
        uid=None,
    ):
        self._worker = None
        self._broker_uri = broker_uri
        self._uid = str(uid) if uid else "AgentConductor-%s" % uuid4()

        self.tasks: List[aiomultiprocess.Process] = []
        self.seed = seed
        self.conf = agent_config
        self._brain_uri: Optional[str] = None
        self._brain: Union[Brain, None] = None
        self.objective = load_with_params(
            self.conf["objective"]["name"], self.conf["objective"]["params"]
        )
        self.agents: List[uuid.UUID] = []

        self.ac_socket = None
        self._brain_process = None
        self.experiment_run_id = experiment_run_id
        self.phase_name = phase_name

    def _handle_sigintterm(self, signum, frame):
        LOG.info(
            "AgentConductor(id=0x%x, uid=%s) "
            "interrupted by signal %s in frame %s",
            id(self),
            self.uid,
            signum,
            frame,
        )
        raise SystemExit()

    @property
    def uid(self):
        """Unique, opaque ID of the agent conductor object"""
        return self._uid

    @property
    def worker(self):
        """Getter for the :py:class:`MajorDomoWorker` object

        This method returns (possibly lazily creating) the current
        :py:class:`MajorDomoWorker` object. It creates this worker on demand.
        It is not safe to call this method between forks, as forks copy
        the context information for the worker which is process-depentent.

        :rtype: MajorDomoWorker
        """
        if self._worker is None:
            self._worker = MajorDomoWorker(self._broker_uri, self.uid)
        return self._worker

    def _init_brain(self, sensors, actuators):
        """Initialize the brain process.

        Each agent, which is represented by an individual conductor,
        has one brain process. This function initializes the brain
        process.

        The agent conductor allocates the port for the brain-muscle
        interconnection. For this, it binds to a random port given from the OS.
        It passes the port to the brain and closes the socket; the Brain will
        then re-open the socket as ZMQ socket. That works because sockets are
        refcounted and the ref count goes to 0 when the ::`Brain` closes the
        socket before re-opening it. The agent conductor then uses the port
        number (not the socket itself) to pass it to the ::`Muscle` objects,
        which then know where to find their ::`Brain`.

        Parameters
        ----------
        sensors : List[SensorInformation]
            List of available sensors.
        actuators : List[ActuatorInformation]
            List of available actuators.

        Returns
        -------
        str
            The listen URI of the brain.
        """

        # We create a simple socket first in order to get a free port from the
        # OS. Its only an ephermal server, we close the port as soon as the
        # Brain process is started.

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", 0))
        listen_port = sock.getsockname()[1]

        # deepcopy, or we'd modify the original. Not what we want:
        try:
            params = deepcopy(self.conf["brain"]["params"])
        except KeyError:
            params = {}

        params.update(
            {
                "seed": self.seed,
                "sensors": sensors,
                "actuators": actuators,
                "objective": self.objective,
                "muscle_updates_listen_uri_or_socket": sock,
                "store_path": self.__construct_store_path(self.conf),
            }
        )
        self._brain: Brain = load_with_params(
            self.conf["brain"]["name"], params
        )
        if "load" in self.conf.keys():
            load_path = self._construct_load_path(self.conf)
            if load_path is not None:
                self._brain.load_model(load_path)

        try:
            self._brain_process = aiomultiprocess.Process(
                name=f"Brain-{self.uid}",
                target=spawn_wrapper,
                args=(
                    f"Brain-{self.uid}",
                    RuntimeConfig().to_dict(),
                    _run_brain,
                    [self.uid, self._brain],
                ),
            )
            self._brain_process.start()
            sock.close()

            LOG.debug(
                "AgentConductor(id=0x%x, uid=%s) started Brain(id=0x%x)",
                id(self),
                self.uid,
                id(self._brain),
            )
        except Exception as e:
            LOG.critical(
                "AgentConductor(id=0x%x, uid=%s) "
                "encountered a fatal error while executing "
                "Brain(id=0x%x): %s",
                id(self),
                self.uid,
                id(self._brain),
                e,
            )
            raise
        return "tcp://%s:%s" % (
            "*" if RuntimeConfig().public_bind else "127.0.0.1",
            listen_port,
        )

    def _init_muscle(self, uid, brain_uri):
        """Function to initialize a new muscle

        Each agent consists of one brain and at least one muscle
        but is not limited to one muscle. There can be multiple
        muscles and muscles can be restarted.

        Parameters
        ----------
        uid : uuid4
            Unique identifier to identify the muscle
        brain_uri : str
            URI string designating the ::`Brain` listening socket to connect
            a ::`Muscle` to.
        """
        try:
            params = deepcopy(self.conf["muscle"]["params"])
        except KeyError:
            params = {}

        params.update(
            {
                "uid": uid,
                "brain_uri": brain_uri,
                "brain_id": id(self._brain),
                "broker_uri": self._broker_uri,
                "path": self._construct_load_path(self.conf),
            }
        )
        muscle = load_with_params(self.conf["muscle"]["name"], params)
        muscle.setup()
        self.agents.append(uid)
        try:
            agent_process = aiomultiprocess.Process(
                name=f"Muscle-{uid}",
                target=spawn_wrapper,
                args=(
                    f"Muscle-{uid}",
                    RuntimeConfig().to_dict(),
                    _run_muscle,
                    [muscle],
                ),
            )
            agent_process.start()
            LOG.debug(
                "AgentConductor(id=0x%x, uid=%s) "
                "started Muscle(id=0x%x, uid=%s).",
                id(self),
                self.uid,
                id(muscle),
                muscle.uid,
            )
            self.tasks.append(agent_process)
        except Exception as e:
            LOG.critical(
                "AgentConductor(id=0x%x, uid=%s) "
                "encountered a fatal error while executing "
                "Muscle(id=0x%x, uid=%s): %s",
                id(self),
                self.uid,
                id(muscle),
                muscle.uid,
                e,
            )
            raise e

    async def run(self):
        """Monitors agents and facilitates information interchange

        This method is the main loop for the :py:class:`AgentConductor`. It
        monitors the :py:class:`Brain` object and :py:class:`Muscle` instances
        of the agent (i.e., the processes) and transceives/routes messages.

        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGABRT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        setproctitle.setproctitle(
            "palaestrAI[AgentConductor-%s]" % self._uid[-6:]
        )

        signal.signal(signal.SIGINT, self._handle_sigintterm)
        signal.signal(signal.SIGTERM, self._handle_sigintterm)
        LOG.info(
            "AgentConductor(id=0x%x, uid=%s) commencing run: "
            "Today's solutions to tomorrow's problems",
            id(self),
            self.uid,
        )
        proceed = True
        request = None
        reply = None
        while proceed:
            try:
                request = await self._housekeeping(reply)
            except TasksNotFinishedError:
                continue
            except SystemExit:
                break

            if isinstance(request, AgentSetupRequest):
                reply = self._handle_agent_setup(request)

            if isinstance(request, ShutdownRequest):
                await self._handle_shutdown(request)
                break

        LOG.debug(
            "AgentConductor(id=0x%x, uid=%s) sending "
            "ShutdownResponse(experiment_run_id=%s)",
            id(self),
            self.uid,
            request.run_id,
        )
        reply = ShutdownResponse(request.run_id)
        try:
            await self.worker.transceive(reply, skip_recv=True)
        except SystemExit:
            pass  # If they really want to, we can skip that, too.
        LOG.info(
            "AgentConductor(id=0x%x, uid=%s) completed shutdown: "
            "ICH, AC, BIN NUN TOD, ADJÖ [sic].",
            id(self),
            self.uid,
        )

    async def _housekeeping(self, reply):
        """Keep the household clean and lively.

        In this method, replies are send and requests are received.
        Furthermore, the AC sees over his child tasks (muscles and
        brain).

        Parameters
        ----------
        reply:
            The next reply to send

        Returns
        -------
        request
            The request received during transceiving.

        """
        LOG.debug(
            "AgentConductor(id=0x%x, uid=%s) starts housekeeping. "
            "Everything needs to be in proper order.",
            id(self),
            self.uid,
        )
        try:
            transceive_task = asyncio.create_task(
                self.worker.transceive(reply)
            )
            muscle_tasks = [asyncio.create_task(p.join()) for p in self.tasks]
            brain_tasks = (
                [asyncio.create_task(self._brain_process.join())]
                if self._brain_process
                else []
            )
            tasks_done, tasks_pending = await asyncio.wait(
                [transceive_task] + muscle_tasks + brain_tasks,
                return_when=asyncio.FIRST_COMPLETED,
            )
            if not tasks_done:
                # This shouldn't happen, but you never know.
                raise TasksNotFinishedError()

            terminated_workers = [
                p
                for p in self.tasks + [self._brain_process]
                if p is not None and not p.is_alive() and p.exitcode != 0
            ]
            if terminated_workers:
                # I don't think the other tasks should end like this?
                LOG.critical(
                    "AgentConductor(id=0x%x, uid=%s) "
                    "has suffered from prematurely dead tasks: %s",
                    id(self),
                    self.uid,
                    [p.name for p in terminated_workers],
                )
                signal.signal(signal.SIGINT, signal.SIG_DFL)
                signal.signal(signal.SIGABRT, signal.SIG_DFL)
                signal.signal(signal.SIGTERM, signal.SIG_DFL)
                raise RuntimeError(
                    "AgentConductor(id=0x%x, uid=%s) "
                    "has dead tasks at hands: %s"
                    % (
                        id(self),
                        self.uid,
                        [p.name for p in terminated_workers],
                    )
                )
            if transceive_task not in tasks_done:
                await transceive_task
            request = transceive_task.result()
        except SystemExit as e:
            LOG.warning(
                "AgentConductor(id=0x%x, uid=%s) "
                "stopping due to SIGINT/SIGTERM",
                id(self),
                self.uid,
            )
            raise e

        LOG.debug(
            "AgentConductor(id=0x%x, uid=%s) got a %s. "
            "Let's see how we handle this one.",
            id(self),
            self.uid,
            request,
        )

        return request

    def _handle_agent_setup(self, request: AgentSetupRequest):
        """Handle the agent setup request.

        One setup request will result in one new muscle created.
        The brain will be created if necessary.

        Parameters
        ----------
        request: :class:`.AgentSetupRequest`
            The agent setup request with information for the muscle to
            be created.

        Returns
        -------
        :class:`.AgentSetupResponse`
            The response for the simulation controller.

        """
        if request.receiver_agent_conductor == self.uid:
            if self._brain is None:
                self._brain_uri = self._init_brain(
                    request.sensors, request.actuators
                )
            self._init_muscle(request.agent_id, self._brain_uri)

            return AgentSetupResponse(
                sender_agent_conductor=self.uid,
                receiver_simulation_controller=request.sender,
                experiment_run_id=request.experiment_run_id,
                experiment_run_instance_id=request.experiment_run_instance_id,
                experiment_run_phase=request.experiment_run_phase,
                agent_id=request.agent_id,
            )

    def _construct_load_path(self, conf: dict) -> Union[str, None]:
        """Construct the path specified by conf

        If required keys are not present an attempt is made
        to use a default value

        If the path could not be constructed a warning is logged

        :param conf: The config for the agent conductor
            The config needs the key 'load'
                load should be a dictionary that has at least 'phase_name' and may have
                       key      |                description            |        default
                'base'          : determines the base path to save to   : '.'
                'experiment_id' : the experiment_id to load from        : current experiment_id
                'agent_name'    : the name of the agent to load from    : same as the loading agent
            and 'name' which is the default fallback for agent_name
        :return: The path to load from on success, None otherwise
        """
        if "load" in conf:
            load_conf = conf["load"]
        else:
            return None

        path = ""

        if "base" in load_conf.keys():
            path += load_conf["base"]
        else:
            path += "."

        if "experiment_id" in load_conf.keys():
            path += f"/{load_conf['experiment_id']}"
        elif self.experiment_run_id is not None:
            path += f"/{self.experiment_run_id}"
        else:
            LOG.warning(
                "AgentConductor(id=0x%x, uid=%s) "
                "got a load_conf but 'experiment_id' is not provided. "
                "THE BRAIN WILL NOT LOAD!",
                id(self),
                self.uid,
            )
            return None

        if "phase_name" in load_conf.keys():
            path += f"/{load_conf['phase_name']}"
        else:
            LOG.warning(
                "AgentConductor(id=0x%x, uid=%s) got a load_conf but 'phase_name' is not provided. "
                "THE BRAIN WILL NOT LOAD!",
                id(self),
                self.uid,
            )
            return None

        if "agent_name" in load_conf.keys():
            path += f"/{load_conf['agent_name']}"
        else:
            path += f"/{conf['name']}"

        return path

    def __construct_store_path(self, conf: dict) -> str:
        """Construct the path specified by conf

        :param conf: The config for the agent conductor
            The config needs the key 'name' which is the name of
            the agent that stores
            It can have the key conf["brain"]["params"]["store_path"]
            to specify a base path to store to
        :return: The path to save to
        """
        path = ""

        if "store_path" in conf["brain"]["params"].keys():
            path += conf["brain"]["params"]["store_path"]
        else:
            path += "."

        path += f"/{self.experiment_run_id}/{self.phase_name}/{conf['name']}"

        return path

    async def _handle_shutdown(self, request):
        """Handle the shutdown request for this agent conductor.

        It is expected that all muscles and the brain of this
        agent conductor already received a shutdown request. Therefore,
        all this method does is to wait(join) for the processes.

        Parameters
        ----------
        request: :class:`.ShutdownRequest`
            The shutdown request
        """
        for task in self.tasks:
            await task.join()
        await self._brain_process.join()
