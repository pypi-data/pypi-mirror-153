from unittest import TestCase
from palaestrai.types import Discrete
import numpy as np


class DiscreteTest(TestCase):
    def setUp(self) -> None:
        self.discrete = Discrete(2)

    def test_sample(self):
        for x in range(0, 50):
            self.assertTrue(0 <= self.discrete.sample() <= 1)

    def test_contains(self):
        # test if all values are contained, but not more
        self.assertTrue(self.discrete.contains(0))
        self.assertTrue(self.discrete.contains(1))
        self.assertFalse(self.discrete.contains(2))

        # test if floats are contained
        self.assertRaises(TypeError, self.discrete.contains, 0.0)
        self.assertRaises(TypeError, self.discrete.contains, 2.0)

        # test if strings are contained
        self.assertRaises(TypeError, self.discrete.contains, "0")
        self.assertRaises(TypeError, self.discrete.contains, "1")
        self.assertRaises(TypeError, self.discrete.contains, "2.0")

        # test if arrays are contained
        self.assertRaises(
            TypeError, self.discrete.contains, np.array([0, 0, 1, 0])
        )
        self.assertRaises(TypeError, self.discrete.contains, np.array([0]))

    def test_flatten(self):
        self.assertTrue(
            np.array_equal(self.discrete.to_vector(np.array(1)), [0, 1])
        )
        self.assertTrue(
            np.array_equal(self.discrete.to_vector(np.array([0])), [1, 0])
        )

    def test_reshape(self):
        self.assertEqual(self.discrete.reshape_to_space([0, 1]), 1)
        self.assertEqual(self.discrete.reshape_to_space([1, 0]), 0)
        self.assertEqual(
            self.discrete.reshape_to_space([1, 0], dtype="S128"), [0]
        )  # this needs to be compared to an actual array, because that is how numpy represents numpy strings

    def test_length(self):
        self.assertEqual(len(self.discrete), 2)
