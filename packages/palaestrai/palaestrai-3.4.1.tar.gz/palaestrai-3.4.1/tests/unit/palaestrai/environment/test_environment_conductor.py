import unittest
from unittest.mock import AsyncMock, call, patch
from uuid import uuid4

from palaestrai.core.protocol import (
    EnvironmentSetupRequest,
    EnvironmentSetupResponse,
    ShutdownRequest,
    ShutdownResponse,
)
from palaestrai.environment.environment_conductor import EnvironmentConductor


class TestEnvironmentConductor(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.mockaio = patch(
            "palaestrai.environment.environment_conductor.aiomultiprocess."
            "Process",
            spec=True,
        ).start()

        self.addCleanup(patch.stopall)

        self.env_cond = EnvironmentConductor(
            {
                "name": (
                    "palaestrai.environment.dummy_environment:"
                    "DummyEnvironment"
                ),
                "uid": "0815",
                "params": {"discrete": False},
            },
            "test_conn",
            123,
            uuid4(),
        )

    def test_one_process_per_environment(self):
        self.env_cond._init_environment()
        self.env_cond._init_environment()
        self.assertEqual(self.mockaio.call_count, 2)
        self.assertEqual(
            len(self.env_cond._tasks), 2, "not correctly executed"
        )

    async def test_run_shutdown(self):
        msg_shutdown = ShutdownRequest(42)
        self.env_cond.worker.transceive = AsyncMock(return_value=msg_shutdown)

        await self.env_cond.run()
        self.env_cond.worker.transceive.assert_awaited()

    async def test_setup_conductor(self):
        msg_setup = EnvironmentSetupRequest(
            experiment_run_id="run away",
            experiment_run_instance_id="run away instance",
            experiment_run_phase=47,
            receiver_environment_conductor_id="the boss",
            sender_simulation_controller_id="the servant",
        )

        msg_setup_response = EnvironmentSetupResponse(
            sender_environment_conductor=self.env_cond.uid,
            receiver_simulation_controller="the servant",
            environment_id="0815",
            experiment_run_id="run away",
            experiment_run_instance_id="run away instance",
            experiment_run_phase=47,
            environment_type=self.env_cond.env_cfg["name"],
            environment_parameters=self.env_cond.env_cfg["params"],
        )

        msg_shutdown = ShutdownRequest(42)
        msg_shutdown_response = ShutdownResponse(42)

        calls = (
            call(None),
            call(msg_setup_response),
            call(msg_setup_response),
            call(msg_shutdown_response, skip_recv=True),
        )

        self.env_cond.worker.transceive = AsyncMock(
            side_effect=[msg_setup, msg_setup, msg_shutdown, None]
        )

        await self.env_cond.run()
        self.assertEqual(len(self.env_cond._tasks), 2)
        self.env_cond._worker.transceive.assert_has_awaits(calls)


if __name__ == "__main__":
    unittest.main()
