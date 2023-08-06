"""This module contains the abstract baseclass :class:`.Objective`,
from which all other objectives should be derived.

"""
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from . import RewardInformation


class Objective(ABC):
    """The base class for all objectives.

    An objective defines the goal of an agent and changing the
    objective can, e.g., transform an attacker agent to a defender
    agent.

    The objective can, e.g., a wrapper for the reward of the
    environment and, in the easiest case, the sign of the reward
    is flipped (or not) to define attacker or defender. However, the
    objective can as well use a complete different
    formula.

    """

    def __init__(self, params: dict):
        self.params = params

    @abstractmethod
    def internal_reward(self, rewards: List["RewardInformation"]) -> float:
        """Calculate the reward of this objective."""
        raise NotImplementedError
