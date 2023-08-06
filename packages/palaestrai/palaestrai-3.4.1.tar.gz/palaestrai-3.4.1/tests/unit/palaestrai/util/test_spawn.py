import unittest

import aiomultiprocess

from palaestrai.core import RuntimeConfig
from palaestrai.util import spawn_wrapper


def _dummy_spawn_target(x=0, y=0):
    c = RuntimeConfig()
    if c.store_uri != "bar":
        exit(5)
    exit(x + y)


async def _async_dummy_spawn_target(x=0, y=0):
    return _dummy_spawn_target(x, y)


class SpawnTest(unittest.IsolatedAsyncioTestCase):
    async def test_spawn_wrapper(self):
        RuntimeConfig()._store_uri = "bar"
        p = aiomultiprocess.Process(
            target=spawn_wrapper,
            args=(
                __name__,
                RuntimeConfig().to_dict(),
                _dummy_spawn_target,
            ),
        )
        p.start()
        await p.join()
        self.assertEqual(p.exitcode, 0)

    async def test_spawn_wrapper_no_args(self):
        RuntimeConfig()._store_uri = "bar"
        p = aiomultiprocess.Process(
            target=spawn_wrapper,
            args=(
                __name__,
                RuntimeConfig().to_dict(),
                _dummy_spawn_target,
                [5],
                {"y": 37},
            ),
        )
        p.start()
        await p.join()
        self.assertEqual(p.exitcode, 42)

    async def test_spawn_wrapper_coroutine(self):
        RuntimeConfig()._store_uri = "bar"
        p = aiomultiprocess.Process(
            target=spawn_wrapper,
            args=(
                __name__,
                RuntimeConfig().to_dict(),
                _async_dummy_spawn_target,
                [5],
                {"y": 37},
            ),
        )
        p.start()
        await p.join()
        self.assertEqual(p.exitcode, 42)


if __name__ == "__main__":
    unittest.main()
