from datetime import datetime, date
import unittest


from pysvgchart.helpers import get_date_or_time_limits


class TestGetDateOrTimeLimits(unittest.TestCase):
    """
    test the get_date_or_time_limits() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_no_data(self):
        """
        fails on min/max
        """
        # given
        dates = []
        # when
        # then
        with self.assertRaises(ValueError):
            get_date_or_time_limits(dates)

    def test_one_date(self):
        """
        fails on range
        """
        # given
        dates = [
            date(2000, 1, 1),
        ]
        # when
        # then
        with self.assertRaises(ValueError):
            get_date_or_time_limits(dates)

    def test_two_same_dates(self):
        """
        fails on range
        """
        # given
        dates = [
            date(2000, 1, 1),
            date(2000, 1, 1),
        ]
        # when
        # then
        with self.assertRaises(ValueError):
            get_date_or_time_limits(dates)

    def test_two_datetimes_less_than_5_minutes(self):
        """
        less than 5 minutes -> seconds increment
        """
        # given
        dates = [
            datetime(2000, 1, 1, 11, 11, 11),
            datetime(2000, 1, 1, 11, 14, 14),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            datetime(2000, 1, 1, 11, 11, 0),
            datetime(2000, 1, 1, 11, 11, 18),
            datetime(2000, 1, 1, 11, 11, 36),
            datetime(2000, 1, 1, 11, 11, 54),
            datetime(2000, 1, 1, 11, 12, 12),
            datetime(2000, 1, 1, 11, 12, 30),
            datetime(2000, 1, 1, 11, 12, 48),
            datetime(2000, 1, 1, 11, 13, 6),
            datetime(2000, 1, 1, 11, 13, 24),
            datetime(2000, 1, 1, 11, 13, 42),
            datetime(2000, 1, 1, 11, 14, 0),
            datetime(2000, 1, 1, 11, 14, 18),
        ]
        self.assertListEqual(expect, actual)

    def test_two_datetimes_less_than_an_hour(self):
        """
        between 5 minutes and 1 hour -> minutes increment, seconds on 0
        """
        # given
        dates = [
            datetime(2000, 1, 1, 11, 11, 11),
            datetime(2000, 1, 1, 11, 42, 14),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            datetime(2000, 1, 1, 11, 11, 0),
            datetime(2000, 1, 1, 11, 14, 0),
            datetime(2000, 1, 1, 11, 17, 0),
            datetime(2000, 1, 1, 11, 20, 0),
            datetime(2000, 1, 1, 11, 23, 0),
            datetime(2000, 1, 1, 11, 26, 0),
            datetime(2000, 1, 1, 11, 29, 0),
            datetime(2000, 1, 1, 11, 32, 0),
            datetime(2000, 1, 1, 11, 35, 0),
            datetime(2000, 1, 1, 11, 38, 0),
            datetime(2000, 1, 1, 11, 41, 0),
            datetime(2000, 1, 1, 11, 44, 0),
        ]
        self.assertListEqual(expect, actual)

    def test_two_datetimes_less_than_a_day(self):
        """
        between 1 hour and 1 day -> hours increment, seconds on 0
        """
        # given
        dates = [
            datetime(2000, 1, 1, 11, 11, 11),
            datetime(2000, 1, 1, 14, 14, 14),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            datetime(2000, 1, 1, 11, 11, 0),
            datetime(2000, 1, 1, 12, 11, 0),
            datetime(2000, 1, 1, 13, 11, 0),
            datetime(2000, 1, 1, 14, 11, 0),
            datetime(2000, 1, 1, 15, 11, 0),
        ]
        self.assertListEqual(expect, actual)

    def test_two_dates_less_than_30_days(self):
        """
        between 1 day and 1 month -> days increment
        """
        # given
        dates = [
            date(2000, 1, 1),
            date(2000, 1, 4),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            date(2000, 1, 1),
            date(2000, 1, 2),
            date(2000, 1, 3),
            date(2000, 1, 4),
        ]
        self.assertListEqual(expect, actual)

    def test_two_datetimes_less_than_30_days(self):
        """
        between 1 day and 1 month -> days increment, seconds on 0
        """
        # given
        dates = [
            datetime(2000, 1, 1, 11, 11, 11),
            datetime(2000, 1, 4, 14, 14, 14),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            datetime(2000, 1, 1, 11, 11, 0),
            datetime(2000, 1, 2, 11, 11, 0),
            datetime(2000, 1, 3, 11, 11, 0),
            datetime(2000, 1, 4, 11, 11, 0),
            datetime(2000, 1, 5, 11, 11, 0),
        ]
        self.assertListEqual(expect, actual)

    def test_two_dates_about_a_month(self):
        """
        about 1 month -> days increment
        """
        # given
        dates = [
            date(2000, 1, 1),
            date(2000, 1, 31),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            date(2000, 1, 1),
            date(2000, 1, 4),
            date(2000, 1, 7),
            date(2000, 1, 10),
            date(2000, 1, 13),
            date(2000, 1, 16),
            date(2000, 1, 19),
            date(2000, 1, 22),
            date(2000, 1, 25),
            date(2000, 1, 28),
            date(2000, 1, 31),
        ]
        self.assertListEqual(expect, actual)

    def test_two_datetimes_about_a_month(self):
        """
        about 1 month -> months increment, time on 00:00:00
        """
        # given
        dates = [
            datetime(2000, 1, 1, 11, 11, 11),
            datetime(2000, 1, 31, 14, 14, 14),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            datetime(2000, 1, 1, 0, 0, 0),
            datetime(2000, 2, 1, 0, 0, 0),
        ]
        self.assertListEqual(expect, actual)

    def test_two_dates_within_two_months(self):
        """
        between 1 and 2 months -> months increment, days on 1
        """
        # given
        dates = [
            date(2000, 12, 3),
            date(2001, 1, 24),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            date(2000, 12, 1),
            date(2001, 1, 1),
            date(2001, 2, 1),
        ]
        self.assertListEqual(expect, actual)

    def test_two_datetimes_within_two_months(self):
        """
        between 1 and 2 months -> months increment, day on 1, time on 00:00:00
        """
        # given
        dates = [
            datetime(2000, 12, 3, 11, 11, 11),
            datetime(2001, 1, 24, 14, 14, 14),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            datetime(2000, 12, 1, 0, 0, 0),
            datetime(2001, 1, 1, 0, 0, 0),
            datetime(2001, 2, 1, 0, 0, 0),
        ]
        self.assertListEqual(expect, actual)

    def test_two_dates_within_three_months(self):
        """
        between 2 and 3 months -> months increment, day on 1
        """
        # given
        dates = [
            date(2000, 11, 3),
            date(2001, 1, 24),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            date(2000, 11, 1),
            date(2000, 12, 1),
            date(2001, 1, 1),
            date(2001, 2, 1),
        ]
        self.assertListEqual(expect, actual)

    def test_two_datetimes_within_three_months(self):
        """
        between 2 and 3 months -> months increment, day on 1, time on 00:00:00
        """
        # given
        dates = [
            datetime(2000, 12, 3, 11, 11, 11),
            datetime(2001, 2, 24, 14, 14, 14),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            datetime(2000, 12, 1, 0, 0, 0),
            datetime(2001, 1, 1, 0, 0, 0),
            datetime(2001, 2, 1, 0, 0, 0),
            datetime(2001, 3, 1, 0, 0, 0),
        ]
        self.assertListEqual(expect, actual)

    def test_two_dates_within_six_months(self):
        """
        between 3 and 6 months -> months increment, day on 1
        """
        # given
        dates = [
            date(2000, 10, 3),
            date(2001, 2, 24),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            date(2000, 10, 1),
            date(2000, 11, 1),
            date(2000, 12, 1),
            date(2001, 1, 1),
            date(2001, 2, 1),
            date(2001, 3, 1),
        ]
        self.assertListEqual(expect, actual)

    def test_two_datetimes_within_six_months(self):
        """
        between 3 and 6 months -> months increment, day on 1, time on 00:00:00
        """
        # given
        dates = [
            datetime(2000, 10, 3, 11, 11, 11),
            datetime(2001, 2, 24, 14, 14, 14),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            datetime(2000, 10, 1, 0, 0, 0),
            datetime(2000, 11, 1, 0, 0, 0),
            datetime(2000, 12, 1, 0, 0, 0),
            datetime(2001, 1, 1, 0, 0, 0),
            datetime(2001, 2, 1, 0, 0, 0),
            datetime(2001, 3, 1, 0, 0, 0),
        ]
        self.assertListEqual(expect, actual)

    def test_two_dates_more_than_six_months(self):
        """
        between 6 and 12 months -> months increment, day on 1
        """
        # given
        dates = [
            date(2000, 8, 3),
            date(2001, 4, 24),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            date(2000, 8, 1),
            date(2000, 9, 1),
            date(2000, 10, 1),
            date(2000, 11, 1),
            date(2000, 12, 1),
            date(2001, 1, 1),
            date(2001, 2, 1),
            date(2001, 3, 1),
            date(2001, 4, 1),
            date(2001, 5, 1),
        ]
        self.assertListEqual(expect, actual)

    def test_two_datetimes_more_than_six_months(self):
        """
        between 6 and 12 months -> months increment, day on 1, time on 00:00:00
        """
        # given
        dates = [
            datetime(2000, 8, 3, 11, 11, 11),
            datetime(2001, 4, 24, 14, 14, 14),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            datetime(2000, 8, 1, 0, 0, 0),
            datetime(2000, 9, 1, 0, 0, 0),
            datetime(2000, 10, 1, 0, 0, 0),
            datetime(2000, 11, 1, 0, 0, 0),
            datetime(2000, 12, 1, 0, 0, 0),
            datetime(2001, 1, 1, 0, 0, 0),
            datetime(2001, 2, 1, 0, 0, 0),
            datetime(2001, 3, 1, 0, 0, 0),
            datetime(2001, 4, 1, 0, 0, 0),
            datetime(2001, 5, 1, 0, 0, 0),
        ]
        self.assertListEqual(expect, actual)

    def test_two_dates_decades_apart(self):
        """
        > 10 years -> years increment, day on 1
        """
        # given
        dates = [
            date(2000, 8, 3),
            date(2011, 4, 24),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            date(2000, 8, 1),
            date(2001, 8, 1),
            date(2002, 8, 1),
            date(2003, 8, 1),
            date(2004, 8, 1),
            date(2005, 8, 1),
            date(2006, 8, 1),
            date(2007, 8, 1),
            date(2008, 8, 1),
            date(2009, 8, 1),
            date(2010, 8, 1),
            date(2011, 8, 1),
        ]
        self.assertListEqual(expect, actual)

    def test_two_datetimes_decades_apart(self):
        """
        > 10 years -> years increment, day on 1, time on 00:00:00
        """
        # given
        dates = [
            datetime(2000, 8, 3, 11, 11, 11),
            datetime(2011, 4, 24, 14, 14, 14),
        ]
        # when
        actual = get_date_or_time_limits(dates)
        # then
        expect = [
            datetime(2000, 8, 1, 0, 0, 0),
            datetime(2001, 8, 1, 0, 0, 0),
            datetime(2002, 8, 1, 0, 0, 0),
            datetime(2003, 8, 1, 0, 0, 0),
            datetime(2004, 8, 1, 0, 0, 0),
            datetime(2005, 8, 1, 0, 0, 0),
            datetime(2006, 8, 1, 0, 0, 0),
            datetime(2007, 8, 1, 0, 0, 0),
            datetime(2008, 8, 1, 0, 0, 0),
            datetime(2009, 8, 1, 0, 0, 0),
            datetime(2010, 8, 1, 0, 0, 0),
            datetime(2011, 8, 1, 0, 0, 0),
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
