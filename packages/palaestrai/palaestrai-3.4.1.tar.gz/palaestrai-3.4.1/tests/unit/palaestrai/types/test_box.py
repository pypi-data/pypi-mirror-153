from unittest import TestCase
from palaestrai.types import Box, Space
import numpy as np


class BoxTest(TestCase):
    def setUp(self) -> None:
        self.box_float = Box(
            low=-1.0, high=2.0, shape=(3, 4), dtype=np.float32
        )
        self.box_float_inner = Box(
            low=0.0, high=1.0, shape=(3, 4), dtype=np.float32
        )
        self.box_diff_bounds = Box(
            low=np.array([0.0, -10.0, 12]),
            high=np.array([1.0, 10.0, 78]),
            dtype=np.float32,
        )
        self.box_diff_bounds_arrays = Box(
            low=[[0.0, 1.0], [2.0, 3.0]],
            high=[[0.0, 1.0], [2.0, 3.0]],
            dtype=np.float32,
        )
        self.scalar_box = Box(
            low=0,
            high=10,
            dtype=np.int32,
        )

    def test_sample(self):
        for x in range(0, 50):
            self.assertTrue(
                self.box_float.sample().min() > -1
                and self.box_float.sample().max() < 3
            )

    def test_contains(self):
        # box should contain its own samples
        sample_self = self.box_float.sample()
        self.assertTrue(self.box_float.contains(sample_self))

        # box should contain samples of more restricted boxes
        sample_other = self.box_float_inner.sample()
        self.assertTrue(self.box_float.contains(sample_other))

        # all values inside of box
        array_expected_true = [
            [0.41128066, 0.3421888, 1.2279652, 1.2973598],
            [1.7220176, 0.7265164, 1.591186, 1.2400235],
            [1.9035902, -0.62997127, 0.12461133, 0.02076343],
        ]
        self.assertTrue(self.box_float.contains(array_expected_true))

        # array not in box because 25.411 > 2.0
        array_expected_false = [
            [25, 0.3421888, 1.2279652, 1.2973598],
            [1.7220176, 0.7265164, 1.591186, 1.2400235],
            [1.9035902, -0.62997127, 0.12461133, 0.02076343],
        ]
        self.assertFalse(self.box_float.contains(array_expected_false))

        # lower and upper bound inside of box
        lower_bound = [[-1, -1, -1, -1]] * 3
        self.assertTrue(self.box_float.contains(lower_bound))
        upper_bound = [[2, 2, 2, 2]] * 3
        self.assertTrue(self.box_float.contains(upper_bound))

        # scalar values inside 1D box
        self.assertTrue(self.scalar_box.contains(0))
        self.assertFalse(
            self.scalar_box.contains([10])
        )  # the box will only accept scalar values, not 1element lists
        self.assertFalse(self.scalar_box.contains(-5))
        self.assertFalse(self.scalar_box.contains([0, 2, 10]))

    def test_contains_single_value(self):
        b = Box(low=0.0, high=1.0, shape=(1,), dtype=np.float32)
        self.assertTrue(b.contains([float(0.52620125)]))

    def test_contains_single_value_in_list(self):
        b = Box(
            low=np.array([0.0]),
            high=np.array([1.0]),
            shape=(1,),
            dtype=np.float32,
        )
        self.assertTrue(b.contains([0.4564]))

    def test_contains_values_list(self):
        b = Box(low=0.0, high=1.1, shape=(3,), dtype=np.float32)
        self.assertTrue(b.contains([0.4564, 0.12314, 0.738457]))

    def test_contains_values_array(self):
        b = Box(
            low=[[0.0, 1.0], [2.0, 3.0]],
            high=[[1.0, 2.0], [3.0, 4.0]],
            dtype=np.float32,
        )
        self.assertTrue(b.contains([[0.12314, 1.738457], [2.3020, 3.0123]]))

    def test_not_contains_str_values(self):
        # single string value
        self.assertFalse(self.box_float.contains(["1"]))

        # all values inside of box, but some are string
        part_string_array = [
            ["0.41128066", "0.3421888", "1.2279652", 1.2973598],
            [1.7220176, 0.7265164, 1.591186, "1.2400235"],
            [1.9035902, -0.62997127, 0.12461133, "0.02076343"],
        ]
        self.assertTrue(self.box_float.contains(part_string_array))

        # all values inside of box, but all are string
        full_string_array = [
            ["0.41128066", "0.3421888", "1.2279652", "1.2973598"],
            ["1.7220176", "0.7265164", "1.591186", "1.2400235"],
            ["1.9035902", "-0.62997127", "0.12461133", "0.02076343"],
        ]
        self.assertTrue(self.box_float.contains(full_string_array))

        # all values inside of box, but the array is represented as string
        string_array = "[\
            [0.41128066, 0.3421888, 1.2279652, 1.2973598],\
            [1.7220176, 0.7265164, 1.591186, 1.2400235],\
            [1.9035902, -0.62997127, 0.12461133, 0.02076343],\
        ]"
        self.assertRaises(ValueError, self.box_float.contains, string_array)

    def test_to_string_equals(self):
        self.assertEqual(
            Box(low=-1.0, high=1.0, shape=(1,)).to_string(),
            "Box(low=[-1.0], high=[1.0], shape=(1,), dtype=np.float32)",
        )

    def test_from_to_string(self):
        box1 = Box.from_string(
            "Box(low=[  0., -10.,  12.], "
            "   high=[ 1., 10., 78.], dtype=np.float32)"
        )
        self.assertEqual(box1, Box.from_string(box1.to_string()))
        self.assertEqual(box1, Space.from_string(box1.to_string()))

    def test_from_string(self):
        self.assertEqual(
            self.box_float,
            Box.from_string(
                "Box(low=-1.0, high=2.0," "shape=(3, 4), dtype=np.float32)"
            ),
        )
        self.assertEqual(
            self.box_float,
            Box.from_string(
                " Box(low=-1.0, high=2.0, shape=(3, 4), dtype=np.float32)"
            ),
        )
        self.assertEqual(
            self.box_diff_bounds,
            Box.from_string(
                "Box(low=[  0., -10.,  12.],"
                "high=[ 1., 10., 78.],"
                "dtype=np.float32)"
            ),
        )

        self.assertEqual(
            self.box_diff_bounds_arrays,
            Box.from_string(
                "Box(low=[ [ 0., 1.], [ 2., 3.]],"
                "high=[ [0., 1.], [2., 3.]],"
                "dtype=np.float32)"
            ),
        )

    def test_space_factory(self):
        self.assertEqual(
            self.box_float,
            Space.from_string(
                " Box(low=-1.0, high=2.0, shape=(3, 4), dtype=np.float32)"
            ),
        )

    def test_to_string_irregular(self):
        box_irr = (
            "Box(low=[-1.0, -1.0, -1.0], "
            "high=[1.0, 1.0, 1.0], "
            "shape=(3,), "
            "dtype=np.float32)"
        )
        box1 = Box(low=-1, high=1, shape=(3,))
        self.assertEqual(box_irr, box1.to_string())

    def test_string_compatibility(self):
        box = self.box_diff_bounds.to_string()
        diff_bounds_fs = Space.from_string(box)
        self.assertEqual(diff_bounds_fs, self.box_diff_bounds)

        box = self.box_float.to_string()
        float_fs = Box.from_string(box)
        self.assertEqual(float_fs, self.box_float)

    def test_flatten(self):
        data = [
            [1, 1, 1.5, 2.0],
            [2, 1.9, 1.345, 1.111],
            [2.0, 1.665, 1.999998, 1.3223443],
        ]
        self.assertTrue(
            np.array_equal(
                self.box_float.to_vector(np.array(data)),
                [
                    1,
                    1,
                    1.5,
                    2.0,
                    2,
                    1.9,
                    1.345,
                    1.111,
                    2.0,
                    1.665,
                    1.999998,
                    1.3223443,
                ],
            )
        )
        data_wrong_shape = [[1, 1, 1.5, 2.0], [2, 1.9, 1.345, 1.111]]
        self.assertTrue(
            np.array_equal(
                self.box_float.to_vector(np.array(data_wrong_shape)),
                [1, 1, 1.5, 2.0, 2, 1.9, 1.345, 1.111],
            )
        )

    def test_reshape(self):
        data = [
            1,
            1,
            1.5,
            2.0,
            2,
            1.9,
            1.345,
            1.111,
            2.0,
            1.665,
            1.999998,
            1.3223443,
        ]
        self.assertTrue(
            np.array_equal(
                self.box_float.reshape_to_space(np.array(data)),
                [
                    [1, 1, 1.5, 2.0],
                    [2, 1.9, 1.345, 1.111],
                    [2.0, 1.665, 1.999998, 1.3223443],
                ],
            )
        )
        data_wrong_length = [1, 1, 1.5, 2.0, 2, 1.9, 1.345, 1.111]
        self.assertRaises(
            ValueError,
            self.box_float.reshape_to_space,
            np.array(data_wrong_length),
        )

    def test_length(self):
        self.assertEqual(len(self.box_float), 12)
        self.assertEqual(len(self.box_float_inner), 12)
        self.assertEqual(len(self.box_diff_bounds), 3)
        self.assertEqual(len(self.box_diff_bounds_arrays), 4)
