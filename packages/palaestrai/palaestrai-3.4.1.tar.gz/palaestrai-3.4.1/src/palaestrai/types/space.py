import re
from abc import ABC, abstractmethod
from collections import Iterable

import numpy as np

from palaestrai.util import seeding
from palaestrai.util.dynaloader import locate


class CanNotConvertException(Exception):
    pass


class Space(ABC):
    """Base class for space definitions

    Derived classes allow a minimal mathematical representation of a space
    concept.
    """

    _SPACENAME_RE = re.compile(r"\A\s*?(\w+)\(([^;]+)\)\s*\Z")
    TYPES = [
        "Box",
        "Dict",
        "Discrete",
        "MultiBinary",
        "MultiDiscrete",
        "Tuple",
    ]

    def __init__(self, shape=None, dtype=None):
        self.shape = None if shape is None else tuple(shape)
        self.dtype = None if dtype is None else np.dtype(dtype)
        self.np_random = None
        self.seed()

    @abstractmethod
    def sample(self):
        """Uniformly randomly sample a random element of this space."""
        pass

    def seed(self, seed=None):
        """Seed the PRNG of this space."""
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    @abstractmethod
    def contains(self, x):
        """Return ``True`` if the value given is a valid member of the space.

        :param x: Any value

        :return: True iff ``x`` is a member of the space
        """

        pass

    def __contains__(self, x):
        return self.contains(x)

    @abstractmethod
    def to_vector(self, data: np.ndarray, **kwargs) -> np.ndarray:
        """Return a flat numpy array of data provided in the shape of the space.

        Should give a warning if the shape of the data is unexpected.

        :param data: The data to be transformed

        :return: The data represented in a flat list
        """
        pass

    @abstractmethod
    def reshape_to_space(self, value: Iterable, **kwargs) -> np.ndarray:
        """Return a list of data in the form of the space

        Should raise a CanNotConvertException if the values can not be converted

        :param value: The values to be represented

        :return: The values in the form of the space
        """
        pass

    @abstractmethod
    def to_string(self):
        """Returns the string representation of the space object.

        String representations of space objects must read like a Python
        constructor, such as ``Box(low=[1.0, 0.0], high=[42.0, 42.42])``. The
        name of the class is used to dynamically construct a new object from a
        string representation.

        :return: The object's string representation.
        """

        pass

    @classmethod
    def from_string(cls, s):
        """Dynamically constructs any descendant space object from a string.

        On the :py:class:`Space` class, this method acts as a factory to
        construct any known descrendant module from a string representation.
        It dynamically locates and instantiates any module that is listed in
        :py:data:`Space.TYPES`.

        All descendant types must also implement this class method as an
        alternative constructor (the known ones do). I.e., you can use
        ``palaestrai.types.Discrete.from_string("Discrete(2)")`` as well as
        ``palaestrai.types.Space.from_string("Discrete(2)")``.

        :param str s: The string representation of a space object.
        """

        if cls != Space:
            raise NotImplementedError()

        m = Space._SPACENAME_RE.match(s)
        classname = m[1] if m else None

        if not classname:
            raise RuntimeError(
                "String '%s' did not match pattern '%s'"
                % (s, Space._SPACENAME_RE)
            )
        if not classname in Space.TYPES:
            raise RuntimeError("Unknown type: palaestrai.types.%s" % classname)

        classpath = "palaestrai.types.%s" % classname
        cls = locate(classpath)
        return cls.from_string(s)

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    @abstractmethod
    def __len__(self):
        """The number of values in the space"""
        pass
