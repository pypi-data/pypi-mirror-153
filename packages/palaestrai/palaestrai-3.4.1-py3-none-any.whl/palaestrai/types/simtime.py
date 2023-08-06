from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class SimTime:
    """Variable representation of a point in time in any environment

    This class represents points in time within a simulated environment. It
    allows to express two distinct scales of measurement: Ticks and actual
    datetime objects.

    *Ticks* are a certain step (‘tick’) of a simulation. They are an abstract
    measure for advancement of a simulation and can refer to anything, such as
    events executed, etc. They have to be monotonically increasing, though.

    *Timestamps* are actual :class:`datetime.datetime` objects referring to a
    certain point of simulated time.
    """

    simtime_ticks: Optional[int]
    simtime_timestamp: Optional[datetime]
