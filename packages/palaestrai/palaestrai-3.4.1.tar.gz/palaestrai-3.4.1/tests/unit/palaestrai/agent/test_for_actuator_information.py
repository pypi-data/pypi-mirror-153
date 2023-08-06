import unittest

import numpy as np
from palaestrai.agent import ActuatorInformation
from palaestrai.types import Box, Discrete, MultiBinary, MultiDiscrete, Tuple
from palaestrai.util.exception import OutOfActionSpaceError


class TestActuatorInformation(unittest.TestCase):
    def setUp(self):
        self.test_box1 = Box(0.0, 10.0, shape=(1,), dtype=np.float32)
        self.test_box2 = Box(
            low=np.array([0.0, -10.0]),
            high=np.array([1.0, 0.0]),
            dtype=np.float32,
        )
        self.test_box3 = Box(
            low=-1.0, high=2.0, shape=(3, 4), dtype=np.float32
        )
        self.test_discrete = Discrete(10)
        self.test_multidiscrete = MultiDiscrete([5, 4, 2])
        self.test_multibinary = MultiBinary(3)

    def test_call_actuator(self):
        act = ActuatorInformation(
            setpoint=None, action_space=self.test_box1, actuator_id="Test"
        )
        act([5.0])

        val = act.setpoint
        self.assertIsInstance(val, list)
        self.assertEqual(val, [5.0])

    def test_set_one_dim_box(self):
        act = ActuatorInformation(
            setpoint=None, action_space=self.test_box1, actuator_id="Test"
        )

        # Not contained within the space
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [15.0]
        self.assertIsNone(act.setpoint)

        # Wrong dimensions
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [5, 5]
        self.assertIsNone(act.setpoint)

        act.setpoint = [5.0]
        self.assertIsInstance(act.setpoint, list)
        self.assertEqual(act.setpoint, [5.0])

    def test_set_two_dim_box(self):
        act = ActuatorInformation(
            setpoint=None, action_space=self.test_box2, actuator_id="Test"
        )

        # Wrong dimensions
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = 0.5
        self.assertIsNone(act.setpoint)

        # Not within the space
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [-1, -5]
        self.assertIsNone(act.setpoint)

        act.setpoint = [0, -10]
        self.assertIsInstance(act.setpoint, list)

    def test_set_multi_dim_box(self):
        act = ActuatorInformation(
            setpoint=None, action_space=self.test_box3, actuator_id="Test"
        )

        # Wrong dimensions
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [0.0]
        self.assertIsNone(act.setpoint)

        # Not within the space
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [-2.0, 0.0, 0.0, 0.0],
            ]
        self.assertIsNone(act.setpoint)

        act.setpoint = [
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ]
        self.assertIsInstance(act.setpoint, list)
        for sublist in act.setpoint:
            self.assertIsInstance(sublist, list)
            for val in sublist:
                self.assertIsInstance(val, float)

    def test_set_discrete(self):
        act = ActuatorInformation(
            setpoint=None, action_space=self.test_discrete, actuator_id="Test"
        )

        # Wrong dimensions
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [5, 5]

        # Not within the space
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = -1

        # Wrong dtype
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = 5.0

        act.setpoint = 5

    def test_set_multi_discrete(self):
        act = ActuatorInformation(None, self.test_multidiscrete, "Test")

        # Wrong dimensions
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [1, 1]

        # Not within the space
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [5, 4, 3]

        # Wrong dtype (should probably fail)
        # with self.assertRaises(OutOfActionSpaceError):
        act.setpoint = [3, 3, 1.0]

        act.setpoint = [1, 1, 1]
        self.assertIsInstance(act.setpoint, list)
        for val in act.setpoint:
            self.assertIsInstance(val, int)

    def test_set_multi_binary(self):
        act = ActuatorInformation(None, self.test_multibinary, "Test")

        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [1, 1]
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [1, 1, 0, 0]

        # Not within the space
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [0, 1, 2]

        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [0, 0.0, 1.0]

        act.setpoint = [0, 1, 0]

    def test_set_tuple(self):
        act = ActuatorInformation(
            None,
            Tuple(self.test_box2, self.test_discrete, self.test_multibinary),
            "Test",
        )

        # Wrong dimensions
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [-10]

        # Not within the space
        with self.assertRaises(OutOfActionSpaceError):
            act.setpoint = [[0, -5], 5, [0, 1, 0], [1.0]]

        act.setpoint = [[0, -5], 5, [0, 1, 0]]


if __name__ == "__main__":
    unittest.main()
