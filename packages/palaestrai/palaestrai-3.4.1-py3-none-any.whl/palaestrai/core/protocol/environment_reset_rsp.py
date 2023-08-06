from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, List

from palaestrai.types import SimTime

if TYPE_CHECKING:
    from palaestrai.agent import ActuatorInformation, SensorInformation


@dataclass
class EnvironmentResetResponse:
    """Response to a reset of an :class:`.Environment`.

    Parameters
    ----------
    sender_environment_id: str
        ID of the sending :class:`.Environment`.
    receiver_simulation_controller_id: str
        ID of the receiving :class:`.SimulationController`.
    create_new_instance: bool
        If set to True, the SimulationController will create a new
        instance of the environment.
    sensors: List[SensorInformation]
        List of :class:`.SensorInformation` after the reset. Should
        normally be the same list as after the first start.
    actuators: List[ActuatorInformation]
        List of :class:`.ActuatorInformation` after the reset. Should
        normally be the same list as after the first start.
    simtime: [palaestrai.types.SimTime (default: ``SimTime(simtime_ticks=1)``)
        The current in-simulation time as provided by the environmment
    walltime: The time the message was created, default: datetime.now()
    """

    sender_environment_id: str
    receiver_simulation_controller_id: str
    create_new_instance: bool
    sensors: List[SensorInformation]
    actuators: List[ActuatorInformation]
    simtime: SimTime = SimTime(simtime_ticks=1, simtime_timestamp=None)
    walltime: datetime = datetime.now()

    @property
    def sender(self):
        return self.sender_environment_id

    @property
    def receiver(self):
        return self.receiver_simulation_controller_id
