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
    def test_unequal_values_1(self, mock_line_series, mock_point):
        mock_line_series.side_effect = echo
        mock_point.side_effect = echo
        # given
        x_values = [1, 2, 3]
        y_values = [
            [0],
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
    def test_unequal_values_2(self, mock_line_series, mock_point):
        mock_line_series.side_effect = echo
        mock_point.side_effect = echo
        # given
        x_values = [1]
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
            call(x=10, y=10),
            call(x=20, y=21),
            call(x=30, y=32),
        ]
        self.assertListEqual(expect, mock_point.mock_calls)
        expect = [
            call(
                points=[
                    {"x": 10, "y": 10},
                    {"x": 20, "y": 21},
                    {"x": 30, "y": 32},
                ],
                x_values=[1, 2, 3],
                y_values=[0, 1, 2],
            ),
        ]
        self.assertListEqual(expect, mock_line_series.mock_calls)
        expect = {
            "a": dict(
                points=[
                    {"x": 10, "y": 10},
                    {"x": 20, "y": 21},
                    {"x": 30, "y": 32},
                ],
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
            call(x=10, y=10),
            call(x=20, y=21),
            call(x=30, y=32),
            # series "b"
            call(x=10, y=11),
            call(x=20, y=22),
            call(x=30, y=33),
            # series "c"
            call(x=10, y=13),
            call(x=20, y=24),
            call(x=30, y=35),
        ]
        self.assertListEqual(expect, mock_point.mock_calls)
        expect = [
            # series "a"
            call(
                points=[
                    {"x": 10, "y": 10},
                    {"x": 20, "y": 21},
                    {"x": 30, "y": 32},
                ],
                x_values=[1, 2, 3],
                y_values=[0, 1, 2],
            ),
            # series "b"
            call(
                points=[
                    {"x": 10, "y": 11},
                    {"x": 20, "y": 22},
                    {"x": 30, "y": 33},
                ],
                x_values=[1, 2, 3],
                y_values=[1, 2, 3],
            ),
            # series "c"
            call(
                points=[
                    {"x": 10, "y": 13},
                    {"x": 20, "y": 24},
                    {"x": 30, "y": 35},
                ],
                x_values=[1, 2, 3],
                y_values=[3, 4, 5],
            ),
        ]
        self.assertListEqual(expect, mock_line_series.mock_calls)
        expect = {
            "a": dict(
                points=[
                    {"x": 10, "y": 10},
                    {"x": 20, "y": 21},
                    {"x": 30, "y": 32},
                ],
                x_values=[1, 2, 3],
                y_values=[0, 1, 2],
            ),
            "b": dict(
                points=[
                    {"x": 10, "y": 11},
                    {"x": 20, "y": 22},
                    {"x": 30, "y": 33},
                ],
                x_values=[1, 2, 3],
                y_values=[1, 2, 3],
            ),
            "c": dict(
                points=[
                    {"x": 10, "y": 13},
                    {"x": 20, "y": 24},
                    {"x": 30, "y": 35},
                ],
                x_values=[1, 2, 3],
                y_values=[3, 4, 5],
            ),
        }
        self.assertDictEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
