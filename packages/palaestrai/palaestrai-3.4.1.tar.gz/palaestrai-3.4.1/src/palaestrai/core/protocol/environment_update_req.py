from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from palaestrai.agent import ActuatorInformation


@dataclass
class EnvironmentUpdateRequest:
    """Updates an environment with new set points from actuators.

    * Sender: :class:`SimulationController`
    * Receiver: :class:`Environment`

    Parameters
    ----------
    sender_simulation_controller : str
        ID of the sending :class:`SimulationController`
    receiver_environment : str
        ID of the receiving environment
    experiment_run_id : str
        ID of the current experiment run this environment participates in
    experiment_run_instance_id : str
        ID of the ::`ExperimentRun` object instance
    experiment_run_phase : int
        Current phase number of the experiment run
    actuators : List[ActuatorInforation]
        A list of :class:`ActuatorInformation`objects that convey new setpoints
        to the environment
    walltime : datetime
        The time the message was created, default: datetime.utcnow()
    """

    sender_simulation_controller: str
    receiver_environment: str
    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int
    actuators: List[ActuatorInformation]
    walltime: datetime = field(default_factory=datetime.utcnow)

    @property
    def sender(self):
        return self.sender_simulation_controller

    @property
    def receiver(self):
        return self.receiver_environment

    @property
    def environment_id(self):
        return self.receiver_environment
