from __future__ import annotations
from typing import List, Tuple, Union

import sys

from palaestrai.agent import (
    RewardInformation,
    SensorInformation,
    ActuatorInformation,
)
from palaestrai.environment import (
    Environment,
    EnvironmentState,
    EnvironmentBaseline,
)
from palaestrai.types import Box, Discrete, SimTime


class CountingEnvironment(Environment):
    """An environment that gives deterministic rewards for end-to-end testing.

    The CountingEnvironment produces one sensor of space ::`Discrete` with
    configuration ``Discrete(2)``, giving the result of ``i % 2``, with
    ``i`` being the current interation. It also prodoces a configurable
    number of actuators. The actuators are named continuously and using them
    yields a reward based on the current iteration and the ID of the actuator.
    Specifically, the  environment will generate `num_actuators` actuators,
    labelled ``Actuator-1``, ``Actuator-2``, etc., with the highest ordinal
    being num_actuators. Triggering the k-th actuator gives a reward equal to
    ``k * setpoint``.

    This way, end-to-end testing from agents to values in the stores can be
    performed.

    Parameters
    ----------
    num_actuators : int
        The number of actuators to create. All actuators have the Space
        ``Discrete(0, 1)``.
    max_iterations : int
        Number of iterations to perform before terminating.
    """

    def __init__(
        self,
        uid: str,
        broker_uri: str,
        seed: int,
        num_actuators: int,
        max_iterations: int,
    ):
        super().__init__(uid, broker_uri, seed)
        self._current_iteration = 0
        self._num_actuators: int = num_actuators
        self._max_iterations: int = max_iterations

    def start_environment(
        self,
    ) -> Union[
        EnvironmentBaseline,
        Tuple[List[SensorInformation], List[ActuatorInformation]],
    ]:
        self._current_iteration = 0
        return EnvironmentBaseline(
            actuators_available=self._make_actuators(),
            sensors_available=[self._make_sensor()],
            simtime=SimTime(
                simtime_ticks=self._current_iteration,
                simtime_timestamp=None,
            ),
        )

    def _make_sensor(self) -> SensorInformation:
        return SensorInformation(
            sensor_id="Sensor-0",
            sensor_value=self._current_iteration % 2,
            observation_space=Discrete(2),
        )

    def _make_actuators(self) -> List[ActuatorInformation]:
        return [
            ActuatorInformation(
                actuator_id="Actuator-%d" % i,
                action_space=Discrete(2),
                setpoint=0,
            )
            for i in range(1, self._num_actuators + 1)
        ]

    def _make_rewards(
        self, setpoints: List[ActuatorInformation]
    ) -> List[RewardInformation]:
        reward_value = sum(
            int(s.setpoint) * int(s.id.split("-")[1]) for s in setpoints
        )
        print(
            ">>> "
            f"At {self._current_iteration}: actuators: {setpoints}: "
            f"reward: {reward_value}",
            file=sys.stderr,
        )
        return [
            RewardInformation(
                reward_value=reward_value,
                observation_space=Box(0, float(reward_value)),
                reward_id="Reward-%d" % self._current_iteration,
            )
        ]

    def update(
        self, actuators: List[ActuatorInformation]
    ) -> Union[
        EnvironmentState,
        Tuple[List[SensorInformation], List[RewardInformation], bool],
    ]:
        self._current_iteration += 1
        return EnvironmentState(
            simtime=SimTime(
                simtime_timestamp=None, simtime_ticks=self._current_iteration
            ),
            rewards=self._make_rewards(actuators),
            sensor_information=[self._make_sensor()],
            done=(self._current_iteration >= self._max_iterations),
        )
