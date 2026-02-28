from datetime import datetime, date
import unittest


from pysvgchart.axes import XAxis


class TestXAxisGetPositions(unittest.TestCase):
    """
    test the get_positions() and get_ticks_positions() functions of the XAxis class
    """

    def setUp(self):
        self.maxDiff = None

    @staticmethod
    def x_axis(data_points, max_ticks=10):
        return XAxis(
            x_position = 0,
            y_position = 0,
            data_points = data_points,
            axis_length = 100,
            label_format = str,
            max_ticks=max_ticks,
        )

    def check_axis(self, x_axis, values, ticks):
        # given - x_axis and values
        # when
        actual = [x for _, x in x_axis.get_ticks_with_positions()]  # discard ticks, keep position
        # then
        expect = [x for x, _ in values]
        self.assertListEqual(expect, actual)
        expect = [
            [f'<line x1="{x}" y1="0" x2="{x}" y2="5" stroke="#2e2e2c"/>']
            for x, _ in values
        ]
        self.assertListEqual(expect, [x.get_element_list() for x in x_axis.tick_lines])
        expect = [
            [f'<text x="{x}" y="10" text-anchor="middle" dominant-baseline="hanging">{t}</text>']
            for x, t in values
        ]
        self.assertListEqual(expect, [x.get_element_list() for x in x_axis.tick_texts])
        expect = [t for t in ticks]
        self.assertListEqual(expect, x_axis.get_ticks_with_positions())

    def test_two_dates_about_a_month(self):
        """
        between 1 day and 1 month
        """
        # given
        x_axis = self.x_axis(
            [
                date(2000, 1, 1),
                date(2000, 1, 4),
            ],
        )
        values = (
            (0.0, "2000-01-01"),
            (33.33333333333333, "2000-01-02"),
            (66.66666666666666, "2000-01-03"),
            (100.0, "2000-01-04"),
        )
        ticks = (
            (date(2000, 1, 1), 0.0),
            (date(2000, 1, 2), 33.33333333333333),
            (date(2000, 1, 3), 66.66666666666666),
            (date(2000, 1, 4), 100.0),
        )
        # when
        # then
        self.check_axis(x_axis, values, ticks)

    def test_two_datetimes_about_a_month(self):
        """
        between 1 day and 1 month
        """
        # given
        x_axis = self.x_axis(
            [
                datetime(2000, 1, 1, 11, 11, 11),
                datetime(2000, 1, 4, 14, 14, 14),
            ],
        )
        values = (
            (0.0, "2000-01-01 11:11:00"),
            (25.0, "2000-01-02 11:11:00"),
            (50.0, "2000-01-03 11:11:00"),
            (75.0, "2000-01-04 11:11:00"),
            (100.0, "2000-01-05 11:11:00"),
        )
        ticks = (
            (datetime(2000, 1, 1, 11, 11, 0), 0.0),
            (datetime(2000, 1, 2, 11, 11, 0), 25.0),
            (datetime(2000, 1, 3, 11, 11, 0), 50.0),
            (datetime(2000, 1, 4, 11, 11, 0), 75.0),
            (datetime(2000, 1, 5, 11, 11, 0), 100.0),
        )
        # when
        # then
        self.check_axis(x_axis, values, ticks)

    def test_two_dates_decades_apart(self):
        """
        > 10 years -> years increment, day on 1
        """
        # given
        x_axis = self.x_axis(
            [
                date(2000, 8, 3),
                date(2011, 4, 24),
            ]
        )
        values = (
            (0.0, "2000-08-01"),
            (9.08638287279064, "2001-08-01"),
            (18.17276574558128, "2002-08-01"),
            (27.25914861837192, "2003-08-01"),
            (36.37042569081404, "2004-08-01"),
            (45.45680856360468, "2005-08-01"),
            (54.54319143639532, "2006-08-01"),
            (63.629574309185955, "2007-08-01"),
            (72.74085138162808, "2008-08-01"),
            (81.82723425441873, "2009-08-01"),
            (90.91361712720936, "2010-08-01"),
            (100.0, "2011-08-01"),
        )
        ticks = (
            (date(2000, 8, 1), 0.0),
            (date(2001, 8, 1), 9.08638287279064),
            (date(2002, 8, 1), 18.17276574558128),
            (date(2003, 8, 1), 27.25914861837192),
            (date(2004, 8, 1), 36.37042569081404),
            (date(2005, 8, 1), 45.45680856360468),
            (date(2006, 8, 1), 54.54319143639532),
            (date(2007, 8, 1), 63.629574309185955),
            (date(2008, 8, 1), 72.74085138162808),
            (date(2009, 8, 1), 81.82723425441873),
            (date(2010, 8, 1), 90.91361712720936),
            (date(2011, 8, 1), 100.0),
        )
        # when
        # then
        self.check_axis(x_axis, values, ticks)

    def test_two_datetimes_decades_apart(self):
        """
        > 10 years -> years increment, day on 1, time on 00:00:00
        """
        # given
        x_axis = self.x_axis(
            [
                datetime(2000, 8, 3, 11, 11, 11),
                datetime(2011, 4, 24, 14, 14, 14),
            ]
        )
        values = (
            (0.0, "2000-08-01 00:00:00"),
            (9.08638287279064, "2001-08-01 00:00:00"),
            (18.17276574558128, "2002-08-01 00:00:00"),
            (27.25914861837192, "2003-08-01 00:00:00"),
            (36.37042569081404, "2004-08-01 00:00:00"),
            (45.45680856360468, "2005-08-01 00:00:00"),
            (54.54319143639532, "2006-08-01 00:00:00"),
            (63.629574309185955, "2007-08-01 00:00:00"),
            (72.74085138162808, "2008-08-01 00:00:00"),
            (81.82723425441873, "2009-08-01 00:00:00"),
            (90.91361712720936, "2010-08-01 00:00:00"),
            (100.0, "2011-08-01 00:00:00"),
        )
        ticks = (
            (datetime(2000, 8, 1, 0, 0, 0), 0.0),
            (datetime(2001, 8, 1, 0, 0, 0), 9.08638287279064),
            (datetime(2002, 8, 1, 0, 0, 0), 18.17276574558128),
            (datetime(2003, 8, 1, 0, 0, 0), 27.25914861837192),
            (datetime(2004, 8, 1, 0, 0, 0), 36.37042569081404),
            (datetime(2005, 8, 1, 0, 0, 0), 45.45680856360468),
            (datetime(2006, 8, 1, 0, 0, 0), 54.54319143639532),
            (datetime(2007, 8, 1, 0, 0, 0), 63.629574309185955),
            (datetime(2008, 8, 1, 0, 0, 0), 72.74085138162808),
            (datetime(2009, 8, 1, 0, 0, 0), 81.82723425441873),
            (datetime(2010, 8, 1, 0, 0, 0), 90.91361712720936),
            (datetime(2011, 8, 1, 0, 0, 0), 100.0),
        )
        # when
        # then
        self.check_axis(x_axis, values, ticks)

    def test_two_close_ints_few_ticks(self):
        # given
        x_axis = self.x_axis(
            [
                42,
                48,
            ],
            max_ticks=3,
        )
        values = (
            (0.0, "42"),
            (33.33333333333333, "44"),
            (66.66666666666666, "46"),
            (100.0, "48"),
        )
        ticks = (
            (42, 0.0),
            (44, 33.33333333333333),
            (46, 66.66666666666666),
            (48, 100.0),
        )
        # when
        # then
        self.check_axis(x_axis, values, ticks)

    def test_two_close_ints_more_ticks(self):
        # given
        x_axis = self.x_axis(
            [
                42,
                48,
            ],
            max_ticks=10,
        )
        values = (
            (0.0, "42"),
            (16.666666666666664, "43"),
            (33.33333333333333, "44"),
            (50.0, "45"),
            (66.66666666666666, "46"),
            (83.33333333333334, "47"),
            (100.0, "48"),
        )
        ticks = (
            (42, 0.0),
            (43, 16.666666666666664),
            (44, 33.33333333333333),
            (45, 50.0),
            (46, 66.66666666666666),
            (47, 83.33333333333334),
            (48, 100.0),
        )
        # when
        # then
        self.check_axis(x_axis, values, ticks)

    def test_two_close_floats_few_ticks(self):
        # given
        x_axis = self.x_axis(
            [
                2.71828182845904523536,
                3.14159265358979323846,
            ],
            max_ticks=3,
        )
        values = (
            (0.0, "2.6"),
            (33.33333333333328, "2.8"),
            (66.66666666666664, "3.0"),
            (100.0, "3.2"),
        )
        ticks = (
            (2.6, 0.0),
            (2.8, 33.33333333333328),
            (3.0, 66.66666666666664),
            (3.2, 100.0),
        )
        # when
        # then
        self.check_axis(x_axis, values, ticks)

    def test_two_close_floats_more_ticks(self):
        # given
        x_axis = self.x_axis(
            [
                2.71828182845904523536,
                3.14159265358979323846,
            ],
            max_ticks=10,
        )
        values = (
            (0.0, "2.7"),
            (11.111111111111079, "2.75"),
            (22.222222222222157, "2.8"),
            (33.33333333333333, "2.85"),
            (44.444444444444414, "2.9"),
            (55.55555555555559, "2.95"),
            (66.66666666666666, "3.0"),
            (77.77777777777774, "3.05"),
            (88.88888888888891, "3.1"),
            (100.0, "3.15"),
        )
        ticks = (
            (2.7, 0.0),
            (2.75, 11.111111111111079),
            (2.8, 22.222222222222157),
            (2.85, 33.33333333333333),
            (2.9, 44.444444444444414),
            (2.95, 55.55555555555559),
            (3.0, 66.66666666666666),
            (3.05, 77.77777777777774),
            (3.1, 88.88888888888891),
            (3.15, 100.0),
        )
        # when
        # then
        self.check_axis(x_axis, values, ticks)

    def test_two_far_ints_few_ticks(self):
        # given
        x_axis = self.x_axis(
            [
                42,
                666,
            ],
            max_ticks=3,
        )
        values = (
            (0.0, "0"),
            (50.0, "500"),
            (100.0, "1000"),
        )
        ticks = (
            (0, 0.0),
            (500, 50.0),
            (1000, 100.0),
        )
        # when
        # then
        self.check_axis(x_axis, values, ticks)

    def test_two_far_ints_more_ticks(self):
        # given
        x_axis = self.x_axis(
            [
                42,
                666,
            ],
            max_ticks=10,
        )
        values = (
            (0.0, "0"),
            (14.285714285714285, "100"),
            (28.57142857142857, "200"),
            (42.857142857142854, "300"),
            (57.14285714285714, "400"),
            (71.42857142857143, "500"),
            (85.71428571428571, "600"),
            (100.0, "700"),
        )
        ticks = (
            (0, 0.0),
            (100, 14.285714285714285),
            (200, 28.57142857142857),
            (300, 42.857142857142854),
            (400, 57.14285714285714),
            (500, 71.42857142857143),
            (600, 85.71428571428571),
            (700, 100.0),
        )
        # when
        # then
        self.check_axis(x_axis, values, ticks)

    def test_two_far_floats_few_ticks(self):
        # given
        x_axis = self.x_axis(
            [
                0.4,
                6553.6,
            ],
            max_ticks=3,
        )
        values = (
            (0.0, "0"),
            (50.0, "5000"),
            (100.0, "10000"),
        )
        ticks = (
            (0, 0.0),
            (5000, 50.0),
            (10000, 100.0),
        )
        # when
        # then
        self.check_axis(x_axis, values, ticks)

    def test_two_far_floats_more_ticks(self):
        # given
        x_axis = self.x_axis(
            [
                0.4,
                6553.6,
            ],
            max_ticks=10,
        )
        values = (
            (0.0, "0"),
            (14.285714285714285, "1000"),
            (28.57142857142857, "2000"),
            (42.857142857142854, "3000"),
            (57.14285714285714, "4000"),
            (71.42857142857143, "5000"),
            (85.71428571428571, "6000"),
            (100.0, "7000"),
        )
        ticks = (
            (0, 0.0),
            (1000, 14.285714285714285),
            (2000, 28.57142857142857),
            (3000, 42.857142857142854),
            (4000, 57.14285714285714),
            (5000, 71.42857142857143),
            (6000, 85.71428571428571),
            (7000, 100.0),
        )
        # when
        # then
        self.check_axis(x_axis, values, ticks)


if __name__ == '__main__':
    unittest.main()
