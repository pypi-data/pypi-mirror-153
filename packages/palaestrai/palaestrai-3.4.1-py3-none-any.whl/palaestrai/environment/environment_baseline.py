"""Defines the initial state (baseline) of an  initialized ::`Environment`."""

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, List

from palaestrai.types import SimTime

if TYPE_CHECKING:
    from palaestrai.agent import SensorInformation, ActuatorInformation


@dataclasses.dataclass
class EnvironmentBaseline:
    """An :class:`~Environment`'s baseline after initializing

    This data class contains data about an environment after it has been
    started, but no actor has acted yet. It contains the sensors/actuator
    available, initial values for sensors, as well as the starting time in
    the environment.

    Attributes
    ----------
    sensors_available : List[SensorInformation]
        Sensors available in the environment, along with initial readings
    actuators_available : List[ActuatorInformation]
        Actuators available
    simtime: palaestrai.types.SimTime (default: SimTime(simtime_ticks=1))
        Environment starting time
    """

    sensors_available: List[SensorInformation]
    actuators_available: List[ActuatorInformation]
    simtime: SimTime = SimTime(simtime_ticks=1, simtime_timestamp=None)
