from dataclasses import dataclass


@dataclass
class EnvironmentSetupRequest:
    """Instructs an :class:`EnvironmentConductor` to initialize
    its :class:`Environment`

    * Sender: :class:`SimulationController`
    * Receiver: :class:`EnvironmentConductor`

    Parameters
    ----------
    sender_simulation_controller_id : str
        The sending :class:`SimulationController`
    receiver_environment_conductor_id : str
        Target :class:`EnvironmentConductor`
    experiment_run_id : str
        ID of the experiment run for which the environment is set up
    experiment_run_instance_id : str
        Instance ID of the ::`ExperimentRun`
    experiment_run_phase : int
        Number of the phase that should be started
    """

    sender_simulation_controller_id: str
    receiver_environment_conductor_id: str

    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int

    @property
    def sender_id(self):
        return self.sender_simulation_controller_id

    @property
    def receiver(self):
        return self.receiver_environment_conductor_id
