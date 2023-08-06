"""
This module contains the class :class:`EnvironmentConductor` that
controls the creation of new environments.
"""

import asyncio
import logging
import signal
import sys
from typing import List
from uuid import uuid4
from numpy.random import RandomState
import aiomultiprocess

from palaestrai.util import seeding, spawn_wrapper
from ..core import BasicState, MajorDomoWorker, RuntimeConfig
from ..core.protocol import (
    EnvironmentSetupRequest,
    EnvironmentSetupResponse,
    ShutdownRequest,
    ShutdownResponse,
)
from ..util.dynaloader import load_with_params

LOG = logging.getLogger("palaestrai.environment.conductor")


class EnvironmentConductor:
    """The environment conductor creates new environment instances.

    There could be multiple simulation runs and each would need a
    separate environment. The environment conductor controls the
    creation of those new environment instances.

    Parameters
    ----------
    env_cfg : dict
        Dictionary with parameters needed by the environment
    broker_uri : str
        URI used to connect to the simulation broker
    seed : uuid4
        Random seed for recreation
    uid : uuid4
        Unique identifier

    """

    def __init__(self, env_cfg, broker_uri, seed: int, uid=None):
        self._uid: str = uid if uid else "EnvironmentConductor-%s" % uuid4()
        self.seed: int = seed
        self.rng: RandomState = seeding.np_random(self.seed)[0]
        self.env_cfg = env_cfg
        self._broker_uri = broker_uri
        self._state = BasicState.PRISTINE

        self._tasks: List[aiomultiprocess.Process] = []
        self._worker = None

        LOG.debug(
            "EnvironmentConductor(id=0x%x, uid=%s) created.",
            id(self),
            self.uid,
        )

    @property
    def uid(self) -> str:
        return str(self._uid)

    @property
    def worker(self):
        if not self._worker:
            self._worker = MajorDomoWorker(
                broker_uri=self._broker_uri,
                service=self.uid,
            )
        return self._worker

    def _handle_signal_interrupt(self, signum):
        """Handle interrupting signals by notifying of the state change."""
        LOG.info(
            "EnvironmentConductor(id=0x%x, uid=%s) interrupted by signal %s.",
            id(self),
            self.uid,
            signum,
        )
        self._state = {
            signal.SIGINT.value: BasicState.SIGINT,
            signal.SIGABRT.value: BasicState.SIGABRT,
            signal.SIGTERM.value: BasicState.SIGTERM,
        }[signum]

    def _init_signal_handler(self):
        """Sets handlers for interrupting signals in the event loop."""
        signals = {signal.SIGINT, signal.SIGABRT, signal.SIGTERM}
        LOG.debug(
            "EnvironmentConductor(id=0x%x, uid=%s) "
            "registering signal handlers for signals %s.",
            id(self),
            self.uid,
            signals,
        )
        loop = asyncio.get_running_loop()
        for signum in signals:
            loop.add_signal_handler(
                signum, self._handle_signal_interrupt, signum
            )

    async def _monitor_state(self):
        known_state = self._state
        while known_state.value == self._state.value:
            try:
                await asyncio.sleep(0.5)
            except asyncio.CancelledError:
                break
        LOG.debug(
            "EnvironmentConductor(id=0x%x, uid=%s) "
            "state changed from %s to %s.",
            id(self),
            self.uid,
            known_state,
            self._state,
        )

    def _init_environment(self):
        """Initialize a new environment.

        Creates a new environment instance with its own UID.

        Returns
        -------
        str
            The unique identifier of the new environment
        """
        env_params = self.env_cfg.get("params", {})
        env_params.update(
            {
                "uid": self.env_cfg.get("uid", f"Environment-{uuid4()}"),
                "broker_uri": self._broker_uri,
                "seed": self.rng.randint(0, sys.maxsize),
            }
        )
        LOG.info(
            "EnvironmentConductor(id=0x%x, uid=%s) "
            "loading Environment '%s' with params '%s'.",
            id(self),
            self.uid,
            self.env_cfg["name"],
            env_params,
        )
        env = load_with_params(self.env_cfg["name"], env_params)

        LOG.debug(
            "EnvironmentConductor(id=0x%x, uid=%s) "
            "loaded Environment %s(id=0x%x, uid=%s).",
            id(self),
            self.uid,
            env.__class__,
            id(env),
            env.uid,
        )
        try:
            env_process = aiomultiprocess.Process(
                name=f"Environment-{self.uid}",
                target=spawn_wrapper,
                args=(
                    f"Environment-{self.uid}",
                    RuntimeConfig().to_dict(),
                    env.run,
                ),
            )
            env_process.start()
            self._tasks.append(env_process)
        except Exception as e:
            LOG.critical(
                "EnvironmentConductor(id=0x%x, uid=%s) "
                "encountered a fatal error while executing "
                "Environment(id=0x%x, uid=%s): %s.",
                id(self),
                self.uid,
                id(env),
                env.uid,
                e,
            )
            raise e
        return env.uid

    async def run(self):
        self._init_signal_handler()
        self._state = BasicState.RUNNING
        request = None
        reply = None
        LOG.info(
            "EnvironmentConductor(id=0x%x, uid=%s) commencing run: "
            "creating better worlds.",
            id(self),
            self.uid,
        )

        state_monitor_task = asyncio.create_task(self._monitor_state())
        while self._state == BasicState.RUNNING:
            transceive_task = asyncio.create_task(
                self.worker.transceive(reply)
            )
            tasks_done, tasks_pending = await asyncio.wait(
                {state_monitor_task, transceive_task},
                return_when=asyncio.FIRST_COMPLETED,
            )
            if transceive_task in tasks_pending:
                continue
            request = transceive_task.result()
            if not request:
                continue

            LOG.info(
                "EnvironmentConductor(id=0x%x, uid=%s) "
                "received request: %s(%s).",
                id(self),
                self.uid,
                request.__class__,
                request.__dict__,
            )

            if isinstance(request, EnvironmentSetupRequest):
                LOG.debug(
                    "EnvironmentConductor(id=0x%x, uid=%s) "
                    "received EnvironmentSetupRequest(experiment_run_id=%s).",
                    id(self),
                    self.uid,
                    request.experiment_run_id,
                )
                env_uid = self._init_environment()
                ssci = request.sender_simulation_controller_id
                reply = EnvironmentSetupResponse(
                    sender_environment_conductor=self.uid,
                    receiver_simulation_controller=ssci,
                    environment_id=env_uid,
                    experiment_run_id=request.experiment_run_id,
                    experiment_run_instance_id=request.experiment_run_instance_id,
                    experiment_run_phase=request.experiment_run_phase,
                    environment_type=self.env_cfg["name"],
                    environment_parameters=self.env_cfg.get("params", dict()),
                )
            if isinstance(request, ShutdownRequest):
                self._state = BasicState.STOPPING
                for task in self._tasks:
                    await task.join()

        reply = ShutdownResponse(
            request.experiment_run_id if request else None
        )
        await self.worker.transceive(reply, skip_recv=True)
        self._state = BasicState.FINISHED
        LOG.info(
            "EnvironmentConductor(id=0x%x, uid=%s) completed shutdown.",
            id(self),
            self.uid,
        )
