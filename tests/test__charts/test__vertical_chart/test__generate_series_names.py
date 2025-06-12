import unittest
from random import choice

from pysvgchart.charts import VerticalChart


PREFIXES = (
    "prefix",
    "foo",
    "bar",
    "baz",
    "Guido",
    "serpent",
    "Ni",
)

class TestGenerateSeriesNames(unittest.TestCase):
    """
    test the static method VerticalChart.generate_series_names()
    """

    def setUp(self) -> None:
        self.maxDiff = None

    def test_nothing(self):
        # given
        prefix = choice(PREFIXES)
        n = 0
        names = None
        # when
        actual = VerticalChart.generate_series_names(prefix=prefix, n=n, names=names)
        # then
        expect = []
        self.assertEqual(expect, actual, msg=f"failed for {prefix=}")

    def test_no_names(self):
        # given
        prefix = choice(PREFIXES)
        n = 3
        names = None
        # when
        actual = VerticalChart.generate_series_names(prefix=prefix, n=n, names=names)
        # then
        expect = [
            f"{prefix} 1",
            f"{prefix} 2",
            f"{prefix} 3",
        ]
        self.assertEqual(expect, actual, msg=f"failed for {prefix=}")

    def test_all_names(self):
        # given
        prefix = choice(PREFIXES)
        n = 3
        names = [
            "foo",
            "bar",
            "baz",
        ]
        # when
        actual = VerticalChart.generate_series_names(prefix=prefix, n=n, names=names)
        # then
        expect = [
            "foo",
            "bar",
            "baz",
        ]
        self.assertEqual(expect, actual, msg=f"failed for {prefix=}")

    def test_too_few_names(self):
        # given
        prefix = choice(PREFIXES)
        n = 3
        names = [
            "foo",
            "bar",
        ]
        # when
        actual = VerticalChart.generate_series_names(prefix=prefix, n=n, names=names)
        # then
        expect = [
            "foo",
            "bar",
            f"{prefix} 3",
        ]
        self.assertEqual(expect, actual, msg=f"failed for {prefix=}")

    def test_too_many_names(self):
        # given
        prefix = choice(PREFIXES)
        n = 3
        names = [
            "foo",
            "bar",
            "baz",
            "oops",
        ]
        # when
        actual = VerticalChart.generate_series_names(prefix=prefix, n=n, names=names)
        # then
        expect = [
            "foo",
            "bar",
            "baz",
        ]
        self.assertEqual(expect, actual, msg=f"failed for {prefix=}")

    def test_gap_in_names(self):
        # given
        prefix = choice(PREFIXES)
        n = 3
        names = [
            "foo",
            None,
            "baz",
        ]
        # when
        actual = VerticalChart.generate_series_names(prefix=prefix, n=n, names=names)
        # then
        expect = [
            "foo",
            f"{prefix} 2",
            "baz",
        ]
        self.assertEqual(expect, actual, msg=f"failed for {prefix=}")


if __name__ == "__main__":
    unittest.main()
