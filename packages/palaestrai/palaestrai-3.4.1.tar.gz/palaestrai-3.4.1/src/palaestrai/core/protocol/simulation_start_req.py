from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class SimulationStartRequest:
    """Requests a :class:`SimulationController` to start a simulation run.

    * Sender: The ::`RunGovernor` that is the parent of the adressed
        ::`SimulationController` and that requests the next run.
    * Receiver: The ::`SimulationController` that should execute the run

    Parameters
    ----------
    sender_run_governor_id : str
        ID of the ::`RunGovernor` that requests the start of the simulation
        run.
    receiver_simulation_controller_id : str
        The receiving ::`SimulationController`
    experiment_run_id : str
        ID of the ::`ExperimentRun` whose next phase should be executed
    experiment_run_instance_id : str
        Instance ID of the ::`ExperimentRun`
    experiment_run_phase : int
        Number of the phase that should be started
    experiment_run_phase_id : str
        Identifying name (unique ID) of the experiment run phase
    experiment_run_phase_configuration : Dict
        Configuration parameters of the phase (e.g., mode, episodes, etc.)
    """

    sender_run_governor_id: str
    receiver_simulation_controller_id: str
    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int
    experiment_run_phase_id: str
    experiment_run_phase_configuration: Dict

    @property
    def sender(self):
        return self.sender_run_governor_id

    @property
    def receiver(self):
        return self.receiver_simulation_controller_id
