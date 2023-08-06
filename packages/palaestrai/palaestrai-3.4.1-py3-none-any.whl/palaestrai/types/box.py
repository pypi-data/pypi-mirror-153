import ast
import logging
import numbers
import re
from typing import Iterable

import numpy as np

from palaestrai.util.dynaloader import locate
from .space import Space

LOG = logging.getLogger("palaestrai.types")


class Box(Space):
    """A box in R^n, i.e.each coordinate is bounded.

    There are two common use cases:

    * Identical bound for each dimension::
        >>> Box(low=-1.0, high=2.0, shape=(3, 4), dtype=np.float32)
        Box(3, 4)

    * Independent bound for each dimension::
        >>> Box(low=np.array([-1.0, -2.0]), high=np.array([2.0, 4.0]), dtype=np.float32)
        Box(2,)

    """

    _BOX_RE = re.compile(r"\A\s*?Box\((.+)\)\s*\Z")
    _SHAPE_RE = re.compile(r"shape=\(((\d+, ?)|((\d+, ?)+\d+ ?))\)")
    _DTYPE_RE = re.compile(r"dtype=(np\.)?(\w+)")
    _LOW_BOUNDARY_RE = re.compile(
        r"low=((?P<single>[0-9.-]+)|(?P<list>\[[^a-zA-Z]*\]))"
    )
    _HIGH_BOUNDARY_RE = re.compile(
        r"high=((?P<single>[0-9.-]+)|(?P<list>\[[^a-zA-Z]*\]))"
    )

    def __init__(self, low, high, shape=None, dtype=np.float32):
        assert dtype is not None, "dtype must be explicitly provided. "
        self.dtype = np.dtype(dtype)

        if shape is None:
            if np.array(low).shape != np.array(high).shape:
                raise ValueError("low and high shapes are not compatible")
            self.shape = np.array(low).shape
            self.low = low
            self.high = high
        else:
            self.shape = tuple(shape)

        if isinstance(low, numbers.Number) and isinstance(
            high, numbers.Number
        ):
            self.low = np.full(self.shape, low)
            self.high = np.full(self.shape, high)
        else:
            if hasattr(low, "__iter__"):
                self.low = np.array(low)
            else:
                raise ValueError(
                    "Incompatible type '%s' for lower boundary" % type(low)
                )
            if hasattr(high, "__iter__"):
                self.high = np.array(high)
            else:
                raise ValueError(
                    "Incompatible type '%s' for higher boundary" % type(high)
                )

        self.low = self.low.astype(self.dtype)
        self.high = self.high.astype(self.dtype)
        super(Box, self).__init__(self.shape, self.dtype)

    def sample(self):
        high = (
            self.high
            if self.dtype.kind == "f"
            else self.high.astype("int64") + 1
        )
        return self.np_random.uniform(
            low=self.low, high=high, size=self.shape
        ).astype(self.dtype)

    def contains(self, x) -> bool:
        if not isinstance(x, np.ndarray):
            x = np.asarray(x, dtype=self.dtype)

        return bool(
            np.can_cast(x.dtype, self.dtype)
            and x.shape == self.shape
            and np.all(x >= self.low)
            and np.all(x <= self.high)
        )

    def to_string(self):
        return "Box(low=%s, high=%s, shape=%s, dtype=np.%s)" % (
            self.low.tolist(),
            self.high.tolist(),
            self.shape,
            self.dtype,
        )

    @classmethod
    def from_string(cls, s):
        complete_match = Box._BOX_RE.match(s)
        if not complete_match:
            raise RuntimeError(
                "String '%s' does not match '%s'" % (s, Box._BOX_RE)
            )
        inner_str = complete_match[1]

        list_split_re = re.compile(r",\s*|\s+")

        lower_boundary_match = Box._LOW_BOUNDARY_RE.search(inner_str)
        if not lower_boundary_match:
            raise RuntimeError(
                "No lower boundary in '%s' (%s)" % (s, Box._LOW_BOUNDARY_RE)
            )
        lower = None
        if lower_boundary_match["single"]:
            lower = float(lower_boundary_match["single"])
        else:  # list
            lower = np.array(ast.literal_eval(lower_boundary_match["list"]))

        higher_boundary_match = Box._HIGH_BOUNDARY_RE.search(inner_str)
        if not higher_boundary_match:
            raise RuntimeError(
                "No higher boundary in '%s' (%s)" % (s, Box._HIGH_BOUNDARY_RE)
            )
        higher = None
        if higher_boundary_match["single"]:
            higher = float(higher_boundary_match["single"])
        else:  # list
            higher = np.array(ast.literal_eval(higher_boundary_match["list"]))

        shape = None
        if not type(higher) is np.ndarray:
            shape_match = Box._SHAPE_RE.search(inner_str)
            if not shape_match:
                raise RuntimeError(
                    "No or invalid shape in '%s' ('%s')"
                    % (inner_str, Box._SHAPE_RE)
                )
            shape = tuple(
                [
                    int(i)
                    for i in shape_match[1].replace(" ", "").split(",")
                    if i
                ]
            )

        dtype_match = Box._DTYPE_RE.search(inner_str)
        if not dtype_match:
            raise RuntimeError(
                "No or invalid dtype in '%s' (pattern '%s')"
                % (inner_str, Box._DTYPE_RE)
            )
        dtype = locate("numpy.%s" % dtype_match[2])

        return Box(low=lower, high=higher, shape=shape, dtype=dtype)

    def to_vector(self, data: np.ndarray, **kwargs) -> np.ndarray:
        """Flattens the data to a 1d array"""
        if not data.shape == self.shape:
            LOG.warning(
                "Box received data to flatten of shape %s while having shape %s",
                data.shape,
                self.shape,
            )
        return data.flatten()

    def reshape_to_space(self, value: Iterable, **kwargs) -> np.ndarray:
        """Reshape the data into the shape a the space"""
        return np.reshape(np.array(value), self.shape)

    def __eq__(self, other):
        return (
            isinstance(other, Box)
            and (self.shape == other.shape)
            and np.allclose(self.low, other.low)
            and np.allclose(self.high, other.high)
        )

    def __len__(self):
        return np.prod(self.shape)
