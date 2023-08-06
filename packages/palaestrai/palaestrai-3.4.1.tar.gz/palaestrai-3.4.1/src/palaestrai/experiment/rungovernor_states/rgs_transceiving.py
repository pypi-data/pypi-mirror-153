import asyncio
import itertools
from typing import TYPE_CHECKING

import aiomultiprocess
from palaestrai.core.protocol import ExperimentRunShutdownRequest
from palaestrai.core.protocol import ExperimentRunStartRequest
from palaestrai.core.protocol import (
    SimulationControllerTerminationRequest as SimCtrlTermReq,
)
from palaestrai.util.exception import (
    DeadChildrenRisingAsZombiesError,
    InvalidRequestError,
    RequestIsNoneError,
    SignalInterruptError,
    TasksNotFinishedError,
)

from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSTransceiving(RunGovernorState):
    """Represent the TRANSCEIVING state of the run governor.

    This state is usually entered after INITIALIZING succeeds. Other
    states that may lead to this state are STARTING_RUN and
    HANDLING_SIM_CONTROLLER_TERMINATION.

    During this state, the run governor waits for incoming requests and
    sends replies to these requests. Depending on the request received,
    the run governor will transition to the next state handling this
    very request.

    Possible next states are
    * :class:`.RGSStarting on ExperimentStartRequest
    * :class:`.RGSHandlingSimControllerTermination on
       SimulationControllerTerminationRequest
    * :class:`.RGSStoppingSimulation on ExperimentShutdownRequest
    * :class:`.RGSErrorHandlingStarting in the error case.

    Parameters
    ----------
    rgc: :class:`.RunGovernor`
        The run governor instance that provides the context for this
        state.

    """

    def __init__(self, ctx: "RunGovernor"):
        super().__init__(ctx, "TRANSCEIVING")

    async def run(self):
        self._create_transceive_task()
        tasks_done, pending, all_processes = await self._wait_for_tasks()

        if not self._tasks_are_done(tasks_done):
            return

        if self._has_dead_children(all_processes):
            return

        await self._get_request(tasks_done)

        for task in pending:
            if task != self.rgc.signal_monitor_task:
                task.cancel()

    def next_state(self):
        from . import (
            RGSErrorHandlingTransceiving,
            RGSHandlingSimControllerTermination,
            RGSStartingSetup,
            RGSStoppingSimulation,
        )

        dispatcher = {
            ExperimentRunStartRequest: RGSStartingSetup,
            SimCtrlTermReq: RGSHandlingSimControllerTermination,
            ExperimentRunShutdownRequest: RGSStoppingSimulation,
        }
        try:
            state = dispatcher[self.rgc.last_request[0].__class__]
        except KeyError:
            self.add_error(
                InvalidRequestError(
                    [req for req in dispatcher],
                    self.rgc.last_request[0].__class__,
                )
            )
        except IndexError:
            # Is raised on signal interrupt because the last request
            # is none.
            pass

        if len(self.rgc.errors) > 0:
            state = RGSErrorHandlingTransceiving

        self.rgc.state = state(self.rgc)

    def _create_transceive_task(self):
        try:
            reply = self.rgc.next_reply.pop()
        except IndexError:
            reply = None

        self.rgc.transceive_task = asyncio.create_task(
            self.rgc.major_domo_worker.transceive(reply)
        )

    async def _wait_for_tasks(self):
        all_processes = [
            proc
            for proc in itertools.chain(
                self.rgc.sim_controllers.values(),
                self.rgc.env_conductors.values(),
                self.rgc.agent_conductors.values(),
            )
        ]

        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) "
            "in transceive and checking tasks (%s)",
            id(self.rgc),
            self.rgc.uid,
            [(proc.name, proc.is_alive()) for proc in all_processes]
            + [self.rgc.signal_monitor_task, self.rgc.transceive_task],
        )

        tasks_done, pending = await asyncio.wait(
            [
                asyncio.create_task(self._join_process(proc))
                for proc in all_processes
            ]
            + [self.rgc.signal_monitor_task, self.rgc.transceive_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        return tasks_done, pending, all_processes

    def _tasks_are_done(self, tasks_done) -> bool:
        if not tasks_done:
            # This shouldn't happen, but you never know
            self.add_error(TasksNotFinishedError())
            return False

        if self.rgc.signal_monitor_task in tasks_done:
            self.add_error(SignalInterruptError())
            return False

        return True

    def _has_dead_children(self, all_processes) -> bool:
        dead_children = [proc for proc in all_processes if not proc.is_alive()]

        if dead_children:
            self.add_error(DeadChildrenRisingAsZombiesError())
            return True
        return False

    async def _get_request(self, tasks_done):

        if self.rgc.transceive_task not in tasks_done:
            await self.rgc.transceive_task

        self.rgc.last_request.append(self.rgc.transceive_task.result())
        self.rgc.transceive_task = None
        if self.rgc.last_request[0] is None:
            LOG.warning(
                "RunGovernor(id=0x%x, uid=%s) "
                "received None request; ignoring",
                id(self.rgc),
                self.rgc.uid,
            )
            self.add_error(RequestIsNoneError())
            return False
        else:
            LOG.info(
                "RunGovernor(id=0x%x, uid=%s) received %s.",
                id(self.rgc),
                self.rgc.uid,
                self.rgc.last_request[0],
            )
        return True

    async def _join_process(self, process: aiomultiprocess.Process):
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) "
            "monitoring Process(name=%s, is_alive=%s)",
            id(self.rgc),
            self.rgc.uid,
            process.name,
            process.is_alive(),
        )
        while process.exitcode is None:
            await asyncio.sleep(5)
            LOG.debug(
                "RunGovernor(id=0x%x, uid=%s) "
                "joined Process(name=%s, is_alive=%s, exitcode=%s, PID=%s)",
                id(self.rgc),
                self.rgc.uid,
                process.name,
                process.is_alive(),
                process.exitcode,
                process.pid,
            )
