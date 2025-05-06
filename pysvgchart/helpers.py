import math
import datetime as dt
import collections.abc


def noop(*args, **kwargs):
    pass


def default_format(value):
    """
    format a number
    """
    return '{0:,}'.format(value) if not isinstance(value, str) else value


def safe_get_element_list(built_in):
    """
    always return a list
    """
    return built_in.get_element_list() if built_in is not None else []


def collapse_element_list(*args):
    """
    flatten any number of lists of elements to a list of elements
    """
    return [e for built_ins in args for built_in in built_ins for e in safe_get_element_list(built_in) if built_ins is not None and built_in is not None]


def get_numeric_limits(
        values,
        max_ticks,
        min_value=None,
        max_value=None,
        include_zero=False,
):
    """
    compute numeric limits for a series of numbers
    :param values: actual values
    :param max_ticks: maximum number of ticks
    :param min_value: optional minimum value to include in limits
    :param max_value: optional maximum value to include in limits
    :param include_zero: whether to include zero in limits
    """
    value_min, value_max = min(values), max(values)
    if min_value is not None:
        value_min = min(value_min, min_value)
    if max_value is not None:
        value_max = max(value_max, max_value)
    if include_zero:
        if value_min > 0:
            value_min = 0
        if value_max < 0:
            value_max = 0

    if value_max == value_min:
        raise ValueError("All values are the same — cannot compute numeric limits.")

    raw_pad = (value_max - value_min) / max_ticks
    magnitude = 10 ** math.floor(math.log10(raw_pad))
    residual = raw_pad / magnitude
    if residual <= 1:
        nice = 1
    elif residual <= 2:
        nice = 2
    elif residual <= 5:
        nice = 5
    else:
        nice = 10

    pad = nice * magnitude
    start = math.floor(value_min / pad)
    end = math.ceil(value_max / pad)
    return [round(y * pad, 10) for y in range(int(start), int(end + 1))]


def get_date_or_time_limits(
        dates,
        max_ticks=10,
        min_value=None,
        max_value=None,
):
    """
    compute date limits for a series of dates/datetimes
    :param dates: actual dates/datetimes
    :param max_ticks: maximum number of ticks
    :param min_value: optional minimum value to include in limits
    :param max_value: optional maximum value to include in limits
    """
    date_min, date_max = min(dates), max(dates)
    if date_min >= date_max:
        raise ValueError("Dates must have a positive range.")

    if min_value and min_value < date_min:
        date_min = min_value

    if max_value and max_value > date_max:
        date_max = max_value

    total_seconds = (date_max - date_min).total_seconds()

    if total_seconds <= 3600:
        interval = dt.timedelta(minutes=max(1, int(total_seconds // max_ticks)))
    elif total_seconds <= 86400:
        interval = dt.timedelta(hours=max(1, int(total_seconds // (max_ticks * 3600))))
    elif total_seconds <= 30 * 86400:
        interval = dt.timedelta(days=max(1, int(total_seconds // (max_ticks * 86400))))
    else:
        total_days = total_seconds / 86400
        approx_months = total_days / 30.0
        raw_interval = approx_months / max_ticks

        if raw_interval <= 1:
            interval_months = 1
        elif raw_interval <= 2:
            interval_months = 2
        elif raw_interval <= 3:
            interval_months = 3
        elif raw_interval <= 6:
            interval_months = 6
        else:
            interval_months = 12

        start = date_min.replace(day=1)
        end = (date_max.replace(day=1) + dt.timedelta(days=32)).replace(day=1)  # first day of next month

        ticks = []
        current_tick = start
        while current_tick <= end:
            ticks.append(current_tick if current_tick >= min(dates) else min(dates))
            month = current_tick.month + interval_months
            year = current_tick.year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            current_tick = current_tick.replace(year=year, month=month)
        return ticks

    ticks = []
    current_tick = date_min.replace(second=0, microsecond=0)
    while True:
        ticks.append(current_tick if current_tick >= min(dates) else min(dates))
        if current_tick > date_max:
            break
        current_tick += interval

    return ticks


def get_limits(
        values,
        max_ticks,
        min_value=None,
        max_value=None,
        include_zero=False,
        min_unique_values=2
):
    """
    compute numeric limits for a series of numbers

    :param values: actual values
    :param max_ticks: maximum number of ticks
    :param min_value: optional minimum value to include in limits
    :param max_value: optional maximum value to include in limits
    :param include_zero: whether to include zero in limits
    :param min_unique_values: minimum number of unique values required
    """
    if values is None or not isinstance(values, collections.abc.Iterable) or len(set(values)) < min_unique_values:
        raise ValueError("Values must be a non-empty iterable with at least %d unique elements.", min_unique_values)
    if all(isinstance(v, (dt.datetime, dt.date)) for v in values):
        return get_date_or_time_limits(
            values,
            max_ticks,
            min_value=min_value,
            max_value=max_value,
        )
    elif all(isinstance(v, (int, float)) for v in values):
        return get_numeric_limits(
            values,
            max_ticks,
            min_value=min_value,
            max_value=max_value,
            include_zero=include_zero,
        )
    else:
        raise TypeError("Invalid data types in values")


def simple_limits(
        values,
        max_ticks,
        min_value=None,
        max_value=None,
        include_zero=False,
        min_unique_values=2,
):
    return values
