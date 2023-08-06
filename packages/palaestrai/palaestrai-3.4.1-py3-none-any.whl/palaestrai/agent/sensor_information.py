"""This module contains the class :class:`SensorInformation` that
stores all information the agents need about a single sensor.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from palaestrai.types import Space


class SensorInformation:
    """Stores information about a single sensor.

    Once created, a *SensorInformation* object can be called to
    retrieve its value, e.g.,:

        a = SensorInformation(42, some_space)
        a()  # => 42
        a.sensor_value  # => 42


    Parameters
    ----------
    sensor_value: int float as described in observation_space
        The value of the sensor's last reading. The type of this value
        is described by :attr:`observation_space`
    observation_space : :class:`palaestrai.types.Space`
        An instance of a palaestrai space object defining the type of
        the value
    sensor_id: str or int, optional
        A unique identifier for this sensor. The agents use the ID only
        for assignment of previous values with the same ID. The ID is
        not analyzed to gain domain knowledge (e.g., if the sensor is
        called "Powergrid.Bus1", the agent will not use the ID to
        identify this sensor as part of a Bus in a powergrid.)

    """

    def __init__(self, sensor_value, observation_space: Space, sensor_id=None):
        self.sensor_value = sensor_value
        self.observation_space = observation_space
        self.sensor_id = sensor_id

    def __call__(self, **kwargs):
        """Return the sensor_value reshaped to the space of the sensor_information object"""
        return self.fitting_sensor_value(**kwargs)

    def original_sensor_value(self):
        """Return the sensor_value in the form originally provided"""
        return self.sensor_value

    def fitting_sensor_value(self, **kwargs):
        """Return the sensor_value reshaped to the space of the sensor_information object"""
        return self.observation_space.reshape_to_space(
            np.array(self.sensor_value), **kwargs
        )

    def __repr__(self):
        return (
            "SensorInformation("
            f"value={self.sensor_value}, observation_space={repr(self.observation_space)}, sensor_id={self.sensor_id})"
        )

    def __len__(self):
        """The number of values in the observation_space"""
        return len(self.observation_space)

    @property
    def id(self):
        return self.sensor_id

    @id.setter
    def id(self, value):
        self.sensor_id = value
