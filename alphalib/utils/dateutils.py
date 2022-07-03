from datetime import datetime, timezone


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
