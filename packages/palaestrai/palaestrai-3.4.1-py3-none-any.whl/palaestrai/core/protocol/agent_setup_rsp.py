from dataclasses import dataclass


@dataclass
class AgentSetupResponse:
    """Response to a successful agent setup

    * Sender: :class:`AgentConductor`
    * Receiver: :class:`SimulationController`

    Parameters
    ----------
    sender_agent_conductor : str
        ID of the transmitting :class:`AgentConductor`
    receiver_simulation_controller : str
        ID of the receiving :class:`SimulationController`
    experiment_run_id : str
        ID of the current experiment run this environment participates in
    experiment_run_instance_id : str
        ID of the ::`ExperimentRun` object instance
    experiment_run_phase : int
        Current phase number of the experiment run
    agent_id : str
        ID of the respective :class:`Agent` we've just set up (i.e., a
        :class:`Muscle`)
    """

    sender_agent_conductor: str
    receiver_simulation_controller: str
    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int
    agent_id: str

    @property
    def sender(self):
        return self.sender_agent_conductor

    @property
    def receiver(self):
        return self.receiver_simulation_controller
