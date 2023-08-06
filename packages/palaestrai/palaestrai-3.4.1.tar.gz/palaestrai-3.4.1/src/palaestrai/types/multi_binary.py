import re
from typing import Iterable

import numpy as np
from .space import Space


class MultiBinary(Space):
    """A special form of MultiDiscrete for multiple binary values"""

    _RE = re.compile(r"\AMultiBinary\(\s*(?P<inner>\d+)\s*\)\Z")

    def __init__(self, n):
        self.n = n
        super(MultiBinary, self).__init__((self.n,), np.int8)

    def sample(self):
        return self.np_random.randint(
            low=0, high=2, size=self.n, dtype=self.dtype
        )

    def contains(self, x):
        if isinstance(x, list):
            x = np.array(x)  # Promote list to array for contains check
        return (
            ((x == 0) | (x == 1)).all()
            and len(x) == self.n
            and (x.dtype == int)
        )

    def to_vector(self, data: np.ndarray, **kwargs) -> np.ndarray:
        """Represent a given binary data as a flat vector."""
        return data.flatten()

    def reshape_to_space(self, value: Iterable, **kwargs) -> np.ndarray:
        """Turn a list of objects into binary data represented by a list.

        :kwargs: dtype: The dtype of the returned array.
                 default: int
        """
        return np.fromiter(value, kwargs.get("dtype", int), self.n)

    def to_string(self):
        return "MultiBinary(%s)" % self.n

    @classmethod
    def from_string(cls, s):
        match = MultiBinary._RE.match(s)
        if not match or not match["inner"]:
            raise RuntimeError(
                "String '%s' did not match '%s'" % (s, MultiBinary._RE)
            )
        return MultiBinary(int(match["inner"]))

    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return isinstance(other, MultiBinary) and self.n == other.n

    def __len__(self):
        return self.n
