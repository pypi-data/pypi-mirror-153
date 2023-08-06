from __future__ import annotations
from dataclasses import dataclass

# from typing import TYPE_CHECKING


@dataclass
class MuscleShutdownRequest:
    """Notifies the :class:`palaestrai.agent.Brain` that the :class:`palaestrai.agent.Muscle received
    a shutdown request.

    Parameters
    ----------
    sender_muscle_id: str
        The uid of the sender muscle.
    agent_id: str
        The uid of the corresponding :class:`.Agent`.
    experiment_run_id: str
        The uid of the corresponding experiment run.

    """

    sender_muscle_id: str
    agent_id: str
    experiment_run_id: str

    @property
    def sender(self):
        return self.sender_muscle_id
