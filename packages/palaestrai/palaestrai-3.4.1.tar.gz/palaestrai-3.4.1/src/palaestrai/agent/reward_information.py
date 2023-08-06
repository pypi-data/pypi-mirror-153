"""This module contains the class :class:`RewardInformation` that
stores all information the agents need about a single reward.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from palaestrai.types import Space


class RewardInformation:
    """Stores information about a single reward.

    Once created, a *RewardInformation* object can be called to
    retrieve its value, e.g.,:

        a = RewardInformation(42, some_space)
        a()  # => 42
        a.reward_value  # => 42


    Parameters
    ----------
    reward_value: int float as described in observation_space
        The value of the reward's last reading. The type of this value
        is described by :attr:`observation_space`
    observation_space : :class:`palaestrai.types.Space`
        An instance of a palaestrai space object defining the type of
        the value
    reward_id: str or int, optional
        A unique identifier for this reward. The agents use the ID only
        for assignment of previous values with the same ID. The ID is
        important, if multiple rewards are available and/or the reward
        is a delayed reward.

    """

    def __init__(self, reward_value, observation_space: Space, reward_id=None):
        self.reward_value = reward_value
        self.observation_space = observation_space
        self.reward_id = reward_id

    def __call__(self):
        """Reads the reward"""
        return self.reward_value

    def __add__(self, other):
        return self.reward_value + other

    def __repr__(self):
        return (
            "RewardInformation("
            f"value={self.reward_value}, observation_space="
            f"{repr(self.observation_space)}, reward_id={self.reward_id})"
        )
