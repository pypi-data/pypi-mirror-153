from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EnvironmentResetRequest:
    """Requests a reset of an :class:`.Environment`.

    Parameters
    ----------
    sender_simulation_controller_id: str
        ID of the sending :class:`.SimulationController`.
    receiver_environment_id: str
        ID of the receiving :class:`.Environment`.

    """

    sender_simulation_controller_id: str
    receiver_environment_id: str

    @property
    def sender(self):
        return self.sender_simulation_controller_id

    @property
    def receiver(self):
        return self.receiver_environment_id
