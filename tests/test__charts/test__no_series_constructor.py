import unittest
from unittest.mock import patch, call


from pysvgchart.charts import no_series_constructor


class TestNoSeriesConstructor(unittest.TestCase):
    """
    test the no_series_constructor() function
    """

    def setUp(self) -> None:
        self.maxDiff = None

    @patch("pysvgchart.charts.Series")
    def test_no_series(self, mock_series):
        mock_series.side_effect = lambda *args: args
        # given
        x_values = [1, 2, 3]
        y_values = []
        x_axis = "x"
        y_axis = "y"
        series_names = []
        bar_width = 1
        bar_gap = 1
        # when
        actual = no_series_constructor(
            x_values,
            y_values,
            x_axis,
            y_axis,
            series_names,
            bar_width,
            bar_gap,
        )
        # then
        expect = []
        self.assertListEqual(expect, mock_series.mock_calls)
        expect = {}
        self.assertDictEqual(expect, actual)

    @patch("pysvgchart.charts.Series")
    def test_too_many_names(self, mock_series):
        mock_series.side_effect = lambda *args: args
        # given
        x_values = [1, 2, 3]
        y_values = []
        x_axis = "x"
        y_axis = "y"
        series_names = ["a", "b", "c"]
        bar_width = 1
        bar_gap = 1
        # when
        # then
        with self.assertRaises(ValueError):
            no_series_constructor(
                x_values,
                y_values,
                x_axis,
                y_axis,
                series_names,
                bar_width,
                bar_gap,
            )

    @patch("pysvgchart.charts.Series")
    def test_too_few_names(self, mock_series):
        mock_series.side_effect = lambda *args: args
        # given
        x_values = [1, 2, 3]
        y_values = [
            [0, 1, 2],
        ]
        x_axis = "x"
        y_axis = "y"
        series_names = []
        bar_width = 1
        bar_gap = 1
        # when
        # then
        with self.assertRaises(ValueError):
            no_series_constructor(
                x_values,
                y_values,
                x_axis,
                y_axis,
                series_names,
                bar_width,
                bar_gap,
            )

    @patch("pysvgchart.charts.Series")
    def test_unequal_values_1(self, mock_series):
        mock_series.side_effect = lambda *args: args
        # given
        x_values = [1, 2, 3]
        y_values = [
            [0],
        ]
        x_axis = "x"
        y_axis = "y"
        series_names = []
        bar_width = 1
        bar_gap = 1
        # when
        # then
        with self.assertRaises(ValueError):
            no_series_constructor(
                x_values,
                y_values,
                x_axis,
                y_axis,
                series_names,
                bar_width,
                bar_gap,
            )

    @patch("pysvgchart.charts.Series")
    def test_unequal_values_2(self, mock_series):
        mock_series.side_effect = lambda *args: args
        # given
        x_values = [1]
        y_values = [
            [0, 1, 2],
        ]
        x_axis = "x"
        y_axis = "y"
        series_names = []
        bar_width = 1
        bar_gap = 1
        # when
        # then
        with self.assertRaises(ValueError):
            no_series_constructor(
                x_values,
                y_values,
                x_axis,
                y_axis,
                series_names,
                bar_width,
                bar_gap,
            )

    @patch("pysvgchart.charts.Series")
    def test_one_series(self, mock_series):
        mock_series.side_effect = lambda *args: args
        # given
        x_values = [1, 2, 3]
        y_values = [
            [0, 1, 2],
        ]
        x_axis = "x"
        y_axis = "y"
        series_names = ["a"]
        bar_width = 1
        bar_gap = 1
        # when
        actual = no_series_constructor(
            x_values,
            y_values,
            x_axis,
            y_axis,
            series_names,
            bar_width,
            bar_gap,
        )
        # then
        expect = [
            call(1, 0),
        ]
        self.assertListEqual(expect, mock_series.mock_calls)
        expect = {
            "a": (1, 0),
        }
        self.assertDictEqual(expect, actual)

    @patch("pysvgchart.charts.Series")
    def test_some_series(self, mock_series):
        mock_series.side_effect = lambda *args: args
        # given
        x_values = [1, 2, 3]
        y_values = [
            [0, 1, 2],
            [1, 2, 3],
            [3, 4, 5],
        ]
        x_axis = "x"
        y_axis = "y"
        series_names = ["a", "b", "c"]
        bar_width = 1
        bar_gap = 1
        # when
        actual = no_series_constructor(
            x_values,
            y_values,
            x_axis,
            y_axis,
            series_names,
            bar_width,
            bar_gap,
        )
        # then
        expect = [
            call(1, 0),
            call(1, 1),
            call(1, 3),
        ]
        self.assertListEqual(expect, mock_series.mock_calls)
        expect = {
            "a": (1, 0),
            "b": (1, 1),
            "c": (1, 3),
        }
        self.assertDictEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
