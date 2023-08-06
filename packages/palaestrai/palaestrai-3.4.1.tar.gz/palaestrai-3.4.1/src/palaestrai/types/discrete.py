import re
from typing import Any

import numpy as np
from .space import Space


class Discrete(Space):
    """A discrete space in :math:`\{ 0, 1, \dots, n-1 \}`.

    Example::

        >>> Discrete(2)

    """

    _RE = re.compile(r"\A\s*?Discrete\((\d+)\)\s*\Z")

    def __init__(self, n):
        assert n >= 0
        self.n = n
        super(Discrete, self).__init__((), np.int64)

    def sample(self):
        return self.np_random.randint(self.n)

    def contains(self, x):
        if isinstance(x, int):
            as_int = x
        elif isinstance(x, (np.generic, np.ndarray)) and (
            x.dtype.kind in np.typecodes["AllInteger"] and x.shape == ()
        ):
            as_int = int(x)
        else:
            raise TypeError(
                f"Expected int, numpy.generic or numpy.ndarray got {type(x)} instead"
            )
        return as_int >= 0 and as_int < self.n

    def to_vector(self, data: np.ndarray, **kwargs) -> np.ndarray:
        """Flatten the discrete data to a ndarray of size self.n"""
        assert (
            data.shape == (1,) or data.shape == 1 or data.shape == ()
        ), f"Expected shape (1,) or 1 or (); Got {data.shape} instead"
        transformed = np.zeros(self.n)
        transformed[data.item()] = 1
        return np.array(transformed)

    def reshape_to_space(self, value: Any, **kwargs) -> np.ndarray:
        """Reshape the flat representation of data into a single number

        :kwargs: dtype: The dtype of the returned array.
                        default: float
        """
        if np.isscalar(value) or np.ndim(value) == 0:
            return np.array([value])
        as_array = np.fromiter(value, kwargs.get("dtype", float), self.n)
        assert (
            len(as_array) == self.n
        ), f"Expected {self.n} data points; Got {len(as_array)} instead"
        return np.array(as_array.argmax())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return f"Discrete({self.n})"

    @classmethod
    def from_string(cls, s):
        match = Discrete._RE.match(s)
        if not match or not match[1]:
            raise RuntimeError(
                "String '%s' did not match '%s'" % (s, Discrete._RE)
            )
        return Discrete(int(match[1]))

    def __eq__(self, other):
        return isinstance(other, Discrete) and self.n == other.n

    def __len__(self):
        return self.n
