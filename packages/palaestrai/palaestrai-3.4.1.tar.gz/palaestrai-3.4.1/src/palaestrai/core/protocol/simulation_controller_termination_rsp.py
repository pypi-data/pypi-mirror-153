from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class SimulationControllerTerminationResponse:
    """Acknowledges the termination of a :py:class:`SimulationController`.

    * Sender: :py:class:`RunGovernor`
    * Receiver: :py:class:`SimulationController`

    Attributes
    ----------
    sender_run_governor_id : str
        Opaque ID of the sending :py:class:`RunGovernor` instance
    receiver_simulation_controller_id : str
        Opaque ID of the receiving :py:class:`SimulationController` instance
    experiment_run_id : str
        ID of the experiment run the agent participates in
    experiment_run_instance_id : str
        ID of the ::`ExperimentRun` object instance
    experiment_run_phase : int
        Current phase number of the experiment run
    restart : bool
        If ``True``, more episodes in the current experiment run phase are
        scheduled.
    complete_shutdown : bool
        If ``True``, the message indicates that the
        :py:class:`RunGovernor` is now shutting down the whole run.
    """

    sender_run_governor_id: str
    receiver_simulation_controller_id: str
    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int
    restart: bool
    complete_shutdown: bool

    @property
    def sender(self):
        return self.sender_run_governor_id

    @property
    def receiver(self):
        return self.receiver_simulation_controller_id
