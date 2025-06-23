"""
shared - definitions shared throughout the code
"""

from datetime import date, datetime


dates_sequence = list[date] | tuple[date, ...]
datetimes_sequence = list[datetime] | tuple[datetime, ...]
number = float | int
numbers_sequence = list[number] | tuple[number, ...]

style_def = dict[str, str]
named_styles = dict[str, style_def]
