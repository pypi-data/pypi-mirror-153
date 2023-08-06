from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EnvironmentStartRequest:
    """Requests to start an environment

    * Sender: :class:`SimulationController`
    * Receiver: :class:`Environment`

    Attributes
    ----------
    sender_simulation_controller : str
        The ID of the sending :class:`SimulationController` (or a derived
        class)
    receiver_environment : str
        The ID of the receiving :class:`Environment` (or derived a class)
    experiment_run_id : str
        ID of the current experiment run this environment participates in
    experiment_run_instance_id : str
        ID of the ::`ExperimentRun` object instance
    experiment_run_phase : int
        Current phase number of the experiment run
    """

    sender_simulation_controller: str
    receiver_environment: str
    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int

    @property
    def sender(self):
        return self.sender_simulation_controller

    @property
    def receiver(self):
        return self.receiver_environment
