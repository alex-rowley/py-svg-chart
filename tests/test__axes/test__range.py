from datetime import datetime, date, timedelta
import unittest


from pysvgchart.axes import Range


class TestRange(unittest.TestCase):
    """
    test the Range class
    """

    def test__int_int_01(self):
        # given
        lo = 2
        hi = 9
        # when
        actual = Range(lo, hi)
        # then
        expect = lo
        self.assertEqual(expect, actual.lo)
        expect = hi
        self.assertEqual(expect, actual.hi)
        expect = 7
        self.assertEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(lo+(hi-lo)/2))

    def test__int_int_02(self):
        # given
        lo = 9
        hi = 2
        # when
        actual = Range(lo, hi)
        # then
        expect = hi
        self.assertEqual(expect, actual.lo)
        expect = lo
        self.assertEqual(expect, actual.hi)
        expect = 7
        self.assertEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(lo+(hi-lo)/2))

    def test__float_float_01(self):
        # given
        lo = 2.1
        hi = 9.2
        # when
        actual = Range(lo, hi)
        # then
        expect = lo
        self.assertEqual(expect, actual.lo)
        expect = hi
        self.assertEqual(expect, actual.hi)
        expect = 7.1
        self.assertAlmostEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(lo+(hi-lo)/2))

    def test__float_float_02(self):
        # given
        lo = 9.1
        hi = 2.2
        # when
        actual = Range(lo, hi)
        # then
        expect = hi
        self.assertEqual(expect, actual.lo)
        expect = lo
        self.assertEqual(expect, actual.hi)
        expect = 6.9
        self.assertAlmostEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(lo+(hi-lo)/2))

    def test__int_float_01(self):
        # given
        lo = 2
        hi = 9.2
        # when
        actual = Range(lo, hi)
        # then
        expect = lo
        self.assertEqual(expect, actual.lo)
        expect = hi
        self.assertEqual(expect, actual.hi)
        expect = 7.2
        self.assertAlmostEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(lo+(hi-lo)/2))

    def test__int_float_02(self):
        # given
        lo = 9
        hi = 2.2
        # when
        actual = Range(lo, hi)
        # then
        expect = hi
        self.assertEqual(expect, actual.lo)
        expect = lo
        self.assertEqual(expect, actual.hi)
        expect = 6.8
        self.assertAlmostEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(lo+(hi-lo)/2))

    def test__float_int_01(self):
        # given
        lo = 2.1
        hi = 9
        # when
        actual = Range(lo, hi)
        # then
        expect = lo
        self.assertEqual(expect, actual.lo)
        expect = hi
        self.assertEqual(expect, actual.hi)
        expect = 6.9
        self.assertAlmostEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(lo+(hi-lo)/2))

    def test__float_int_02(self):
        # given
        lo = 9.1
        hi = 2
        # when
        actual = Range(lo, hi)
        # then
        expect = hi
        self.assertEqual(expect, actual.lo)
        expect = lo
        self.assertEqual(expect, actual.hi)
        expect = 7.1
        self.assertAlmostEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(lo+(hi-lo)/2))

    def test__datetime_datetime_01(self):
        # given
        lo = datetime(1984, 2, 29, 11, 12, 13)
        hi = datetime(1984, 3, 1, 23, 59, 59)
        # when
        actual = Range(lo, hi)
        # then
        expect = lo
        self.assertEqual(expect, actual.lo)
        expect = hi
        self.assertEqual(expect, actual.hi)
        expect = timedelta(days=1, hours=12, minutes=47, seconds=46)
        self.assertEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(lo+(hi-lo)/2))

    def test__datetime_datetime_02(self):
        # given
        lo = datetime(1984, 3, 1, 23, 59, 59)
        hi = datetime(1984, 2, 29, 11, 12, 13)
        # when
        actual = Range(lo, hi)
        # then
        expect = hi
        self.assertEqual(expect, actual.lo)
        expect = lo
        self.assertEqual(expect, actual.hi)
        expect = timedelta(days=1, hours=12, minutes=47, seconds=46)
        self.assertEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(lo+(hi-lo)/2))

    def test__date_date_01(self):
        # given
        lo = date(1984, 2, 29)
        hi = date(1984, 3, 4)
        # when
        actual = Range(lo, hi)
        # then
        expect = lo
        self.assertEqual(expect, actual.lo)
        expect = hi
        self.assertEqual(expect, actual.hi)
        expect = timedelta(days=4)
        self.assertEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(lo+(hi-lo)/2))

    def test__date_date_02(self):
        # given
        lo = date(1984, 3, 4)
        hi = date(1984, 2, 29)
        # when
        actual = Range(lo, hi)
        # then
        expect = hi
        self.assertEqual(expect, actual.lo)
        expect = lo
        self.assertEqual(expect, actual.hi)
        expect = timedelta(days=4)
        self.assertEqual(expect, actual.size)
        expect = 0.5
        self.assertAlmostEqual(expect, actual.value_to_fraction(lo+(hi-lo)/2))

    def test__str_str_01(self):
        # given
        lo = "bar"
        hi = "foo"
        # when
        actual = Range(lo, hi)
        # then
        expect = lo
        self.assertEqual(expect, actual.lo)
        expect = hi
        self.assertEqual(expect, actual.hi)
        expect = None
        self.assertEqual(expect, actual.size)
        expect = "baz"
        self.assertEqual(expect, actual.value_to_fraction("baz"))

    def test__str_str_02(self):
        # given
        lo = "foo"
        hi = "bar"
        # when
        actual = Range(lo, hi)
        # then
        expect = hi
        self.assertEqual(expect, actual.lo)
        expect = lo
        self.assertEqual(expect, actual.hi)
        expect = None
        self.assertEqual(expect, actual.size)
        expect = "baz"
        self.assertEqual(expect, actual.value_to_fraction("baz"))


if __name__ == "__main__":
    unittest.main()
