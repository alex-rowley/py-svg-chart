from datetime import datetime, date
import unittest


from pysvgchart.axes import YAxis


class TestYAxisGetPositions(unittest.TestCase):
    """
    test the get_positions()and get_ticks_positions() functions of the YAxis class
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

    def check_axis(self, y_axis, values, ticks):
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
        expect = [t for t in ticks]
        self.assertListEqual(expect, y_axis.get_ticks_with_positions())

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
        ticks = (
            (date(2000, 1, 1), 100.0),
            (date(2000, 1, 2), 66.66666666666667),
            (date(2000, 1, 3), 33.333333333333336),
            (date(2000, 1, 4), 0.0),
        )
        # when
        # then
        self.check_axis(y_axis, values, ticks)

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
        ticks = (
            (datetime(2000, 1, 1, 11, 11, 0), 100.0),
            (datetime(2000, 1, 2, 11, 11, 0), 75.0),
            (datetime(2000, 1, 3, 11, 11, 0), 50.0),
            (datetime(2000, 1, 4, 11, 11, 0), 25.0),
            (datetime(2000, 1, 5, 11, 11, 0), 0.0),
        )
        # when
        # then
        self.check_axis(y_axis, values, ticks)

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
        ticks = (
            (date(2000, 8, 1), 100.0),
            (date(2001, 8, 1), 90.91361712720936),
            (date(2002, 8, 1), 81.82723425441873),
            (date(2003, 8, 1), 72.74085138162808),
            (date(2004, 8, 1), 63.62957430918597),
            (date(2005, 8, 1), 54.54319143639532),
            (date(2006, 8, 1), 45.45680856360468),
            (date(2007, 8, 1), 36.370425690814045),
            (date(2008, 8, 1), 27.25914861837192),
            (date(2009, 8, 1), 18.172765745581277),
            (date(2010, 8, 1), 9.086382872790644),
            (date(2011, 8, 1), 0.0),
        )
        # when
        # then
        self.check_axis(y_axis, values, ticks)

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
        ticks = (
            (datetime(2000, 8, 1, 0, 0, 0), 100.0),
            (datetime(2001, 8, 1, 0, 0, 0), 90.91361712720936),
            (datetime(2002, 8, 1, 0, 0, 0), 81.82723425441873),
            (datetime(2003, 8, 1, 0, 0, 0), 72.74085138162808),
            (datetime(2004, 8, 1, 0, 0, 0), 63.62957430918597),
            (datetime(2005, 8, 1, 0, 0, 0), 54.54319143639532),
            (datetime(2006, 8, 1, 0, 0, 0), 45.45680856360468),
            (datetime(2007, 8, 1, 0, 0, 0), 36.370425690814045),
            (datetime(2008, 8, 1, 0, 0, 0), 27.25914861837192),
            (datetime(2009, 8, 1, 0, 0, 0), 18.172765745581277),
            (datetime(2010, 8, 1, 0, 0, 0), 9.086382872790644),
            (datetime(2011, 8, 1, 0, 0, 0), 0.0),
        )
        # when
        # then
        self.check_axis(y_axis, values, ticks)

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
        ticks = (
            (42, 100.0),
            (44, 66.66666666666667),
            (46, 33.333333333333336),
            (48, 0.0),
        )
        # when
        # then
        self.check_axis(y_axis, values, ticks)

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
        ticks = (
            (42.0, 100.0),
            (43.0, 83.33333333333334),
            (44.0, 66.66666666666667),
            (45.0, 50.0),
            (46.0, 33.333333333333336),
            (47.0, 16.666666666666664),
            (48.0, 0.0),
        )
        # when
        # then
        self.check_axis(y_axis, values, ticks)

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
        ticks = (
            (2.6, 100.0),
            (2.8, 66.66666666666671),
            (3.0, 33.33333333333336),
            (3.2, 0.0),
        )
        # when
        # then
        self.check_axis(y_axis, values, ticks)

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
        ticks = (
            (2.7, 100.0),
            (2.75, 88.88888888888891),
            (2.8, 77.77777777777784),
            (2.85, 66.66666666666667),
            (2.9, 55.55555555555558),
            (2.95, 44.44444444444441),
            (3.0, 33.333333333333336),
            (3.05, 22.222222222222253),
            (3.1, 11.111111111111082),
            (3.15, 0.0),
        )
        # when
        # then
        self.check_axis(y_axis, values, ticks)

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
        ticks = (
            (0, 100.0),
            (500, 50.0),
            (1000, 0.0),
        )
        # when
        # then
        self.check_axis(y_axis, values, ticks)

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
        ticks=(
            (0, 100.0),
            (100, 85.71428571428572),
            (200, 71.42857142857143),
            (300, 57.14285714285714),
            (400, 42.85714285714286),
            (500, 28.57142857142857),
            (600, 14.28571428571429),
            (700, 0.0),
        )
        # when
        # then
        self.check_axis(y_axis, values, ticks)

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
        ticks=(
            (0, 100.0),
            (5000, 50.0),
            (10000, 0.0),
        )
        # when
        # then
        self.check_axis(y_axis, values, ticks)

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
        ticks=(
            (0, 100.0),
            (1000, 85.71428571428572),
            (2000, 71.42857142857143),
            (3000, 57.14285714285714),
            (4000, 42.85714285714286),
            (5000, 28.57142857142857),
            (6000, 14.28571428571429),
            (7000, 0.0),
        )
        # when
        # then
        self.check_axis(y_axis, values, ticks)


if __name__ == '__main__':
    unittest.main()
