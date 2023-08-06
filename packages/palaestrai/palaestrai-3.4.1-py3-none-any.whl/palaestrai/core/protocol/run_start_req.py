from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from palaestrai.experiment import ExperimentRun


@dataclass
class ExperimentRunStartRequest:
    """Request to a :class:`RunGovernor` to start a new experiment run

    Parameters
    ----------
    sender_executor_id: str
        ID of the sending executor.
    receiver_run_governor_id: str
        ID of the receiving run governor.
    experiment_run: :class:`ExperimentRun`
        The experiment run that should be executed.
    experiment_run_id: str
        ID for this instance run of the given run.
    """

    sender_executor_id: str
    receiver_run_governor_id: str
    experiment_run_id: str
    experiment_run: ExperimentRun

    @property
    def sender(self):
        """ID of the sending executor."""
        return self.sender_executor_id

    @property
    def receiver(self):
        """ID of the receiving run governor."""
        return self.receiver_run_governor_id

    def __str__(self):
        return (
            "ExperimentRunStartRequest for Run='%s'" % self.experiment_run.uid
        )
