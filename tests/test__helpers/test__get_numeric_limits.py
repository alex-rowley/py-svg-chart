import unittest


from pysvgchart.helpers import get_numeric_limits


class TestNumericLimits(unittest.TestCase):
    """
    test the get_numeric_limits() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_no_data(self):
        # given
        values = []
        max_ticks = 10
        # when        # then
        with self.assertRaises(ValueError):
            get_numeric_limits(values, max_ticks)

    def test_one_value(self):
        # given
        values = [
            42,
        ]
        max_ticks = 10
        # when        # then
        with self.assertRaises(ValueError):
            get_numeric_limits(values, max_ticks)

    def test_two_same_values(self):
        # given
        values = [
            42,
            42,
        ]
        max_ticks = 10
        # when        # then
        with self.assertRaises(ValueError):
            get_numeric_limits(values, max_ticks)

    def test_two_close_ints_few_ticks(self):
        # given
        values = [
            42,
            48,
        ]
        max_ticks = 3
        # when
        actual = get_numeric_limits(values, max_ticks)
        # then
        expect = [
            42,
            44,
            46,
            48,
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
        actual = get_numeric_limits(values, max_ticks)
        # then
        expect = [
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
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
        actual = get_numeric_limits(values, max_ticks)
        # then
        expect = [
            2.6,
            2.8,
            3.0,
            3.2,
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
        actual = get_numeric_limits(values, max_ticks)
        # then
        expect = [
            2.70,
            2.75,
            2.80,
            2.85,
            2.90,
            2.95,
            3.00,
            3.05,
            3.10,
            3.15,
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
        actual = get_numeric_limits(values, max_ticks)
        # then
        expect = [
            0,
            500,
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
        actual = get_numeric_limits(values, max_ticks)
        # then
        expect = [
            0,
            100,
            200,
            300,
            400,
            500,
            600,
            700,
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
        actual = get_numeric_limits(values, max_ticks)
        # then
        expect = [
            0,
            5000,
            10000,
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
        actual = get_numeric_limits(values, max_ticks)
        # then
        expect = [
            0.0,
            1000.0,
            2000.0,
            3000.0,
            4000.0,
            5000.0,
            6000.0,
            7000.0,
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
