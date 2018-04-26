import datetime as dt

import pytimeparse
from flaskbb.utils.helpers import time_utcnow


def text_to_bool(text):
    text = text.lower()
    if text in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
        return True
    elif text in ('no', 'n', 'false', 'f', '0', 'disable', 'off'):
        return False
    else:
        raise ValueError


def text_to_datetime(text):
    return time_utcnow() + dt.timedelta(seconds=pytimeparse.parse(text))
