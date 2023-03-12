from datetime import datetime, timezone

import pandas as pd
from dateutil.relativedelta import relativedelta


def current_time_utc() -> datetime:
    """Get current time in iso format

    Returns:
        str: current time in iso format
    """
    return datetime.utcnow().replace(tzinfo=timezone.utc, microsecond=0)  # .isoformat()


def to_isoformat(dt: datetime):
    """Convert datetime object to iso format

    Args:
        dt (datetime): datetime object

    Returns:
        str: datetime object in iso format
    """
    return dt.isoformat()


def to_epoch_time(dt: datetime) -> float:
    """Convert datetime object to epoch time

    Args:
        dt (datetime): datetime object

    Returns:
        float: datetime object in epoch time
    """
    return dt.replace(tzinfo=timezone.utc).timestamp()


def from_epoch_time(value: float) -> datetime:
    """Get datetime object from epoch time

    Generates a datetime object from epoch time

    Args:
        value: epoch time

    Returns:
        datetime: datetime object
    """

    return datetime.fromtimestamp(value, tz=timezone.utc)


def from_isoformat(iso_time: str) -> datetime:
    """Get datetime object from iso time string

    Args:
        iso_time (str): ISO time string

    Returns:
            datetime: datetime object
    """
    if str is None:
        return datetime.min.replace(
            tzinfo=timezone.utc
        )  # https://bugs.python.org/issue31212

    return datetime.fromisoformat(iso_time)


def days_diff(start_time: datetime, end_time: datetime) -> int:
    """Difference in days between two datetime objects

    Args:
        start_time (datetime): start time
        end_time (datetime): end time

    Returns:
        int: difference in days
    """
    if start_time is None or end_time is None:
        return 999
    diff = end_time.replace(tzinfo=timezone.utc) - start_time.replace(
        tzinfo=timezone.utc
    )
    return round(diff.total_seconds() / 60 / 24)


def from_epoch_time(value) -> datetime:
    return pd.to_datetime(value, unit="s")


def month_from(mths_ago=-2, first_day=True) -> datetime:
    now = datetime.now()
    if first_day:
        current_month = datetime(now.year, now.month, 1)
    else:
        current_month = now
    return current_month + relativedelta(months=mths_ago)


def trunc_datetime(dt: datetime):
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def years_from_now(years: int) -> datetime:
    return datetime.now() - relativedelta(years=years)
