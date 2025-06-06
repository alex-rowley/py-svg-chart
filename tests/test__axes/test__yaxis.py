from datetime import datetime, date
import unittest


from pysvgchart.axes import YAxis
from pysvgchart.shapes import Line, Text


class TestYAxisGetPositions(unittest.TestCase):
    """
    test the get_positions() function of the YAxis class
    """

    def setUp(self):
        self.maxDiff = None

    @staticmethod
    def y_axis(data_points, max_ticks=10):
        return YAxis(
            x_position = 0,
            y_position = 0,
            data_points = data_points,
            axis_length = 100,
            label_format = str,
            max_ticks=max_ticks,
        )

    def check_axis(self, y_axis, values):
        # given - y_axis and values
        # when
        actual = [y for _, y in y_axis.get_ticks_with_positions()]  # discard ticks, keep position
        # then
        expect = [y for y, _ in values]
        self.assertListEqual(expect, actual)
        expect = [
            [f'<line x1="-5" y1="{y}" x2="0" y2="{y}" stroke="#2e2e2c"/>']
            for y, _ in values
        ]
        self.assertListEqual(expect, [y.get_element_list() for y in y_axis.tick_lines])
        expect = [
            [f'<text x="-10" y="{y}" text-anchor="end" dominant-baseline="middle">{t}</text>']
            for y, t in values
        ]
        self.assertListEqual(expect, [y.get_element_list() for y in y_axis.tick_texts])

    def test_two_dates_about_a_month(self):
        """
        between 1 day and 1 month
        """
        # given
        y_axis = self.y_axis(
            [
                date(2000, 1, 1),
                date(2000, 1, 4),
            ],
        )
        values = (
            (100.0, "2000-01-01"),
            (66.66666666666667, "2000-01-02"),
            (33.333333333333336, "2000-01-03"),
            (0.0, "2000-01-04"),
        )
        # when
        # then
        self.check_axis(y_axis, values)

    def test_two_datetimes_about_a_month(self):
        """
        between 1 day and 1 month
        """
        # given
        y_axis = self.y_axis(
            [
                datetime(2000, 1, 1, 11, 11, 11),
                datetime(2000, 1, 4, 14, 14, 14),
            ],
        )
        values = (
            (100.0, "2000-01-01 11:11:00"),
            (75.0, "2000-01-02 11:11:00"),
            (50.0, "2000-01-03 11:11:00"),
            (25.0, "2000-01-04 11:11:00"),
            (0.0, "2000-01-05 11:11:00"),
        )
        # when
        # then
        self.check_axis(y_axis, values)

    def test_two_dates_decades_apart(self):
        """
        > 10 years -> years increment, day on 1
        """
        # given
        y_axis = self.y_axis(
            [
                date(2000, 8, 3),
                date(2011, 4, 24),
            ]
        )
        values = (
            (100.0, "2000-08-01"),
            (90.91361712720936, "2001-08-01"),
            (81.82723425441873, "2002-08-01"),
            (72.74085138162808, "2003-08-01"),
            (63.62957430918597, "2004-08-01"),
            (54.54319143639532, "2005-08-01"),
            (45.45680856360468, "2006-08-01"),
            (36.370425690814045, "2007-08-01"),
            (27.25914861837192, "2008-08-01"),
            (18.172765745581277, "2009-08-01"),
            (9.086382872790644, "2010-08-01"),
            (0.0, "2011-08-01"),
        )
        # when
        # then
        self.check_axis(y_axis, values)

    def test_two_datetimes_decades_apart(self):
        """
        > 10 years -> years increment, day on 1, time on 00:00:00
        """
        # given
        y_axis = self.y_axis(
            [
                datetime(2000, 8, 3, 11, 11, 11),
                datetime(2011, 4, 24, 14, 14, 14),
            ]
        )
        values = (
            (100.0, "2000-08-01 00:00:00"),
            (90.91361712720936, "2001-08-01 00:00:00"),
            (81.82723425441873, "2002-08-01 00:00:00"),
            (72.74085138162808, "2003-08-01 00:00:00"),
            (63.62957430918597, "2004-08-01 00:00:00"),
            (54.54319143639532, "2005-08-01 00:00:00"),
            (45.45680856360468, "2006-08-01 00:00:00"),
            (36.370425690814045, "2007-08-01 00:00:00"),
            (27.25914861837192, "2008-08-01 00:00:00"),
            (18.172765745581277, "2009-08-01 00:00:00"),
            (9.086382872790644, "2010-08-01 00:00:00"),
            (0.0, "2011-08-01 00:00:00"),
        )
        # when
        # then
        self.check_axis(y_axis, values)

    def test_two_close_ints_few_ticks(self):
        # given
        y_axis = self.y_axis(
            [
                42,
                48,
            ],
            max_ticks=3,
        )
        values = (
            (100.0, "42"),
            (66.66666666666667, "44"),
            (33.333333333333336, "46"),
            (0.0, "48"),
        )
        # when
        # then
        self.check_axis(y_axis, values)

    def test_two_close_ints_more_ticks(self):
        # given
        y_axis = self.y_axis(
            [
                42,
                48,
            ],
            max_ticks=10,
        )
        values = (
            (100.0, "42.0"),
            (83.33333333333334, "43.0"),
            (66.66666666666667, "44.0"),
            (50.0, "45.0"),
            (33.333333333333336, "46.0"),
            (16.666666666666664, "47.0"),
            (0.0, "48.0"),
        )
        # when
        # then
        self.check_axis(y_axis, values)

    def test_two_close_floats_few_ticks(self):
        # given
        y_axis = self.y_axis(
            [
                2.71828182845904523536,
                3.14159265358979323846,
            ],
            max_ticks=3,
        )
        values = (
            (100.0, "2.6"),
            (66.66666666666671, "2.8"),
            (33.33333333333336, "3.0"),
            (0.0, "3.2"),
        )
        # when
        # then
        self.check_axis(y_axis, values)

    def test_two_close_floats_more_ticks(self):
        # given
        y_axis = self.y_axis(
            [
                2.71828182845904523536,
                3.14159265358979323846,
            ],
            max_ticks=10,
        )
        values = (
            (100.0, "2.7"),
            (88.88888888888891, "2.75"),
            (77.77777777777784, "2.8"),
            (66.66666666666667, "2.85"),
            (55.55555555555558, "2.9"),
            (44.44444444444441, "2.95"),
            (33.333333333333336, "3.0"),
            (22.222222222222253, "3.05"),
            (11.111111111111082, "3.1"),
            (0.0, "3.15"),
        )
        # when
        # then
        self.check_axis(y_axis, values)

    def test_two_far_ints_few_ticks(self):
        # given
        y_axis = self.y_axis(
            [
                42,
                666,
            ],
            max_ticks=3,
        )
        values = (
            (100.0, "0"),
            (50.0, "500"),
            (0.0, "1000"),
        )
        # when
        # then
        self.check_axis(y_axis, values)

    def test_two_far_ints_more_ticks(self):
        # given
        y_axis = self.y_axis(
            [
                42,
                666,
            ],
            max_ticks=10,
        )
        values = (
            (100.0, "0"),
            (85.71428571428572, "100"),
            (71.42857142857143, "200"),
            (57.14285714285714, "300"),
            (42.85714285714286, "400"),
            (28.57142857142857, "500"),
            (14.28571428571429, "600"),
            (0.0, "700"),
        )
        # when
        # then
        self.check_axis(y_axis, values)

    def test_two_far_floats_few_ticks(self):
        # given
        y_axis = self.y_axis(
            [
                0.4,
                6553.6,
            ],
            max_ticks=3,
        )
        values = (
            (100.0, "0"),
            (50.0, "5000"),
            (0.0, "10000"),
        )
        # when
        # then
        self.check_axis(y_axis, values)

    def test_two_far_floats_more_ticks(self):
        # given
        y_axis = self.y_axis(
            [
                0.4,
                6553.6,
            ],
            max_ticks=10,
        )
        values = (
            (100.0, "0"),
            (85.71428571428572, "1000"),
            (71.42857142857143, "2000"),
            (57.14285714285714, "3000"),
            (42.85714285714286, "4000"),
            (28.57142857142857, "5000"),
            (14.28571428571429, "6000"),
            (0.0, "7000"),
        )
        # when
        # then
        self.check_axis(y_axis, values)


if __name__ == '__main__':
    unittest.main()
