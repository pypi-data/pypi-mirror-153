import hashlib
import os
import struct
from typing import Union, Optional, Tuple, cast, List

from numpy.random import RandomState


def np_random(seed: Optional[int] = None) -> Tuple[RandomState, int]:
    if seed is not None and not (isinstance(seed, int) and 0 <= seed):
        raise RuntimeError(
            "Seed must be a non-negative integer "
            "or omitted, not {}".format(seed)
        )

    seed = create_seed(seed)

    rng: RandomState = RandomState()
    rng.seed(_int_list_from_bigint(hash_seed(seed)))
    return rng, seed


def hash_seed(seed: Optional[int] = None, max_bytes: int = 8) -> int:
    """Any given evaluation is likely to have many PRNG's active at
    once. (Most commonly, because the environment is running in
    multiple processes.) There's literature indicating that having
    linear correlations between seeds of multiple PRNG's can correlate
    the outputs:

    http://blogs.unity3d.com/2015/01/07/a-primer-on-repeatable-random-numbers/
    http://stackoverflow.com/questions/1554958/how-different-do-random-seeds-need-to-be
    http://dl.acm.org/citation.cfm?id=1276928

    Thus, for sanity we hash the seeds before using them. (This scheme
    is likely not crypto-strength, but it should be good enough to get
    rid of simple correlations.)

    Args:
        seed (Optional[int]): None seeds from an operating system specific randomness source.
        max_bytes: Maximum number of bytes to use in the hashed seed.
    """
    if seed is None:
        seed = create_seed(max_bytes=max_bytes)
    hsh = hashlib.sha512(str(seed).encode("utf8")).digest()
    return _bigint_from_bytes(hsh[:max_bytes])


def create_seed(a: Union[int, str, None] = None, max_bytes: int = 8) -> int:
    """Create a strong random seed. Otherwise, Python 2 would seed using
    the system time, which might be non-robust especially in the
    presence of concurrency.

    Args:
        a (Union[int, str, None]): None seeds from an operating system specific randomness source.
        max_bytes: Maximum number of bytes to use in the seed.
    """
    # Adapted from https://svn.python.org/projects/python/tags/r32/Lib/random.py
    if a is None:
        a = _bigint_from_bytes(os.urandom(max_bytes))
    elif isinstance(a, str):
        try:
            a = int_to_seed(int(a), max_bytes)
        except ValueError:
            a = cast(str, a)
            a_bytes = a.encode("utf8")
            a_bytes = a_bytes + hashlib.sha512(a_bytes).digest()
            a = _bigint_from_bytes(a_bytes[:max_bytes])
    elif isinstance(a, int):
        a = int_to_seed(a, max_bytes)
    else:
        raise RuntimeError("Invalid type for seed: %s (%s)" % (type(a), a))

    return a


def int_to_seed(a: int, max_bytes: int) -> int:
    """Turns integer into a seed.

    Parameters
    ----------
    a           Seed starting point
    max_bytes   Maximum number of bytes to use in the seed

    Returns
    -------
    a           Seed
    """
    a = a % 2 ** (8 * max_bytes)
    return a


def _bigint_from_bytes(bytes_: bytes) -> int:
    sizeof_int = 4
    padding = sizeof_int - len(bytes_) % sizeof_int
    bytes_ += b"\0" * padding
    int_count = int(len(bytes_) / sizeof_int)
    unpacked = struct.unpack("{}I".format(int_count), bytes_)
    accum = 0
    for i, val in enumerate(unpacked):
        accum += 2 ** (sizeof_int * 8 * i) * val
    return accum


def _int_list_from_bigint(bigint: int) -> List[int]:
    # Special case 0
    if bigint < 0:
        raise TypeError("Seed must be non-negative, not {}".format(bigint))
    elif bigint == 0:
        return [0]

    ints = []
    while bigint > 0:
        bigint, mod = divmod(bigint, 2**32)
        ints.append(mod)
    return ints
