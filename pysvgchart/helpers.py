import math
import datetime as dt


def noop(*args, **kwargs):
    pass


def default_format(value):
    """
    format a number
    """
    return "{0:,}".format(value) if not isinstance(value, str) else value


def safe_get_element_list(elements):
    """
    elements may not exist and may lack the get_element_list() function
    """
    if elements is not None and hasattr(elements, "get_element_list"):
        yield from elements.get_element_list()


def collapse_element_list(*list_of_list_of_elements) -> list:
    """
    flatten any number of lists of elements to a list of elements
    """
    return [
        element
        for list_of_elements in list_of_list_of_elements
        for elements in (
            list_of_elements if isinstance(list_of_elements, (list, tuple, set)) else []
        )
        for element in safe_get_element_list(elements)
    ]


def get_numeric_ticks(
    values,
    max_ticks,
    min_value=None,
    max_value=None,
    include_zero=False,
):
    """
    compute ticks for a series of numbers
    :param values: actual values
    :param max_ticks: maximum number of ticks
    :param min_value: optional minimum value to include in ticks
    :param max_value: optional maximum value to include in ticks
    :param include_zero: whether to include zero in ticks
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
        raise ValueError("All values are the same — cannot compute min/max.")

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


def get_date_or_time_ticks(
    dates,
    max_ticks=10,
    min_value=None,
    max_value=None,
):
    """
    compute ticks for a series of dates/datetimes
    :param dates: actual dates/datetimes
    :param max_ticks: maximum number of ticks
    :param min_value: optional minimum value to include in ticks
    :param max_value: optional maximum value to include in ticks
    """
    date_min, date_max = min(dates), max(dates)
    if date_min >= date_max:
        raise ValueError("Dates must have a positive range.")

    if min_value and min_value < date_min:
        date_min = min_value

    if max_value and max_value > date_max:
        date_max = max_value

    total_seconds = (date_max - date_min).total_seconds()

    if total_seconds <= 300:  # 5 minutes
        interval = dt.timedelta(seconds=max(1, int(total_seconds // max_ticks)))
    elif total_seconds <= 3600:  # an hour
        interval = dt.timedelta(minutes=max(1, int(total_seconds // (max_ticks * 60))))
    elif total_seconds <= 86400:  # a day
        interval = dt.timedelta(hours=max(1, int(total_seconds // (max_ticks * 3600))))
    elif total_seconds <= 30 * 86400:  # about a month
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

        # enclosing period of whole months
        start = date_min.replace(day=1)
        end = (date_max.replace(day=1) + dt.timedelta(days=32)).replace(day=1)
        # time to 00:00:00 for datetimes
        if isinstance(start, dt.datetime):
            start = dt.datetime.combine(start.date(), dt.time(0, 0, 0))
        if isinstance(end, dt.datetime):
            end = dt.datetime.combine(end.date(), dt.time(0, 0, 0))

        current_tick = start
        ticks = [current_tick]
        while ticks[-1] < end:
            month = current_tick.month + interval_months
            year = current_tick.year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            current_tick = current_tick.replace(year=year, month=month)
            ticks.append(current_tick)
        return ticks

    current_tick = (
        date_min.replace(second=0, microsecond=0) if isinstance(date_min, dt.datetime) else date_min
    )
    ticks = [current_tick]
    while ticks[-1] < date_max:
        current_tick += interval
        ticks.append(current_tick)

    return ticks
