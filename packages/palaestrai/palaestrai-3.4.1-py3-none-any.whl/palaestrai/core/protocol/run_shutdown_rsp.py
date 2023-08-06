from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExperimentRunShutdownResponse:
    """Response to a :class:`Executor` if an experiment run was stopped
    successfully.

    Parameters
    ----------
    sender_run_governor_id: str
        ID of the sending run governor.
    receiver_executor_id: str
        ID of the receiving executor.
    experiment_run_id: str
        ID of the started experiment run.
    successful: bool
        True, if the start was successful. False otherwise.
    error: Exception
        The error (message) if successful is False.

    """

    sender_run_governor_id: str
    receiver_executor_id: str
    experiment_run_id: str
    successful: bool
    error: Exception

    @property
    def sender(self):
        """ID of the sending run governor."""
        return self.sender_run_governor_id

    @property
    def receiver(self):
        """ID of the receiving executor."""
        return self.receiver_executor_id
