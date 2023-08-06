from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EnvironmentResetNotificationRequest:
    """Notifies an agent about an environment reset.

    Parameters
    ----------
    sender_simulation_controller_id: str
        ID of the sending :class:`.SimulationController`.
    receiver_agent_id: str
        ID of the receiving :class:`palaestrai.agent.Muscle`.

    """

    sender_simulation_controller_id: str
    receiver_agent_id: str

    @property
    def sender(self):
        return self.sender_simulation_controller_id

    @property
    def receiver(self):
        return self.receiver_agent_id
