from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from palaestrai.types import SimTime
    from palaestrai.agent import SensorInformation, RewardInformation


@dataclasses.dataclass
class EnvironmentState:
    """Describes the current state of an :class:`~Environment`.

    This dataclass is used as return value of the :meth:`~Environment.update()`
    method. It contains current sensor readings, reward of the environment,
    indicates whether the environment has terminated or not, and finally gives
    time information.

    Attributes
    ----------

    sensor_information : List[SensorInformation]
        List of current sensor values after evaluating the environment
    rewards : List[RewardInformation]
        Current rewards given from the environment
    done : bool
        Whether the environment has terminated (``True``) or not (``False``)
    simtime: SimTime (default: None)
        Environment starting time
    """

    sensor_information: List[SensorInformation]
    rewards: List[RewardInformation]
    done: bool
    simtime: Optional[SimTime] = None
