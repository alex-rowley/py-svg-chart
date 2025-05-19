from datetime import datetime, date, timedelta
from random import sample
import unittest


from pysvgchart.ranges import LinearRange, MappingRange


class TestLinearRange(unittest.TestCase):
    """
    test the LinearRange class
    """

    def test__ints(self):
        # given
        values = sample(range(2, 10), k=8)
        # when
        actual = LinearRange(values)
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
        actual = LinearRange(values)
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
        actual = LinearRange(values)
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
        actual = LinearRange(values)
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


class TestMappingRange(unittest.TestCase):
    """
    test the MappingRange class
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
        actual = MappingRange(values)
        # then
        for index, value in enumerate(values):
            expect = (2 * index + 1) / 16
            self.assertEqual(expect, actual.value_to_fraction(value), msg=f"failed for {value=} {index=}")


if __name__ == "__main__":
    unittest.main()
