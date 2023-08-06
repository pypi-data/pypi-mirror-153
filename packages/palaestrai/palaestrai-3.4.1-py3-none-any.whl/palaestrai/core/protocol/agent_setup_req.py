from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from palaestrai.agent import SensorInformation, ActuatorInformation


@dataclass
class AgentSetupRequest:
    """Initializes the setup of an :class:`Agent`.

    * Sender: :class:`SimulationController`
    * Receiver: :class:`AgentConductor`

    Parameters
    ----------
    sender_simulation_controller : str
        ID of the sending :class:`SimulationController`
    receiver_agent_conductor : str
        ID of the receiving :class:`AgentConductor`
    experiment_run_id : str
        ID of the experiment run the agent participates in
    experiment_run_instance_id : str
        ID of the ::`ExperimentRun` object instance
    experiment_run_phase : int
        Current phase number of the experiment run
    configuration : Dict
        The complete agent configuration
    sensors : List[SensorInformation]
        List of :class:`SensorInformation objects for the sensors available
        to the agent
    actuators : List[ActuatorInformation]
        List of of :class:`ActuatorInformation objects for the
        actuators available to the agent
    agent_id : str
        ID of the agent we're setting up (e.g., a :class:`Muscle`)
    agent_name : Optional[str]
        Name of the :class:`Agent`, if any
    """

    sender_simulation_controller: str
    receiver_agent_conductor: str
    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int
    configuration: Dict
    sensors: List[SensorInformation]
    actuators: List[ActuatorInformation]
    agent_id: str
    agent_name: Optional[str]

    @property
    def sender(self):
        return self.sender_simulation_controller

    @property
    def receiver(self):
        return self.receiver_agent_conductor
