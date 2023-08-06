import datetime
import os
from decimal import Decimal

import pytz
from aws_lambda_powertools import Logger

__all__ = [
    "get_logger",
    "get_mty_datetime",
    "cast_default",
    "cast_date",
    "cast_number"
]

LOG_LEVELS = {
    "1": "DEBUG",
    "2": "INFO",
    "3": "WARNING",
    "4": "ERROR",
    "5": "CRITICAL"
}


def get_logger(name=None):
    """
    Create a logger for code
    Args:
        name:

    Returns:

    """
    level_log = LOG_LEVELS.get(os.environ.get('LOG_LEVEL', '4'))
    logger = Logger(service=name, level=level_log, log_record_order=["level", "message"], location=None,
                    sampling_rate=None)
    return logger


def get_mty_datetime():
    """
    Returns datetime with the timezone America/Monterrey

    Returns: datetime object

    """
    mty = pytz.timezone('America/Monterrey')
    return datetime.datetime.now(tz=mty)


def cast_default(o):
    """
    Cast all date time and Decimals objects in a dict
    Args:
        o: Any element in dictionary

    Returns:
        element cast to correct type
    """
    o = cast_date(o)
    if isinstance(o, Decimal):
        o = cast_number(o)
    return o


def cast_date(element: datetime.date):
    """
    Gets a string in format iso from a datetime object
    Args:
        element: datetime object

    Returns: String like 'YYYY-mm-ddTHH:MM:SS.MILLIS'
    """
    if isinstance(element, (datetime.date, datetime.time)):
        element = element.isoformat()
    return element


def cast_number(number: (str, Decimal)) -> (int, float):
    """
    Cast any string or Decimal object to float or int
    Args:
        number: Any number with data type Decimal or int

    Returns:
        An int or float object
    """
    if isinstance(number, str):
        if number.isnumeric():
            return int(number)
        else:
            try:
                return float(number)
            except ValueError:
                try:
                    return float(number.replace(',', ''))
                except ValueError:
                    raise ValueError("The value not is int o float")
    elif isinstance(number, Decimal):
        return cast_number(str(number))
    elif isinstance(number, (float, int)):
        return number
