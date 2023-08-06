import numpy as np
import warnings

from palaestrai.types import Box
from palaestrai.types import Discrete
from palaestrai.types import MultiDiscrete
from palaestrai.types import MultiBinary
from palaestrai.types import Tuple


def flatdim(space):
    warnings.warn(
        "flatdim is deprecated use len(*information) or len(space) instead.",
        DeprecationWarning,
    )
    if isinstance(space, Box):
        return int(np.prod(space.shape))
    elif isinstance(space, Discrete):
        return int(space.n)
    elif isinstance(space, Tuple):
        return int(sum([flatdim(s) for s in space.spaces]))
    elif isinstance(space, MultiBinary):
        return int(space.n)
    elif isinstance(space, MultiDiscrete):
        return int(np.prod(space.shape))
    else:
        raise NotImplementedError


def flatten(space, x):
    warnings.warn(
        "flatten is deprecated use *information.flat_setpoint or space.flatten instead.",
        DeprecationWarning,
    )
    if isinstance(space, Box):
        return np.asarray(x, dtype=np.float32).flatten()
    elif isinstance(space, Discrete):
        onehot = np.zeros(space.n, dtype=np.float32)
        onehot[x] = 1.0
        return onehot
    elif isinstance(space, Tuple):
        return np.concatenate(
            [flatten(s, x_part) for x_part, s in zip(x, space.spaces)]
        )
    elif isinstance(space, MultiBinary):
        return np.asarray(x).flatten()
    elif isinstance(space, MultiDiscrete):
        onehot = np.zeros(np.sum(space.nvec), dtype=np.float32)
        xj = 0
        for xi, si in zip(x, space.nvec):
            onehot[xi + xj] = 1.0
            xj = xj + si
        return onehot
    else:
        raise NotImplementedError


def unflatten(space, x):
    warnings.warn(
        "unflatten is deprecated use *information.fitting_setpoint or space.reshape_to_space instead.",
        DeprecationWarning,
    )
    if isinstance(space, Box):
        return np.asarray(x, dtype=np.float32).reshape(space.shape)
    elif isinstance(space, Discrete):
        return int(np.nonzero(x)[0][0])
    elif isinstance(space, Tuple):
        dims = [flatdim(s) for s in space.spaces]
        list_flattened = np.split(x, np.cumsum(dims)[:-1])
        list_unflattened = [
            unflatten(s, flattened)
            for flattened, s in zip(list_flattened, space.spaces)
        ]
        return tuple(list_unflattened)
    elif isinstance(space, MultiBinary):
        return np.asarray(x).reshape(space.shape)
    elif isinstance(space, MultiDiscrete):
        result = []
        s = 0
        for si in space.nvec:
            for xi in range(s, s + si):
                if x[xi] == 1.0:
                    result.append(xi - s)
            s = s + si
        if space.nvec.shape == np.array(result).shape:
            return result
    else:
        raise NotImplementedError
