from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from palaestrai.agent import (
        SensorInformation,
        ActuatorInformation,
    )


@dataclass
class AgentUpdateResponse:
    """Responds after an agent has acted via its :class:`Muscle`

    * Sender: :class:`Muscle`
    * Receiver: :class:`SimulationController`

    Parameters
    ----------
    sender_agent_id : str
        ID of the sending agent, e.g., a :class:`Muscle`
    receiver_simulation_controller_id : str
        ID of the receiving :class:`SimulationController`
    experiment_run_id : str
        ID of the current experiment run this environment participates in
    experiment_run_instance_id : str
        ID of the ::`ExperimentRun` object instance
    experiment_run_phase : int
        Current phase number of the experiment run
    sensor_information : List[SensorInformation]
        List of sensor readings :class:`SensorInformation`
    actuator_information : List[ActuatorInformation]
        List of actuator actions via :class:`ActuatorInformation`
    walltime : datetime.datetime
        The time the message was created, default: datetime.utcnow()
    """

    sender_agent_id: str
    receiver_simulation_controller_id: str
    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int
    sensor_information: List[SensorInformation]
    actuator_information: List[ActuatorInformation]
    walltime: datetime = field(default_factory=datetime.utcnow)

    @property
    def sender(self):
        return self.sender_agent_id

    @property
    def receiver(self):
        return self.receiver

    @property
    def actuators(self):
        return self.actuator_information
