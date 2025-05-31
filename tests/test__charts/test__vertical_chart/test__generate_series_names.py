import unittest


from pysvgchart.charts import VerticalChart


class TestGenerateSeriesNames(unittest.TestCase):
    """
    test the static method VerticalChart.generate_series_names()
    """

    def setUp(self) -> None:
        self.maxDiff = None

    def test_nothing(self):
        # given
        names = None
        n = 0
        # when
        actual = VerticalChart.generate_series_names(names=names, n=n)
        # then
        expect = []
        self.assertEqual(expect, actual)

    def test_no_names(self):
        # given
        names = None
        n = 3
        # when
        actual = VerticalChart.generate_series_names(names=names, n=n)
        # then
        expect = [
            "Series 1",
            "Series 2",
            "Series 3",
        ]
        self.assertEqual(expect, actual)

    def test_all_names(self):
        # given
        names = [
            "foo",
            "bar",
            "baz",
        ]
        n = 3
        # when
        actual = VerticalChart.generate_series_names(names=names, n=n)
        # then
        expect = [
            "foo",
            "bar",
            "baz",
        ]
        self.assertEqual(expect, actual)

    def test_too_few_names(self):
        # given
        names = [
            "foo",
            "bar",
        ]
        n = 3
        # when
        actual = VerticalChart.generate_series_names(names=names, n=n)
        # then
        expect = [
            "foo",
            "bar",
            "Series 3",
        ]
        self.assertEqual(expect, actual)

    def test_too_many_names(self):
        # given
        names = [
            "foo",
            "bar",
            "baz",
            "oops",
        ]
        n = 3
        # when
        actual = VerticalChart.generate_series_names(names=names, n=n)
        # then
        expect = [
            "foo",
            "bar",
            "baz",
        ]
        self.assertEqual(expect, actual)

    def test_gap_in_names(self):
        # given
        names = [
            "foo",
            None,
            "baz",
        ]
        n = 3
        # when
        actual = VerticalChart.generate_series_names(names=names, n=n)
        # then
        expect = [
            "foo",
            "Series 2",
            "baz",
        ]
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
