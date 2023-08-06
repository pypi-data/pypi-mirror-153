from dataclasses import dataclass


@dataclass
class EnvironmentSetupResponse:
    """Signals successful environment setup and delivers environment parameters

    * Sender: :class:`EnvironmentConductor´
    * Receiver: :class:`SimulationController`

    Parameters
    ----------
    sender_environment_conductor : str
        ID of the sending :class:`EnvironmentConductor`
    receiver_simulation_controller: str
        ID of the receiving :class:`SimulationController`
    experiment_run_id : str
        ID of the ::`ExperimentRun` whose next phase should be executed
    experiment_run_instance_id : str
        Instance ID of the ::`ExperimentRun`
    phase : int
        Number of the phase that should be started
    environment_id : str
        ID of the newly setup environment
    environment_parameters: dict
        All parameters that describe the environment that has just been set up
    """

    environment_id: str
    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int
    sender_environment_conductor: str
    receiver_simulation_controller: str
    environment_type: str
    environment_parameters: dict

    @property
    def sender(self):
        return self.sender_environment_conductor

    @property
    def receiver(self):
        return self.receiver_simulation_controller
