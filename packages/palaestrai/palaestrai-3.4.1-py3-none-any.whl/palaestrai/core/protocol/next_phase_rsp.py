from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NextPhaseResponse:
    """A response of a :class:`RunGovernor` to itself for a next phase
    request.

    This message object might seem a bit unnecessary at first. But to
    not (further) violate the major domo pattern, the run governor
    needs to send a reply in the transceiving state. But unless the run
    governor has received an ExperimentRunStartRequest or an
    ExperimentRunShutdownRequest, no reply is available.

    This response is send although there is no one waiting for it.

    Parameters
    ----------
    sender_run_governor_id: str
        ID of the sending run governor
    receiver_run_governor_id: str
        ID of the receiving run governer (it's the same as the sender).
    has_next_phase: bool
        True if at least one phase is following.
    """

    sender_run_governor_id: str
    receiver_run_governor_id: str
    has_next_phase: bool

    @property
    def sender(self):
        """ID of the sending run governor."""
        return self.sender_run_governor_id

    @property
    def receiver(self):
        """ID of the receiving run governor."""
        return self.receiver_run_governor_id
