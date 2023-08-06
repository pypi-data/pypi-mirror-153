"""Provides an API for date and time related functions."""
import datetime
import time


def now():
    """Return the current date and time, represented as milliseconds since the
    UNIX epoch.
    """
    return int(datetime.datetime.utcnow().timestamp() * 1000)
