from dataclasses import dataclass
from typing import Any


@dataclass
class SimulationControllerTerminationRequest:
    """Announces that a :py:class:`SimulationController` has exited

    * Sender: :py:class:`SimulationController`
    * Receiver: :py:class:`RunGovernor`

    :param sender_simulation_controller_id: Opaque ID of the sending
        :py:class:`SimulationController` instance
    :param receiver_run_governor_id: Opaque ID of the receiving
        :py:class:`RunGovernor` instance
    :param experiment_run_id: Opaque ID of an experiment run
    :param environment_terminated: `True` if the environment terminated the
        run, `False` if something else (e.g., agent reset) issued the
        termination of the simulation run.
    :param additional_results: Any additional results the simulation
        communicates to the :py:class:`RunGovernor`, e.g., for a
        :py:class:`TerminationCondition`
    :param last_reward: Last reward issued in the simulation
    """

    sender_simulation_controller_id: str
    receiver_run_governor_id: str
    experiment_run_id: str
    environment_terminated: bool
    additional_results: Any
    last_reward: Any

    @property
    def sender(self):
        return self.sender_simulation_controller_id

    @property
    def receiver(self):
        return self.receiver_run_governor_id
