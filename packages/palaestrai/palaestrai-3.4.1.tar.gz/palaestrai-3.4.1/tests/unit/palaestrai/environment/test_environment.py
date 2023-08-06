import unittest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from palaestrai.agent import (
    SensorInformation,
    ActuatorInformation,
    RewardInformation,
)
from palaestrai.core.protocol import (
    EnvironmentShutdownRequest,
    EnvironmentShutdownResponse,
    EnvironmentStartRequest,
    EnvironmentStartResponse,
    EnvironmentUpdateRequest,
    EnvironmentUpdateResponse,
    EnvironmentResetRequest,
    EnvironmentResetResponse,
)
from palaestrai.environment.dummy_environment import DummyEnvironment
from palaestrai.types import Discrete


class TestEnvironment(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.env = DummyEnvironment(
            uid=str(uuid4()),
            broker_uri="test://connection",
            seed=123,
            discrete=False,
        )
        self.setup_req = EnvironmentStartRequest(
            sender_simulation_controller="sc-0",
            receiver_environment="0",
            experiment_run_id="1",
            experiment_run_instance_id="inst-0",
            experiment_run_phase=0,
        )
        self.update_req = EnvironmentUpdateRequest(
            experiment_run_instance_id="HelloFooBar",
            experiment_run_phase=47,
            sender_simulation_controller="2",
            receiver_environment="0",
            experiment_run_id="1",
            actuators=list(),
        )
        self.shutdown_req = EnvironmentShutdownRequest(
            experiment_run_id="1", environment_id="0"
        )
        self.reset_req = EnvironmentResetRequest("0", "1")
        # self.reset_rsp = EnvironmentResetResponse("0")

    def test_handle_setup(self):
        self.env.start_environment = MagicMock(
            return_value=(
                [SensorInformation(0, Discrete(1), "0")],
                [ActuatorInformation(0, Discrete(1), "0")],
            )
        )
        rsp = self.env._handle_setup(self.setup_req)

        self.env.start_environment.assert_called_once()
        self.assertIsInstance(rsp, EnvironmentStartResponse)
        self.assertTrue(all(self.env.uid in x.id for x in rsp.sensors))
        self.assertTrue(all(self.env.uid in x.id for x in rsp.actuators))

    def test_handle_update(self):
        self.env.update = MagicMock(
            return_value=(
                [SensorInformation(0, Discrete(1), "0")],
                [RewardInformation(0, Discrete(1), "0")],
                False,
                None,
            )
        )
        rsp = self.env._handle_update(self.update_req)

        self.env.update.assert_called_once()
        self.assertIsInstance(rsp, EnvironmentUpdateResponse)
        self.assertTrue(all(self.env.uid in x.id for x in rsp.sensors))

    def test_handle_shutdown(self):
        self.env.shutdown = MagicMock(return_value=True)
        rsp = self.env._handle_shutdown(self.shutdown_req)

        self.env.shutdown.assert_called_once()
        self.assertIsInstance(rsp, EnvironmentShutdownResponse)

    def test_handle_reset(self):
        self.env.shutdown = MagicMock()
        self.env.start_environment = MagicMock(
            return_value=(
                [SensorInformation(0, Discrete(1), "0")],
                [ActuatorInformation(0, Discrete(1), "0")],
            )
        )
        result = self.env._handle_reset(self.reset_req)

        self.assertIsInstance(result, EnvironmentResetResponse)
        self.assertTrue(all(self.env.uid in x.id for x in result.sensors))
        self.assertTrue(all(self.env.uid in x.id for x in result.actuators))

        self.env.shutdown.assert_called_once()
        self.env.start_environment.assert_called_once()

    async def test_run(self):
        setup_msg = self.setup_req
        update_msg = self.update_req
        shutdown_msg = self.shutdown_req
        self.env.worker.transceive = AsyncMock()
        self.env.worker.transceive.side_effect = [
            setup_msg,
            update_msg,
            update_msg,
            update_msg,
            shutdown_msg,
            shutdown_msg,  # Final message, will not be handled
        ]
        self.env.start_environment = MagicMock(return_value=(list(), list()))
        self.env.update = MagicMock(return_value=(list(), list(), False))
        await self.env.run()

        self.assertEqual(self.env.worker.transceive.call_count, 6)
        self.env.start_environment.assert_called_once()
        self.assertEqual(self.env.update.call_count, 3)

    def test_remove_uuid_correct(self):
        actuator1 = ActuatorInformation(
            1, Discrete(2), "Test1.Power.dontcare1"
        )
        actuator2 = ActuatorInformation(
            2, Discrete(2), "Test1.Power.dontcare2"
        )
        a_list = [actuator1, actuator2]
        self.env._remove_uid(a_list)

        self.assertEqual(a_list[0].actuator_id, "Power.dontcare1")
        self.assertEqual(a_list[1].actuator_id, "Power.dontcare2")


if __name__ == "__main__":
    unittest.main()
