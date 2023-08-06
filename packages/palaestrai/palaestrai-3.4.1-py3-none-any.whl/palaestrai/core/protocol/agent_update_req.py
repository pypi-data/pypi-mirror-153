from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from palaestrai.agent import (
        SensorInformation,
        ActuatorInformation,
        RewardInformation,
    )
    from palaestrai.types import Mode, SimTime


@dataclass
class AgentUpdateRequest:
    """Provides fresh data from a :class:`SimulationController` to
    an :class:`Agent`.

    * Sender: :class:`SimulationController`
    * Receiver: :class:`Muscle`

    Parameters
    ----------
    sender_simulation_controller : str
        The sending :class:`SimulationController`
    receiver_agent_id : str
        The receiving agent, e.g., a :class:`Muscle`
    experiment_run_id : str
        ID of the current experiment run this agent participates in
    experiment_run_instance_id : str
        ID of the ::`ExperimentRun` object instance
    experiment_run_phase : int
        Current phase number of the experiment run
    actuators : List[ActuatorInformation]
        List of actuators available for the agent
    sensors : List[SensorInformation]
        Sensor input data for the agent
    reward : List[RewardInformation]
        Current reward from the environment
    is_terminal : bool
        Indicates whether this is the last update from the environment or not
    simtimes : Dict[str, palaestrai.types.SimTime]
        Contains time values from the environment. It maps environment UIDs to
        either simtime_ticks (::`int`) or simtime_timestamps (::`datetime`)
        via the ::`SimTime` class.
    walltime : datetime.datetime
        The time the message was created, default: datetime.utcnow()
    """

    sender_simulation_controller_id: str
    receiver_agent_id: str
    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int
    actuators: List[ActuatorInformation]
    sensors: List[SensorInformation]
    rewards: List[RewardInformation]
    is_terminal: bool
    mode: Mode
    simtimes: Dict[str, SimTime] = field(default_factory=dict)
    walltime: datetime = field(default_factory=datetime.utcnow)

    @property
    def sender(self):
        return self.sender_simulation_controller_id

    @property
    def receiver(self):
        return self.receiver_agent_id
