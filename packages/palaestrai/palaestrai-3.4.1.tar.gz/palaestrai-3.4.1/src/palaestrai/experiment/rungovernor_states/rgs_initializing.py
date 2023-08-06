import asyncio
import signal
from typing import TYPE_CHECKING

from palaestrai.core import MajorDomoClient, MajorDomoWorker

from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSInitializing(RunGovernorState):
    """Represent the INITIALIZING state of the run governor.

    This state is entered after the PRISTINE state. During this state,
    a signal handler and a signal monitor for graceful termination are
    initialized and the communication is set up.

    Possible next states are
    * :class:`.RGSTransceiving` in the normal case.
    * :class:`.RGSErrorHandlingInitializing in the error case.

    Parameters
    ----------
    rgc: :class:`.RunGovernor`
        The run governor instance that provides the context for this
        state.

    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "INITIALIZING")

    async def run(self):
        self._init_signal_handler()
        self._init_signal_monitor()
        self._init_communication()

    def next_state(self):
        from . import RGSErrorHandlingInitializing, RGSTransceiving

        if len(self.rgc.errors) > 0:
            self.rgc.state = RGSErrorHandlingInitializing(self.rgc)
        else:
            self.rgc.state = RGSTransceiving(self.rgc)

    def _init_signal_handler(self):
        signals = {signal.SIGABRT, signal.SIGTERM}
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) "
            "registering signal handlers for signals %s.",
            id(self.rgc),
            self.rgc.uid,
            signals,
        )
        loop = asyncio.get_running_loop()
        for signum in signals:
            loop.add_signal_handler(
                signum, self._handle_signal_termination, signum
            )
        loop.add_signal_handler(signal.SIGINT, self._handle_signal_interrupt)

    def _handle_signal_termination(self, signum):
        LOG.info(
            "RunGovernor(id=0x%x, uid=%s) interrupted by signal %s.",
            id(self.rgc),
            self.rgc.uid,
            signum,
        )
        self.rgc.signal_received = signum

    def _handle_signal_interrupt(self):
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) received SIGINT; "
            "trusting the upper brass is handling this.",
            id(self.rgc),
            self.rgc.uid,
        )

    def _init_signal_monitor(self):
        """Create a task that monitors the signal_received flag."""
        self.rgc.signal_monitor_task = asyncio.create_task(
            self._monitor_signal()
        )

    async def _monitor_signal(self):
        """Check if the signal_received was set."""
        while self.rgc.signal_received is None:
            try:
                await asyncio.sleep(0.5)
            except asyncio.CancelledError:
                break
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) received signal %s.",
            id(self.rgc),
            self.rgc.uid,
            self.rgc.signal_received,
        )
        self.rgc.signal_received = None

    def _init_communication(self):
        self.rgc.major_domo_worker = MajorDomoWorker(
            broker_uri=self.rgc.broker_uri,
            service=self.rgc.uid,
        )
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) started "
            "MajorDomoWorker(id=0x%x, uri=%s).",
            id(self.rgc),
            self.rgc.uid,
            id(self.rgc.major_domo_worker),
            self.rgc.broker_uri,
        )
        self.rgc.major_domo_client = MajorDomoClient(self.rgc.broker_uri)
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) started "
            "MajorDomoClient(id=0x%x, uri=%s).",
            id(self.rgc),
            self.rgc.uid,
            id(self.rgc.major_domo_client),
            self.rgc.broker_uri,
        )
