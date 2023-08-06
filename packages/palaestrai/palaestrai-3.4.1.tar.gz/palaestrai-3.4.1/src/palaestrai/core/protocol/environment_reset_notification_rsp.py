from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EnvironmentResetNotificationResponse:
    """Response to an environment reset notification.

    Parameters
    ----------
    sender_agent_id: str
        ID of the sending :class:`palaestrai.agent.Muscle`.
    receiver_simulation_controller_id: str
        ID of the receiving :class:`.SimulationController`.

    """

    sender_agent_id: str
    receiver_simulation_controller_id: str

    @property
    def sender(self):
        return self.sender_agent_id

    @property
    def receiver(self):
        return self.receiver_simulation_controller_id
