import asyncio
import itertools
import os
import signal
from typing import TYPE_CHECKING

import aiomultiprocess

from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSFinalizing(RunGovernorState):
    """Represents the FINALIZING state.

    Possible next states are
    * :class:`.RGSDone`.
    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "FINALIZING")

    async def run(self):
        await self._shutdown_tasks()
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) completed shutdown",
            id(self.rgc),
            self.rgc.uid,
        )

    def next_state(self):
        from . import RGSDone

        self.rgc.state = RGSDone(self.rgc)

    async def _shutdown_tasks(self):
        """Terminates all running subprocesses and waits for their end."""

        asyncio.get_running_loop().remove_signal_handler(signal.SIGTERM)
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) terminating process group. "
            "If there are no leftovers, this RunGovernor leaves for "
            "good.",
            id(self.rgc),
            self.rgc.uid,
        )
        os.killpg(0, signal.SIGTERM)
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) saw processes surviving. "
            "Let the reaping begin.",
            id(self.rgc),
            self.rgc.uid,
        )
        await asyncio.gather(
            *[
                RGSFinalizing._reap_process(p)
                for p in itertools.chain(
                    self.rgc.agent_conductors.values(),
                    self.rgc.env_conductors.values(),
                    self.rgc.sim_controllers.values(),
                )
            ]
        )

        self.rgc.agent_conductors = {}
        self.rgc.sim_controllers = {}
        self.rgc.env_conductors = {}

    @staticmethod
    async def _reap_process(process: aiomultiprocess.Process):
        """Terminates a process, joins and reaps it.

        :param process: The process we have to reap
        """
        if process.is_alive():
            process.terminate()
        try:
            await process.join(timeout=3)
        except asyncio.TimeoutError:
            if process.is_alive():
                process.kill()
