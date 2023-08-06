from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExperimentRunShutdownRequest:
    """Request to a :class:`RunGovernor` to stop an experiment run.

    Parameters
    ----------
    sender_executor_id: str
        ID of the sending executor.
    receiver_run_governor_id: str
        ID of the receiving run governor.
    experiment_run: :class:`ExperimentRun`
        The experiment run that should be executed.

    """

    sender_executor_id: str
    receiver_run_governor_id: str
    experiment_run_id: str

    @property
    def sender(self):
        """ID of the sending executor."""
        return self.sender_executor_id

    @property
    def receiver(self):
        """ID of the receiving run governor."""
        return self.receiver_run_governor_id
