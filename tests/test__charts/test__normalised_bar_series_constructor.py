import unittest
from unittest.mock import patch, call, MagicMock


from pysvgchart.charts import normalised_bar_series_constructor


def echo(*args, **kwargs):
    if args and kwargs:
        return args, kwargs
    if args:
        return args
    if kwargs:
        return kwargs
    return None


class TestNormalisedBarSeriesConstructor(unittest.TestCase):
    """
    test the normalised_bar_series_constructor() function
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
        y_axis.position.y = 1000
        y_axis.length = 100
        series_names = []
        bar_width = 1
        bar_gap = 1
        # when
        # then
        with self.assertRaises(ValueError):
            normalised_bar_series_constructor(
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
        y_axis.position.y = 1000
        y_axis.length = 100
        series_names = ["a", "b", "c"]
        bar_width = 1
        bar_gap = 1
        # when
        # then
        with self.assertRaises(ValueError):
            normalised_bar_series_constructor(
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
        y_axis.position.y = 1000
        y_axis.length = 100
        series_names = []
        bar_width = 1
        bar_gap = 1
        # when
        # then
        with self.assertRaises(ValueError):
            normalised_bar_series_constructor(
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
        y_axis.position.y = 1000
        y_axis.length = 100
        series_names = []
        bar_width = 1
        bar_gap = 1
        # when
        # then
        with self.assertRaises(ValueError):
            normalised_bar_series_constructor(
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
        y_axis.position.y = 1000
        y_axis.length = 100
        series_names = []
        bar_width = 1
        bar_gap = 1
        # when
        # then
        with self.assertRaises(ValueError):
            normalised_bar_series_constructor(
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
        actual = normalised_bar_series_constructor(
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
            call(20, 21.0),
            call(30, 31.0),
        ]
        self.assertListEqual(expect, mock_point.mock_calls)
        expect = [
            call(
                points=[(10, 10), (20, 21.0), (30, 31.0)],
                x_values=[1, 2, 3],
                y_values=[0, 1, 2],
                bar_heights=[0, -1.0, -1.0],
                bar_width=1,
            ),
        ]
        self.assertListEqual(expect, mock_bar_series.mock_calls)
        expect = {
            "a": dict(
                    points=[(10, 10), (20, 21.0), (30, 31.0)],
                    x_values=[1, 2, 3],
                    y_values=[0, 1, 2],
                    bar_heights=[0, -1.0, -1.0],
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
            [1, 1, 0],
            [1, 1, 2],
            [1, 2, 2],
            [1, 4, 4],
        ]
        x_axis = MagicMock()
        x_axis.get_positions.return_value = [10, 20, 30]
        y_axis = MagicMock()
        y_axis.get_positions.side_effect = lambda yyy: list(map(lambda v: v[0] + v[1], zip(yyy, [10, 20, 30])))
        y_axis.position.y = 1000
        y_axis.length = 100
        series_names = ["a", "b", "c", "d"]
        bar_width = 1
        bar_gap = 1
        # when
        actual = normalised_bar_series_constructor(
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
            call(10, 10.250),
            call(20, 20.125),
            call(30, 30.000),
            # series "b"
            call(10, 10.500),
            call(20, 20.250),
            call(30, 30.250),
            # series "c"
            call(10, 10.750),
            call(20, 20.500),
            call(30, 30.500),
            # series "d"
            call(10, 11.0),
            call(20, 21.0),
            call(30, 31.0),
        ]
        self.assertListEqual(expect, mock_point.mock_calls)
        expect = [
            # series "a"
            call(
                points=[(10, 10.250), (20, 20.125), (30, 30.000)],
                x_values=[1, 2, 3],
                y_values=[1, 1, 0],
                bar_heights=[-0.250, -0.125, 0.000],
                bar_width=1,
            ),
            # series "b"
            call(
                points=[(10, 10.500), (20, 20.250), (30, 30.250)],
                x_values=[1, 2, 3],
                y_values=[1, 1, 2],
                bar_heights=[-0.250, -0.125, -0.250],
                bar_width=1,
            ),
            # series "c"
            call(
                points=[(10, 10.750), (20, 20.500), (30, 30.500)],
                x_values=[1, 2, 3],
                y_values=[1, 2, 2],
                bar_heights=[-0.250, -0.250, -0.250],
                bar_width=1,
            ),
            # series "d"
            call(
                points=[(10, 11.0), (20, 21.0), (30, 31.0)],
                x_values=[1, 2, 3],
                y_values=[1, 4, 4],
                bar_heights=[-0.250, -0.500, -0.500],
                bar_width=1,
            ),
        ]
        self.assertListEqual(expect, mock_bar_series.mock_calls)
        expect = {
            "a": dict(
                points=[(10, 10.250), (20, 20.125), (30, 30.000)],
                x_values=[1, 2, 3],
                y_values=[1, 1, 0],
                bar_heights=[-0.250, -0.125, 0.000],
                bar_width=1,
            ),
            "b": dict(
                points=[(10, 10.500), (20, 20.250), (30, 30.250)],
                x_values=[1, 2, 3],
                y_values=[1, 1, 2],
                bar_heights=[-0.250, -0.125, -0.250],
                bar_width=1,
            ),
            "c": dict(
                points=[(10, 10.750), (20, 20.500), (30, 30.500)],
                x_values=[1, 2, 3],
                y_values=[1, 2, 2],
                bar_heights=[-0.250, -0.250, -0.250],
                bar_width=1,
            ),
            "d": dict(
                points=[(10, 11.0), (20, 21.0), (30, 31.0)],
                x_values=[1, 2, 3],
                y_values=[1, 4, 4],
                bar_heights=[-0.250, -0.500, -0.500],
                bar_width=1,
            ),
        }
        self.assertDictEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
