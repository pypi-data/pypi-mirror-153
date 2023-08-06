from palaestrai.agent import RewardInformation
from palaestrai.agent.objective import Objective
from typing import List


class DummyObjective(Objective):
    def __init__(self, params):
        super().__init__(params)

    def internal_reward(self, rewards: List[RewardInformation]):
        final_rewards = []
        for reward in rewards:
            r = reward.reward_value
            final_rewards.append(r)
        return sum(final_rewards)
