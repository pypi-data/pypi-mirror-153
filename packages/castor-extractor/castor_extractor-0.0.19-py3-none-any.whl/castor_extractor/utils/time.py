from datetime import date, datetime


def current_datetime() -> datetime:
    """Returns the current datetime"""
    return datetime.utcnow()


def current_date() -> date:
    """Returns the current datetime"""
    return current_datetime().date()


def current_timestamp() -> int:
    """
    Returns the current timestamp from epoch (rounded to the nearest second)
    """
    return int(datetime.timestamp(current_datetime()))
