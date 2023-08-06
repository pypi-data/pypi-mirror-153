from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import RunGovernor


class RunGovernorState(ABC):
    """The base class for all run governor states.

    Parameters
    ----------
    rgc: :class:`.RunGovernor`
        The run governor that provides the context for this state.
        Therefore, the abbreviation rgc (run governor context)
    name: str
        The name of this state.

    """

    def __init__(self, rgc: RunGovernor, name: str):
        self.rgc = rgc
        self.name = name

    @abstractmethod
    async def run(self) -> None:
        """The main function of this state.

        All commands of this state should be executed here. The last
        command should be :meth:`next_state` to initialize the
        transition to the following state.

        """
        pass

    @abstractmethod
    def next_state(self) -> None:
        """Transition to the next state.

        Based on the outcome of the :meth:`run` method, the next state
        should be determined in this function.
        """
        pass

    def add_error(self, error: Exception) -> None:
        """Add an error to the error list of the run governor.

        Parameters
        ----------
        error: Exception
            The error that raised, catched, and should be saved for
            error handling.

        """
        self.rgc.errors.append((error, self.name))
