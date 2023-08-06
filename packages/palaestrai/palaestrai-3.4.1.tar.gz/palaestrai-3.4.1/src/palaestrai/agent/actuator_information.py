"""This module contains the class :class:`ActuatorInformation` that
stores all information the agents need about an actuator.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from palaestrai.util.exception import OutOfActionSpaceError

if TYPE_CHECKING:
    from palaestrai.types import Space


class ActuatorInformation:
    """Stores information about a single actuator.

    The actuator information class is used to transfer actuator
    information. It can be called to set a new setpoint:

        a = Actuator(some_space)
        a(42)  # a.setpoint is now 42

    Parameters
    ----------
    action_space : :class:`palaestrai.types.Space`
        An instance of a palaestrai space that defines the type of
        the :attr:`setpoint`.
    setpoint : any, optional
        The set value for this actuator. The type is defined by the
        :attr:`action_space`. Can be skipped and set afterwards.
    actuator_id : int or str, optional
        A unique identifier for this actuator. The agents use this ID
        only to assign the setpoints to the correct actuator. The ID
        is not analyzed to gain domain knowledge.
    """

    def __init__(self, setpoint, action_space: Space, actuator_id=None):
        self._setpoint = setpoint
        self.actuator_id = actuator_id
        self.action_space = action_space

    @property
    def setpoint(self):
        return self._setpoint

    @setpoint.setter
    def setpoint(self, setpoint):
        if setpoint is not None and self.action_space is not None:
            try:
                contained = self.action_space.contains(setpoint)
                if not contained:
                    msg = (
                        f"Setpoint '{setpoint}' is not contained "
                        f"within space '{self.action_space}'."
                    )
            except (ValueError, TypeError) as e:
                msg = e.with_traceback
                contained = False

            if not contained:
                raise OutOfActionSpaceError(msg)

            self._setpoint = setpoint

    def flat_setpoint(self, **kwargs):
        """Return a flat vector representation of the setpoint"""
        return self.action_space.to_vector(np.array(self.setpoint), **kwargs)

    def fitting_setpoint(self, **kwargs):
        """Return the setpoint reshaped to the space of the actuator_information object"""
        return self.action_space.reshape_to_space(
            np.array(self.setpoint), **kwargs
        )

    def __call__(self, setpoint):
        self.setpoint = setpoint

    def __repr__(self):
        return (
            "ActuatorInformation("
            "setpoint=%s, action_space=%s, actuator_id=%s)"
            % (self.setpoint, repr(self.action_space), self.actuator_id)
        )

    def __len__(self):
        """The number of values in the action_space"""
        return len(self.action_space)

    @property
    def id(self):
        return self.actuator_id

    @id.setter
    def id(self, value):
        self.actuator_id = value
