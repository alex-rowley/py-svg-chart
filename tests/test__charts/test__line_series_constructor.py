import unittest
from unittest.mock import patch, call, MagicMock


from pysvgchart.charts import line_series_constructor


def echo(*args, **kwargs):
    if args and kwargs:
        return args, kwargs
    if args:
        return args
    if kwargs:
        return kwargs
    return None


class TestLineSeriesConstructor(unittest.TestCase):
    """
    test the line_series_constructor() function
    """

    def setUp(self) -> None:
        self.maxDiff = None

    @patch("pysvgchart.charts.Point")
    @patch("pysvgchart.charts.LineSeries")
    def test_no_series(self, mock_line_series, mock_point):
        mock_line_series.side_effect = echo
        mock_point.side_effect = echo
        # given
        x_values = [1, 2, 3]
        y_values = []
        x_axis = MagicMock()
        x_axis.get_positions.return_value = [10, 20, 30]
        y_axis = MagicMock()
        y_axis.get_positions.side_effect = lambda yyy: list(map(lambda v: v[0] + v[1], zip(yyy, [10, 20, 30])))
        series_names = []
        bar_width = 1
        bar_gap = 1
        # when
        actual = line_series_constructor(
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
        self.assertListEqual(expect, mock_point.mock_calls)
        expect = []
        self.assertListEqual(expect, mock_line_series.mock_calls)
        expect = {}
        self.assertDictEqual(expect, actual)

    @patch("pysvgchart.charts.Point")
    @patch("pysvgchart.charts.LineSeries")
    def test_too_many_names(self, mock_line_series, mock_point):
        mock_line_series.side_effect = echo
        mock_point.side_effect = echo
        # given
        x_values = [1, 2, 3]
        y_values = []
        x_axis = MagicMock()
        x_axis.get_positions.return_value = [10, 20, 30]
        y_axis = MagicMock()
        y_axis.get_positions.side_effect = lambda yyy: list(map(lambda v: v[0] + v[1], zip(yyy, [10, 20, 30])))
        series_names = ["a", "b", "c"]
        bar_width = 1
        bar_gap = 1
        # when
        # then
        with self.assertRaises(ValueError):
            line_series_constructor(
                x_values,
                y_values,
                x_axis,
                y_axis,
                series_names,
                bar_width,
                bar_gap,
            )

    @patch("pysvgchart.charts.Point")
    @patch("pysvgchart.charts.LineSeries")
    def test_too_few_names(self, mock_line_series, mock_point):
        mock_line_series.side_effect = echo
        mock_point.side_effect = echo
        # given
        x_values = [1, 2, 3]
        y_values = [
            [0, 1, 2],
        ]
        x_axis = MagicMock()
        x_axis.get_positions.return_value = [10, 20, 30]
        y_axis = MagicMock()
        y_axis.get_positions.side_effect = lambda yyy: list(map(lambda v: v[0] + v[1], zip(yyy, [10, 20, 30])))
        series_names = []
        bar_width = 1
        bar_gap = 1
        # when
        # then
        with self.assertRaises(ValueError):
            line_series_constructor(
                x_values,
                y_values,
                x_axis,
                y_axis,
                series_names,
                bar_width,
                bar_gap,
            )

    @patch("pysvgchart.charts.Point")
    @patch("pysvgchart.charts.LineSeries")
    def test_one_series(self, mock_line_series, mock_point):
        mock_line_series.side_effect = echo
        mock_point.side_effect = echo
        # given
        x_values = [1, 2, 3]
        y_values = [
            [0, 1, 2],
        ]
        x_axis = MagicMock()
        x_axis.get_positions.return_value = [10, 20, 30]
        y_axis = MagicMock()
        y_axis.get_positions.side_effect = lambda yyy: list(map(lambda v: v[0] + v[1], zip(yyy, [10, 20, 30])))
        series_names = ["a"]
        bar_width = 1
        bar_gap = 1
        # when
        actual = line_series_constructor(
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
            call(10, 10),
            call(20, 21),
            call(30, 32),
        ]
        self.assertListEqual(expect, mock_point.mock_calls)
        expect = [
            call(
                points=[(10, 10), (20, 21), (30, 32)],
                x_values=[1, 2, 3],
                y_values=[0, 1, 2],
            ),
        ]
        self.assertListEqual(expect, mock_line_series.mock_calls)
        expect = {
            "a": dict(
                    points=[(10, 10), (20, 21), (30, 32)],
                    x_values=[1, 2, 3],
                    y_values=[0, 1, 2],
            ),
        }
        self.assertDictEqual(expect, actual)

    @patch("pysvgchart.charts.Point")
    @patch("pysvgchart.charts.LineSeries")
    def test_some_series(self, mock_line_series, mock_point):
        mock_line_series.side_effect = echo
        mock_point.side_effect = echo
        # given
        x_values = [1, 2, 3]
        y_values = [
            [0, 1, 2],
            [1, 2, 3],
            [3, 4, 5],
        ]
        x_axis = MagicMock()
        x_axis.get_positions.return_value = [10, 20, 30]
        y_axis = MagicMock()
        y_axis.get_positions.side_effect = lambda yyy: list(map(lambda v: v[0] + v[1], zip(yyy, [10, 20, 30])))
        series_names = ["a", "b", "c"]
        bar_width = 1
        bar_gap = 1
        # when
        actual = line_series_constructor(
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
            # series "a"
            call(10, 10),
            call(20, 21),
            call(30, 32),
            # series "b"
            call(10, 11),
            call(20, 22),
            call(30, 33),
            # series "c"
            call(10, 13),
            call(20, 24),
            call(30, 35),
        ]
        self.assertListEqual(expect, mock_point.mock_calls)
        expect = [
            # series "a"
            call(
                points=[(10, 10), (20, 21), (30, 32)],
                x_values=[1, 2, 3],
                y_values=[0, 1, 2],
            ),
            # series "b"
            call(
                points=[(10, 11), (20, 22), (30, 33)],
                x_values=[1, 2, 3],
                y_values=[1, 2, 3],
            ),
            # series "c"
            call(
                points=[(10, 13), (20, 24), (30, 35)],
                x_values=[1, 2, 3],
                y_values=[3, 4, 5],
            ),
        ]
        self.assertListEqual(expect, mock_line_series.mock_calls)
        expect = {
            "a": dict(
                    points=[(10, 10), (20, 21), (30, 32)],
                    x_values=[1, 2, 3],
                    y_values=[0, 1, 2],
            ),
            "b": dict(
                points=[(10, 11), (20, 22), (30, 33)],
                x_values=[1, 2, 3],
                y_values=[1, 2, 3],
            ),
            "c": dict(
                points=[(10, 13), (20, 24), (30, 35)],
                x_values=[1, 2, 3],
                y_values=[3, 4, 5],
            ),
        }
        self.assertDictEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
