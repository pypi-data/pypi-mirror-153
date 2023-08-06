from unittest import TestCase
import numpy as np
from palaestrai.types import Box
from palaestrai.types import Discrete
from palaestrai.types import MultiDiscrete
from palaestrai.types import MultiBinary
from palaestrai.types import Tuple
from palaestrai.types import utils


class UtilsTest(TestCase):
    def setUp(self) -> None:
        self.box_float = Box(
            low=-1.0, high=2.0, shape=(3, 4), dtype=np.float32
        )
        self.discrete_sample = Discrete(3)
        self.multi_binary_sample = MultiBinary(2)
        self.multi_discrete_sample = MultiDiscrete([5, 4, 2])
        self.tuple_discrete_sample = Tuple(Discrete(2), Discrete(3))
        self.tuple_boxes_sample = Tuple(
            Box(low=-1.0, high=2.0, shape=(3, 4), dtype=np.float32),
            Box(low=-2.0, high=3.0, shape=(2, 3), dtype=np.float32),
        )

    def test_flatdim(self):
        self.assertEqual(utils.flatdim(self.box_float), 12)
        self.assertEqual(utils.flatdim(self.discrete_sample), 3)
        self.assertEqual(utils.flatdim(self.tuple_discrete_sample), 5)
        self.assertEqual(utils.flatdim(self.tuple_boxes_sample), 18)
        self.assertEqual(utils.flatdim(self.multi_binary_sample), 2)
        self.assertEqual(utils.flatdim(self.multi_discrete_sample), 3)
        with self.assertRaises(NotImplementedError):
            utils.flatdim("any other type")

    def test_flatten_Box(self):
        x = [
            [1.9454306, 0.25988454, -0.41315162, 1.3343621],
            [1.7871696, -0.6225805, 0.88759154, 0.5394544],
            [1.2164323, 0.21180445, 1.0201195, -0.4387453],
        ]
        x_expected = np.array(
            [
                1.9454306,
                0.25988454,
                -0.41315162,
                1.3343621,
                1.7871696,
                -0.6225805,
                0.88759154,
                0.5394544,
                1.2164323,
                0.21180445,
                1.0201195,
                -0.4387453,
            ],
            dtype=np.float32,
        )

        self.assertEqual(
            utils.flatten(self.box_float, x).shape, x_expected.shape
        )
        for pair in zip(x_expected, utils.flatten(self.box_float, x)):
            self.assertEqual(pair[0], pair[1])

    def test_flatten_discrete(self):
        x = 2
        x_expected = [0.0, 0.0, 1.0]

        for pair in zip(x_expected, utils.flatten(self.discrete_sample, x)):
            self.assertEqual(pair[0], pair[1])

    def test_flatten_Tuple(self):
        # for tuple of discrete:
        t = (1, 2)
        t_expected = [0.0, 1.0, 0.0, 0.0, 1.0]
        for pair in zip(
            t_expected, utils.flatten(self.tuple_discrete_sample, t)
        ):
            self.assertEqual(pair[0], pair[1])
        # for tuple of boxes:
        tboxes = (
            [
                [1.9454306, 0.25988454, -0.41315162, 1.3343621],
                [1.7871696, -0.6225805, 0.88759154, 0.5394544],
                [1.2164323, 0.21180445, 1.0201195, -0.4387453],
            ],
            [
                [1.9454306, 0.25988454, -0.41315162],
                [1.7871696, -0.6225805, 0.88759154],
            ],
        )
        tboxes_expected = np.array(
            [
                1.9454306,
                0.25988454,
                -0.41315162,
                1.3343621,
                1.7871696,
                -0.6225805,
                0.88759154,
                0.5394544,
                1.2164323,
                0.21180445,
                1.0201195,
                -0.4387453,
                1.9454306,
                0.25988454,
                -0.41315162,
                1.7871696,
                -0.6225805,
                0.88759154,
            ],
            dtype=np.float32,
        )

        self.assertEqual(
            utils.flatten(self.tuple_boxes_sample, tboxes).shape,
            tboxes_expected.shape,
        )
        for pair in zip(
            tboxes_expected, utils.flatten(self.tuple_boxes_sample, tboxes)
        ):
            self.assertEqual(pair[0], pair[1])

    def test_flatten_multibinary(self):
        x = np.array([0, 1], dtype=int)
        x_expected = np.array([0, 1], dtype=int)
        for pair in zip(
            x_expected, utils.flatten(self.multi_binary_sample, x)
        ):
            self.assertEqual(pair[0], pair[1])

    def test_flatten_multidiscrete(self):
        x = np.array([1, 1, 0], dtype=int)
        x_expected = np.array(
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0],
            dtype=np.float32,
        )
        for pair in zip(
            x_expected, utils.flatten(self.multi_discrete_sample, x)
        ):
            self.assertEqual(pair[0], pair[1])

    def test_flatten_othertypes(self):
        with self.assertRaises(NotImplementedError):
            utils.flatten("other space", "any other type")

    def test_unflatten_Box(self):
        x = np.array(
            [
                1.9454306,
                0.25988454,
                -0.41315162,
                1.3343621,
                1.7871696,
                -0.6225805,
                0.88759154,
                0.5394544,
                1.2164323,
                0.21180445,
                1.0201195,
                -0.4387453,
            ],
            dtype=np.float32,
        )

        x_expected = np.array(
            [
                [1.9454306, 0.25988454, -0.41315162, 1.3343621],
                [1.7871696, -0.6225805, 0.88759154, 0.5394544],
                [1.2164323, 0.21180445, 1.0201195, -0.4387453],
            ],
            dtype=np.float32,
        )

        self.assertEqual(
            utils.unflatten(self.box_float, x).shape, x_expected.shape
        )
        for pair in zip(utils.unflatten(self.box_float, x), x_expected):
            self.assertEqual(np.array_equal(pair[0], pair[1]), True)

    def test_unflatten_Discrete(self):

        x = [0.0, 0.0, 1.0]
        x_expected = 2
        self.assertEqual(x_expected, utils.unflatten(self.discrete_sample, x))

    def test_unflatten_Tuple(self):
        # for tuple of discrete:
        t = [0.0, 1.0, 0.0, 0.0, 1.0]
        t_expected = (1, 2)
        for pair in zip(
            t_expected, utils.unflatten(self.tuple_discrete_sample, t)
        ):
            self.assertEqual(pair[0], pair[1])
        # for tuple of boxes:
        tboxes = np.array(
            [
                1.9454306,
                0.25988454,
                -0.41315162,
                1.3343621,
                1.7871696,
                -0.6225805,
                0.88759154,
                0.5394544,
                1.2164323,
                0.21180445,
                1.0201195,
                -0.4387453,
                1.9454306,
                0.25988454,
                -0.41315162,
                1.7871696,
                -0.6225805,
                0.88759154,
            ],
            dtype=np.float32,
        )
        tboxes_expected = (
            np.array(
                [
                    [1.9454306, 0.25988454, -0.41315162, 1.3343621],
                    [1.7871696, -0.6225805, 0.88759154, 0.5394544],
                    [1.2164323, 0.21180445, 1.0201195, -0.4387453],
                ],
                dtype=np.float32,
            ),
            np.array(
                [
                    [1.9454306, 0.25988454, -0.41315162],
                    [1.7871696, -0.6225805, 0.88759154],
                ],
                dtype=np.float32,
            ),
        )

        # both shape and values are checked in np.array_equal
        for pair in zip(
            tboxes_expected, utils.unflatten(self.tuple_boxes_sample, tboxes)
        ):
            self.assertEqual(np.array_equal(pair[0], pair[1]), True)

    def test_unflatten_multibinary(self):
        x = np.array([0, 1], dtype=int)
        x_expected = np.array([0, 1], dtype=int)  # trivial ?!
        for pair in zip(
            x_expected, utils.unflatten(self.multi_binary_sample, x)
        ):
            self.assertEqual(pair[0], pair[1])

    def test_unflatten_multidiscrete(self):
        x = np.array(
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0],
            dtype=np.float32,
        )
        x_expected = np.array([4, 1, 0], dtype=int)
        for pair in zip(
            x_expected, utils.unflatten(self.multi_discrete_sample, x)
        ):
            self.assertEqual(pair[0], pair[1])

    def test_unflatten_othertypes(self):
        with self.assertRaises(NotImplementedError):
            utils.unflatten("other space", "any other type")
