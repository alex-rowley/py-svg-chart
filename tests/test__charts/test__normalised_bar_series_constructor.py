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
            [0, 1, 2],
            [1, 2, 3],
            [3, 7, 5],
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
            call(10, 10),
            call(20, 20.1),
            call(30, 30.2),
            # series "b"
            call(10, 10.25),
            call(20, 20.3),
            call(30, 30.5),
            # series "c"
            call(10, 11.0),
            call(20, 21.0),
            call(30, 31.0),
        ]
        self.assertListEqual(expect, mock_point.mock_calls)
        expect = [
            # series "a"
            call(
                points=[(10, 10.0), (20, 20.1), (30, 30.2)],
                x_values=[1, 2, 3],
                y_values=[0, 1, 2],
                bar_heights=[0.0, -0.10000000000000142, -0.1999999999999993],
                bar_width=1,
            ),
            # series "b"
            call(
                points=[(10, 10.25), (20, 20.3), (30, 30.5)],
                x_values=[1, 2, 3],
                y_values=[1, 2, 3],
                bar_heights=[-0.25, -0.1999999999999993, -0.3000000000000007],
                bar_width=1,
            ),
            # series "c"
            call(
                points=[(10, 11.0), (20, 21.0), (30, 31.0)],
                x_values=[1, 2, 3],
                y_values=[3, 7, 5],
                bar_heights=[-0.75, -0.6999999999999993, -0.5],
                bar_width=1,
            ),
        ]
        self.assertListEqual(expect, mock_bar_series.mock_calls)
        expect = {
            "a": dict(
                points=[(10, 10), (20, 20.1), (30, 30.2)],
                x_values=[1, 2, 3],
                y_values=[0, 1, 2],
                bar_heights=[0.0, -0.10000000000000142, -0.1999999999999993],
                bar_width=1,
            ),
            "b": dict(
                points=[(10, 10.25), (20, 20.3), (30, 30.5)],
                x_values=[1, 2, 3],
                y_values=[1, 2, 3],
                bar_heights=[-0.25, -0.1999999999999993, -0.3000000000000007],
                bar_width=1,
            ),
            "c": dict(
                points=[(10, 11.0), (20, 21.0), (30, 31.0)],
                x_values=[1, 2, 3],
                y_values=[3, 7, 5],
                bar_heights=[-0.75, -0.6999999999999993, -0.5],
                bar_width=1,
            ),
        }
        self.assertDictEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
