from __future__ import annotations
from dataclasses import dataclass

# from typing import TYPE_CHECKING


@dataclass
class MuscleShutdownResponse:
    """Responds after a :class:`palaestrai.agent.Muscle` sent a
    :class:`.MuscleShutdownRequest` to the :class:`palaestrai.agent.Brain`.

    """
