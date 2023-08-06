"""
This module contains the class :class:`DummyEnvironment`. It could be
used in an experiment for reference purposes.
"""
import random
from typing import List, Callable

from palaestrai.agent import SensorInformation, ActuatorInformation
from palaestrai.types import Discrete, Box
from .environment import Environment
from ..agent.reward_information import RewardInformation


class DummyEnvironment(Environment):
    """
    This class provides a dummy environment with a fixed number of sensors. The
    environment terminates after a fixed number of updates.

    Parameters
    ----------
    connection : broker_connection
        the URI which is used to connect to the simulation broker. It is used
        to communicate with the simulation controller.
    uid : uuid4
        a universal id for the environment
    seed : int
        Seed for recreation
    discrete : bool, optional
        If set to True, the environment will only use discrete spaces.
        Otherwise, the spaces are continuous. Default is `True`.
    """

    def __init__(
        self, uid: str, broker_uri: str, seed: int, discrete: bool = True
    ):
        super().__init__(uid, broker_uri, seed)
        self.iter: int = 0
        self.discrete: bool = discrete

    def start_environment(self):
        """
        This method is called when an `EnvironmentStartRequest` message is
        received. This dummy environment is represented by 10 sensors and
        10 actuators. The sensors are of the type `SensorInformation` and have
        a random value of either 0 or 1, an `observation_space` between 0 and 1
        and an integer number as id.
        The actuators are of the type `ActuatorInformation` and contain a
        setpoint of Discrete(1), an `action_space` of None and an integer
        number as id.

        Returns
        -------
        tuple :
            A list containing the `SensorInformation` for each of the 10
            sensors and a list containing the `ActuatorInformation` for each
            of the 10 actuators.
        """
        self.iter = 0
        sensors = []
        actuators = []
        for num in range(10):
            sensors.append(self._create_sensor(num))
            actuators.append(self._create_actuator(num))
        self.sensors = sensors
        self.actuators = actuators
        return sensors, actuators

    def update(self, actuators):
        """
        This method is called when an `EnvironmentUpdateRequest` message is
        received. While setpoints of the actuators manipulate an actual
        environment, in here those setpoints have no impact on the behavior of
        the dummy environment.
        The state of this dummy environment is represented via random values of
        the `SensorInformation` from the 10 sensors.
        In this dummy environment the reward for the state is a random value of
        either 0 or 1.
        The method returns a list of `SensorInformation`, the random reward and
        the boolean `is_terminal`. After 10 updates the `is_terminal` value is
        set to True which triggers the respective shutdown messages.

        Parameters
        ----------
        actuators : list[`ActuatorInformation`]
            A list of `ActuatorInformation` to interact with the environment.

        Returns
        -------
        tuple :
            A list of `SensorInformation` representing the 10 sensors, the
            reward and boolean for `is_terminal`.

        """

        sensors = []
        for num in range(10):
            sensors.append(self._create_sensor(num))
        reward = [RewardInformation(9000, Discrete(9000), "Reward")]

        if self.iter < 10:
            self.iter += 1
            return sensors, reward, False
        else:
            return sensors, reward, True

    def _create_actuator(self, actuator_id):
        if self.discrete:
            return ActuatorInformation(
                action_space=Discrete(10),
                setpoint=None,
                actuator_id=actuator_id,
            )
        else:
            return ActuatorInformation(
                action_space=Box([0], [10]),
                setpoint=None,
                actuator_id=actuator_id,
            )

    def _create_sensor(self, sensor_id):
        if self.discrete:
            return SensorInformation(
                sensor_value=random.randint(0, 1),
                observation_space=Discrete(2),
                sensor_id=sensor_id,
            )
        else:
            return SensorInformation(
                sensor_value=random.randint(0, 1),
                observation_space=Box([0], [2]),
                sensor_id=sensor_id,
            )
