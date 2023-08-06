from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from palaestrai.agent import (
        SensorInformation,
        RewardInformation,
        ActuatorInformation,
    )


@dataclass
class MuscleUpdateRequest:
    """Notifies the :class:`Brain` that a :class:`Muscle` of an action.

    * Sender: A :class:`Muscle` after acting
    * Receiver: The :class:`Brain`

    Parameters
    -----------
    sensors_available: List[SensorInformation]
        List of sensor information on which the muscle
        acted, not the scaled/transformed values which are given to the network
    actuators_available: List[ActuatorInformation]
        A list of actuator information which defined the
        output space of the network, not the values which the network produced
    network_input: List
        A list containing the values which are given to the network
    last_network_output: List
        A list of actions the muscle proposed to do last
    reward: List[RewardInformation]
        Reward received from the last action
    is_terminal: bool
        Indicates whether this was the last action as the
        environment (or agent) are done
    additional_data: dict
        A dictionary containing additional data which has to be
        exchanged between muscle and brain.
    """

    sensors_available: List[SensorInformation]
    actuators_available: List[ActuatorInformation]
    network_input: List
    last_network_output: List
    reward: List[RewardInformation]
    is_terminal: bool
    additional_data: dict
