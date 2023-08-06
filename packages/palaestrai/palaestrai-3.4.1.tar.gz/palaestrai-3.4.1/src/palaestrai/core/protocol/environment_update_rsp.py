from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from palaestrai.types import SimTime
    from palaestrai.agent import SensorInformation
    from palaestrai.agent import RewardInformation


@dataclass
class EnvironmentUpdateResponse:
    """Reports the current state of the environment.

    * Sender: :class:`Environment`
    * Receiver: :class:`SimulationController

    Parameters
    ----------
    sender_environment_id : str
        ID of the sending :class:`Environment`
    receiver_simulation_controller_id : str
        ID of the receiving :class:`SimulationController`
    experiment_run_id : str
        ID of the current experiment run this environment participates in
    experiment_run_instance_id : str
        ID of the ::`ExperimentRun` object instance
    experiment_run_phase : int
        Current phase number of the experiment run
    sensors : List[SensorInformation]
        Current list of sensor data
    param reward : List[RewardInformation]
        Reward given by the environment
    is_terminal : bool
        Indicates whether the environment has reached a terminal state
    simtime : Optional[palaestrai.types.SimTime]
        The current in-simulation time as provided by the environmment
    walltime : datetime
        The time the message was created, default: datetime.utcnow()
    """

    sender_environment_id: str
    receiver_simulation_controller_id: str
    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int
    sensors: List[SensorInformation]
    rewards: List[RewardInformation]
    is_terminal: bool
    simtime: Optional[SimTime] = None
    walltime: datetime = field(default_factory=datetime.utcnow)

    @property
    def sender(self):
        return self.sender_environment_id

    @property
    def receiver(self):
        return self.receiver_simulation_controller_id
