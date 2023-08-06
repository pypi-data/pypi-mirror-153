"""This module contains the class :class:`Agent` that
stores all information regarding a specific agent.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from . import Brain, Muscle, SensorInformation, ActuatorInformation


@dataclass
class Agent:
    """Stores information about an agent.

    The agent class is used to store information about an
    agent. It is currently used by the simulation controller
    to have a internal representation of all agents.

    Parameters
    ----------
    uid : uuid4
        The uid is used to identify an agent
    brain: :class:`palaestrai.agent.Brain`
        An instance of a palaestrai brain. It
        defines what type of AI is used
    brain_params: dict
        This dictionary contains all parameters needed
        by the brain.
    muscle: :class:`palaestrai.agent.Muscle`
        An instance of a palaestrai muscle. It
        defines what type of AI is used and is linked
        to the type of brain
    muscle_params: dict
        This dictionary contains all parameters needed
        by the muscle.
    sensors: any
        The list of sensors the agent is allowed to
        access.
    actuators: any
        The list of actuators the agent is allowed to
        access.
    """

    uid: str
    brain: Brain
    brain_params: dict
    muscle: Muscle
    muscle_params: dict
    sensors: List[SensorInformation]
    actuators: List[ActuatorInformation]
