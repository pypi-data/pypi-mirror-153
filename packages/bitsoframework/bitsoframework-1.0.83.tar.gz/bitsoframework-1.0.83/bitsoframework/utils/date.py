from datetime import timedelta, datetime

from django.conf import settings
from django.utils.timezone import is_aware, make_aware, is_naive, make_naive


def fix_timezone(value, timezone=None, is_dst=None):
    if settings.USE_TZ:
        if not is_aware(value):
            return make_aware(value, timezone=timezone, is_dst=is_dst)
    elif not is_naive(value):
        return make_naive(value, timezone=timezone)
    return value


def as_date(value):
    if isinstance(value, datetime):
        return value.date()

    return value


def get_weekdays_between(start, end):
    if isinstance(start, datetime):
        start = start.date()

    if isinstance(end, datetime):
        end = end.date()

    dt = start

    dates = []

    while dt <= end:

        weekday = dt.isoweekday()
        if weekday > 5:
            dt += timedelta(days=8 - weekday)

        if dt <= end:
            dates.append(dt)
            dt += timedelta(days=1)

    return dates
