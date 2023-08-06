from astropy.time import Time, TimezoneInfo
from datetime import datetime
from typing import Union


def resolve_date_iso(date: Union[Time, datetime, str]):
    """
    Helper function for resolving varied date input to an iso string.
    Args:
        date: Union[Time, datetime, str] date provided as string, datetime.datetime,
         or astropy.time.Time object
         if string, must be given as UTC!

    Returns: str = iso formatted string representation of the input time
    """
    if isinstance(date, Time):
        return date.utc.iso
    elif isinstance(date, datetime):
        return Time(date.astimezone(TimezoneInfo())).iso  # Defaults to UTC so we don't need pytz.
    elif isinstance(date, str):
        return Time(date).iso  # string assumed to be UTC as per docstring.
    else:
        raise ValueError(f'given date {date} was not a proper astropy.time.Time, datetime.datetime, or UTC string')
