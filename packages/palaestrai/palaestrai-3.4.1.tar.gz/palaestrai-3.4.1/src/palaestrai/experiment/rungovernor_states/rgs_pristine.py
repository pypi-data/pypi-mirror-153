import os
from typing import TYPE_CHECKING

from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSPristine(RunGovernorState):
    """Represent the PRISTINE state of the run governor.

    No changes on the run governor have taken place until :meth:`run`
    is called. During this state, the process group is set so that
    all subprocesses can be identified as subprocesses of the run
    governor on the OS level.

    Notes
    -----
    The operation os.setpgrp is only available on UNIX-like systems.
    If a port to windows is ever considered again, a workaround is
    required.

    Possible next states are:

    * :class:`.RGSInitializing` since no errors are expected in this
      state.

    Parameters
    ----------
    rgc: :class:`.RunGovernor`
        The run governor instance that provides the context for this
        state.


    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "PRISTINE")

    async def run(self):
        # TODO: Maybe do some further cleanup first
        self.rgc.experiment_run = None
        self.rgc.experiment_run_id = None
        self.rgc.last_request = list()
        self.rgc.next_reply = list()

        os.setpgrp()
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) now leads process group %s.",
            id(self.rgc),
            self.rgc.uid,
            os.getpgid(os.getpid()),
        )

    def next_state(self):
        from . import RGSInitializing

        self.rgc.state = RGSInitializing(self.rgc)
