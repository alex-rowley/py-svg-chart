import unittest
from unittest.mock import patch, call, MagicMock


from pysvgchart.charts import bar_series_constructor


def echo(*args, **kwargs):
    if args and kwargs:
        return args, kwargs
    if args:
        return args
    if kwargs:
        return kwargs
    return None


class TestBarSeriesConstructor(unittest.TestCase):
    """
    test the bar_series_constructor() function
    """

    def setUp(self) -> None:
        self.maxDiff = None

    @patch("pysvgchart.charts.Point")
    @patch("pysvgchart.charts.BarSeries")
    def test_no_series(self, mock_bar_series, mock_point):
        mock_bar_series.side_effect = echo
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
        actual = bar_series_constructor(
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
        self.assertListEqual(expect, mock_bar_series.mock_calls)
        expect = {}
        self.assertDictEqual(expect, actual)

    @patch("pysvgchart.charts.Point")
    @patch("pysvgchart.charts.BarSeries")
    def test_too_many_names(self, mock_bar_series, mock_point):
        mock_bar_series.side_effect = echo
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
            bar_series_constructor(
                x_values,
                y_values,
                x_axis,
                y_axis,
                series_names,
                bar_width,
                bar_gap,
            )

    @patch("pysvgchart.charts.Point")
    @patch("pysvgchart.charts.BarSeries")
    def test_too_few_names(self, mock_bar_series, mock_point):
        mock_bar_series.side_effect = echo
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
            bar_series_constructor(
                x_values,
                y_values,
                x_axis,
                y_axis,
                series_names,
                bar_width,
                bar_gap,
            )

    @patch("pysvgchart.charts.Point")
    @patch("pysvgchart.charts.BarSeries")
    def test_unequal_values_1(self, mock_bar_series, mock_point):
        mock_bar_series.side_effect = echo
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
            bar_series_constructor(
                x_values,
                y_values,
                x_axis,
                y_axis,
                series_names,
                bar_width,
                bar_gap,
            )

    @patch("pysvgchart.charts.Point")
    @patch("pysvgchart.charts.BarSeries")
    def test_unequal_values_2(self, mock_bar_series, mock_point):
        mock_bar_series.side_effect = echo
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
            bar_series_constructor(
                x_values,
                y_values,
                x_axis,
                y_axis,
                series_names,
                bar_width,
                bar_gap,
            )

    @patch("pysvgchart.charts.Point")
    @patch("pysvgchart.charts.BarSeries")
    def test_one_series(self, mock_bar_series, mock_point):
        mock_bar_series.side_effect = echo
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
        y_axis.position.y = 1000
        y_axis.length = 100
        series_names = ["a"]
        bar_width = 1
        bar_gap = 1
        # when
        actual = bar_series_constructor(
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
                points=[(10.0, 10), (20.0, 21), (30.0, 32)],
                x_values=[1, 2, 3],
                y_values=[0, 1, 2],
                bar_heights=[1090, 1079, 1068],  # 1100 - point.y
                bar_width=1,
            ),
        ]
        self.assertListEqual(expect, mock_bar_series.mock_calls)
        expect = {
            "a": dict(
                    points=[(10.0, 10), (20.0, 21), (30.0, 32)],
                    x_values=[1, 2, 3],
                    y_values=[0, 1, 2],
                    bar_heights=[1090, 1079, 1068],
                    bar_width=1,
            ),
        }
        self.assertDictEqual(expect, actual)

    @patch("pysvgchart.charts.Point")
    @patch("pysvgchart.charts.BarSeries")
    def test_some_series(self, mock_bar_series, mock_point):
        mock_bar_series.side_effect = echo
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
        y_axis.position.y = 1000
        y_axis.length = 100
        series_names = ["a", "b", "c"]
        bar_width = 1
        bar_gap = 1
        # when
        actual = bar_series_constructor(
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
            call(8.0, 10),
            call(18.0, 21),
            call(28.0, 32),
            # series "b"
            call(10.0, 11),
            call(20.0, 22),
            call(30.0, 33),
            # series "c"
            call(12.0, 13),
            call(22.0, 24),
            call(32.0, 35),
        ]
        self.assertListEqual(expect, mock_point.mock_calls)
        expect = [
            # series "a"
            call(
                points=[(8.0, 10), (18.0, 21), (28.0, 32)],
                x_values=[1, 2, 3],
                y_values=[0, 1, 2],
                bar_heights=[1090, 1079, 1068],  # 1100 - point.y
                bar_width=1,
            ),
            # series "b"
            call(
                points=[(10.0, 11), (20.0, 22), (30.0, 33)],
                x_values=[1, 2, 3],
                y_values=[1, 2, 3],
                bar_heights=[1089, 1078, 1067],  # 1100 - point.y
                bar_width=1,
            ),
            # series "c"
            call(
                points=[(12.0, 13), (22.0, 24), (32.0, 35)],
                x_values=[1, 2, 3],
                y_values=[3, 4, 5],
                bar_heights=[1087, 1076, 1065],  # 1100 - point.y
                bar_width=1,
            ),
        ]
        self.assertListEqual(expect, mock_bar_series.mock_calls)
        expect = {
            "a": dict(
                points=[(8.0, 10), (18.0, 21), (28.0, 32)],
                x_values=[1, 2, 3],
                y_values=[0, 1, 2],
                bar_heights=[1090, 1079, 1068],
                bar_width=1,
            ),
            "b": dict(
                points=[(10.0, 11), (20.0, 22), (30.0, 33)],
                x_values=[1, 2, 3],
                y_values=[1, 2, 3],
                bar_heights=[1089, 1078, 1067],
                bar_width=1,
            ),
            "c": dict(
                points=[(12.0, 13), (22.0, 24), (32.0, 35)],
                x_values=[1, 2, 3],
                y_values=[3, 4, 5],
                bar_heights=[1087, 1076, 1065],
                bar_width=1,
            ),
        }
        self.assertDictEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
