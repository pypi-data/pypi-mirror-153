from unittest import TestCase

from numpy.random import RandomState

from palaestrai.util.seeding import (
    create_seed,
    np_random,
    hash_seed,
    _bigint_from_bytes,
    _int_list_from_bigint,
)


class SeedingTest(TestCase):
    def test_np_random_runtime_error(self):
        # Check Runtime Errors
        self.assertRaises(RuntimeError, np_random, 12.0)
        self.assertRaises(RuntimeError, np_random, "asdf")

    def test_np_random_keep_seed(self):
        rng, seed = np_random(4)
        self.assertEqual(seed, 4)
        self.assertIsInstance(rng, RandomState)

    def test_np_random_deterministic_seed(self):
        rng, seed = np_random(4)
        self.assertEqual(seed, 4)
        self.assertIsInstance(rng, RandomState)
        rng2, seed2 = np_random()
        self.assertIsInstance(rng2, RandomState)
        self.assertIsInstance(seed2, int)

    def test_np_random_deterministic_seed2(self):
        rng, seed = np_random(4)
        rng_2, seed_2 = np_random(4)
        self.assertEqual(seed, seed_2)
        rng_state = rng._bit_generator.state
        rng2_state = rng_2._bit_generator.state
        self.assertTrue(str(rng_state) == str(rng2_state))

    def test_hash_seed(self):
        seed_1 = hash_seed()
        self.assertIsInstance(seed_1, int)
        seed_2 = hash_seed(5)
        self.assertNotEqual(seed_2, 5)
        seed_3 = hash_seed(5)
        self.assertEqual(seed_3, seed_2)

    def test_create_seed(self):
        no_seed = create_seed()
        assert isinstance(no_seed, int)

        str_seed = create_seed("9")
        assert isinstance(str_seed, int)
        str_seed2 = create_seed("9")
        assert str_seed2 == str_seed
        str_seed_diff = create_seed("asdf")
        str_seed_diff2 = create_seed("asdf")
        assert str_seed_diff != str_seed
        assert str_seed_diff2 == str_seed_diff

        int_types_seed = create_seed(9)
        int_types_seed2 = create_seed(9)
        assert isinstance(int_types_seed, int)
        assert int_types_seed == str_seed
        assert int_types_seed == int_types_seed2

    def test_bigint_from_bytes(self):
        bytes_s = b"asdfasdfdsfsdaf"
        self.assertEqual(
            _bigint_from_bytes(bytes_s), _bigint_from_bytes(bytes_s)
        )

    def test_int_list_from_bigint(self):
        int_list = _int_list_from_bigint(249213748921473982147893214)
        self.assertEqual(int_list, [1275107294, 1716681061, 13509904])
