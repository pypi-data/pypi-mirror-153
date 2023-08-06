from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NextPhaseRequest:
    """A request that is send from a :class:`RunGovernor` to itself.

    Actually, this request is not sent at all. It is directly stored
    in the run governor's list of last requests (sending it via client
    results in an error because of time-related dependencies in the
    order of messages sent by the run governor).

    It is processed in the state STARTING_SETUP and initiates a new
    phase of an experiment run.

    Parameters
    ----------
    sender_run_governor_id: str
        ID of the sending run governor
    receiver_run_governor_id: str
        ID of the receiving run governer (it's the same as the sender).
    next_phase: int
        Index of the next phase to execute.
    """

    sender_run_governor_id: str
    receiver_run_governor_id: str
    next_phase: int

    @property
    def sender(self):
        """ID of the sending run governor."""
        return self.sender_run_governor_id

    @property
    def receiver(self):
        """ID of the receiving run governor."""
        return self.receiver_run_governor_id
