from datetime import datetime, date, timedelta
from random import sample
import unittest


from pysvgchart.scales import LinearScale, LogarithmicScale, MappingScale


class TestLinearScale(unittest.TestCase):
    """
    test the LinearScale class
    """

    def test__ints(self):
        # given
        values = sample(range(2, 10), k=8)
        # when
        actual = LinearScale(values)
        # then
        msg = f"failed for {values=}"
        expect = 2
        self.assertEqual(expect, actual.lo, msg=msg)
        expect = 9
        self.assertEqual(expect, actual.hi, msg=msg)
        expect = 9 - 2
        self.assertEqual(expect, actual.size, msg=msg)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(5.5), msg=msg)

    def test__floats(self):
        # given
        values = sample([x / 8 for x in range(2, 10)], k=8)
        # when
        actual = LinearScale(values)
        # then
        msg = f"failed for {values=}"
        expect = 2 / 8
        self.assertEqual(expect, actual.lo, msg=msg)
        expect = 9 / 8
        self.assertEqual(expect, actual.hi, msg=msg)
        expect = 9 / 8 - 2 / 8
        self.assertEqual(expect, actual.size, msg=msg)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(5.5 / 8), msg=msg)

    def test__datetimes(self):
        # given
        values = sample(
            [
                datetime(1984, x, 29, x, x, x)
                for x in range(2, 10)
            ],
            k=8,
        )
        # when
        actual = LinearScale(values)
        # then
        msg = f"failed for {values=}"
        expect = datetime(1984, 2, 29, 2, 2, 2)
        self.assertEqual(expect, actual.lo, msg=msg)
        expect = datetime(1984, 9, 29, 9, 9, 9)
        self.assertEqual(expect, actual.hi, msg=msg)
        expect = datetime(1984, 9, 29, 9, 9, 9) - datetime(1984, 2, 29, 2, 2, 2)
        self.assertEqual(expect, actual.size, msg=msg)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(datetime(1984, 6, 14, 17, 35, 35)), msg=msg)

    def test__dates(self):
        # given
        values = sample(
            [
                date(1984, x, 29)
                for x in range(2, 10)
            ],
            k=8,
        )
        # when
        actual = LinearScale(values)
        # then
        msg = f"failed for {values=}"
        expect = date(1984, 2, 29)
        self.assertEqual(expect, actual.lo, msg=msg)
        expect = date(1984, 9, 29)
        self.assertEqual(expect, actual.hi, msg=msg)
        expect = date(1984, 9, 29) - date(1984, 2, 29)
        self.assertEqual(expect, actual.size, msg=msg)
        expect = 0.5
        delta = timedelta(days=1).total_seconds() - 1  # just less than a full day -> best approximation
        self.assertAlmostEqual(expect, actual.value_to_fraction(date(1984, 6, 14)), delta=delta, msg=msg)


class TestLogarithmicScale(unittest.TestCase):
    """
    test the LogarithmicScale class
    """

    def test__close_ints(self):
        # given
        values = [1, 10, 100]
        # when
        actual = LogarithmicScale(values)
        # then
        expect = 0.0
        self.assertEqual(expect, actual.log_lo)
        expect = 2.0
        self.assertEqual(expect, actual.log_hi)
        expect = 2.0
        self.assertEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(10))

    def test__far_ints(self):
        # given
        values = [10, 1000, 100000, 10000000, 1000000000]
        # when
        actual = LogarithmicScale(values)
        # then
        expect = 1.0
        self.assertEqual(expect, actual.log_lo)
        expect = 9.0
        self.assertEqual(expect, actual.log_hi)
        expect = 8.0
        self.assertEqual(expect, actual.size)
        expect = 0.25
        self.assertAlmostEqual(expect, actual.value_to_fraction(1000))
        expect = 0.50
        self.assertAlmostEqual(expect, actual.value_to_fraction(100000))
        expect = 0.75
        self.assertAlmostEqual(expect, actual.value_to_fraction(10000000))

    def test__close_floats(self):
        # given
        values = [0.1, 1, 10]
        # when
        actual = LogarithmicScale(values)
        # then
        expect = -1.0
        self.assertEqual(expect, actual.log_lo)
        expect = 1.0
        self.assertEqual(expect, actual.log_hi)
        expect = 2.0
        self.assertEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(1))

    def test__far_floats(self):
        # given
        values = [0.001, 0.1, 10, 1000]
        # when
        actual = LogarithmicScale(values)
        # then
        expect = -3.0
        self.assertEqual(expect, actual.log_lo)
        expect = 3.0
        self.assertEqual(expect, actual.log_hi)
        expect = 6.0
        self.assertEqual(expect, actual.size)
        expect = 0.3333333333
        self.assertAlmostEqual(expect, actual.value_to_fraction(0.1))
        expect = 0.6666666666
        self.assertAlmostEqual(expect, actual.value_to_fraction(10))
        expect = 1.0
        self.assertAlmostEqual(expect, actual.value_to_fraction(1000))


class TestMappingScale(unittest.TestCase):
    """
    test the MappingScale class
    """

    def test__strs(self):
        # given
        values = [
            "bar",
            "baz",
            "foo",
            "guido",
            "ni",
            "python",
            "rabbit",
            "swallow",
        ]
        # when
        actual = MappingScale(values)
        # then
        for index, value in enumerate(values):
            expect = (2 * index + 1) / 16
            self.assertEqual(expect, actual.value_to_fraction(value), msg=f"failed for {value=} {index=}")


if __name__ == "__main__":
    unittest.main()
