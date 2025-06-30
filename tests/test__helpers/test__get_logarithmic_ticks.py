import unittest


from pysvgchart.helpers import get_logarithmic_ticks


class TestLogarithmicTicks(unittest.TestCase):
    """
    test the get_logarithmic_ticks() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_no_data(self):
        # given
        values = []
        max_ticks = 10
        # when        # then
        with self.assertRaises(ValueError):
            get_logarithmic_ticks(values, max_ticks)

    def test_one_value(self):
        # given
        values = [
            42,
        ]
        max_ticks = 10
        # when        # then
        with self.assertRaises(ValueError):
            get_logarithmic_ticks(values, max_ticks)

    def test_two_same_values(self):
        # given
        values = [
            42,
            42,
        ]
        max_ticks = 10
        # when        # then
        with self.assertRaises(ValueError):
            get_logarithmic_ticks(values, max_ticks)

    def test_two_close_ints_few_ticks(self):
        # given
        values = [
            42,
            48,
        ]
        max_ticks = 3
        # when
        actual = get_logarithmic_ticks(values, max_ticks)
        # then
        expect = [
            10,
            100,
        ]
        self.assertListEqual(expect, actual)

    def test_two_close_ints_more_ticks(self):
        # given
        values = [
            42,
            48,
        ]
        max_ticks = 10
        # when
        actual = get_logarithmic_ticks(values, max_ticks)
        # then
        expect = [
            10,
            100,
        ]
        self.assertListEqual(expect, actual)

    def test_two_close_floats_few_ticks(self):
        # given
        values = [
            2.71828182845904523536,
            3.14159265358979323846,
        ]
        max_ticks = 3
        # when
        actual = get_logarithmic_ticks(values, max_ticks)
        # then
        expect = [
            1,
            10,
        ]
        self.assertListEqual(expect, actual)

    def test_two_close_floats_more_ticks(self):
        # given
        values = [
            2.71828182845904523536,
            3.14159265358979323846,
        ]
        max_ticks = 10
        # when
        actual = get_logarithmic_ticks(values, max_ticks)
        # then
        expect = [
            1,
            10,
        ]
        self.assertListEqual(expect, actual)

    def test_two_far_ints_few_ticks(self):
        # given
        values = [
            42,
            666,
        ]
        max_ticks = 3
        # when
        actual = get_logarithmic_ticks(values, max_ticks)
        # then
        expect = [
            10,
            100,
            1000,
        ]
        self.assertListEqual(expect, actual)

    def test_two_far_ints_more_ticks(self):
        # given
        values = [
            42,
            666,
        ]
        max_ticks = 10
        # when
        actual = get_logarithmic_ticks(values, max_ticks)
        # then
        expect = [
            10,
            100,
            1000,
        ]
        self.assertListEqual(expect, actual)

    def test_two_far_floats_few_ticks(self):
        # given
        values = [
            0.4,
            6553.6,
        ]
        max_ticks = 3
        # when
        actual = get_logarithmic_ticks(values, max_ticks)
        # then
        expect = [
            0.1,
            100,
            100000,
        ]
        self.assertListEqual(expect, actual)

    def test_two_far_floats_more_ticks(self):
        # given
        values = [
            0.4,
            6553.6,
        ]
        max_ticks = 10
        # when
        actual = get_logarithmic_ticks(values, max_ticks)
        # then
        expect = [
            0.1,
            1,
            10,
            100,
            1000,
            10000,
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
