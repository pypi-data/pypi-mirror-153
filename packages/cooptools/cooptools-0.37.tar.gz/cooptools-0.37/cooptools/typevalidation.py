import dateutil
from datetime import date, datetime, timezone as tz
import pandas as pd
import uuid
import math

def float_as_currency(val: float) -> str:
    return "${:,.2f}".format(round(val, 2))


def int_tryParse(value) -> int:
    try:
        return int(value)
    except:
        return None


def date_tryParse(value) -> date:
    return force_to_date_or_None(value)

def datestamp_tryParse(value, include_time: bool = True, include_ms: bool = True) -> datetime:
    try:
        val = force_to_datetime_or_None(value)

        if not include_time:
            val = datetime.combine(val, datetime.min.time())

        if not include_ms:
            val = val.replace(microsecond=0)

        return val
    except:
        return None

def uuid_tryparse(val) -> uuid.UUID:
    if isinstance(val, uuid.UUID):
        return val
    elif isinstance(val, str) and val != '':
        return uuid.UUID(val)
    elif isinstance(val, float) and math.isnan(val):
        return None
    else:
        raise TypeError(f"Unhandled UUID value: {val}")

def force_to_date_or_None(val):
    my_datetime = force_to_datetime_or_None(val)
    if my_datetime is None:
        return None
    else:
        return my_datetime.date()

def force_to_datetime_or_None(val, force_to_midnight: bool = False):
    try:
        # parse supported inputs to a datetime
        if isinstance(val, datetime):
            ret = val
        elif isinstance(val, date):
            ret = datetime.combine(val, datetime.min.time())
        elif isinstance(val, pd.Timestamp):
            the_date = val.to_pydatetime().date()
            ret = datetime.combine(the_date, datetime.min.time())
        else:
            val = dateutil.parser.parse(val)
            ret = force_to_datetime_or_None(val)

        # force to midnight if requested
        if force_to_midnight:
            ret = datetime.combine(ret.date(), datetime.min.time())

        # return value that was parsed
        return ret
    except:
        return None


if __name__ == "__main__":
    try_vals = [
        date.today(),
        '10.21.21',
        '10/21/21',
        None,
        datetime.today(),
        '2014-08-01 11:00:00+02:00'
    ]

    results = map(force_to_datetime_or_None, try_vals)

    print(list(results))

    results = map(lambda x: datestamp_tryParse(x, include_ms=False), try_vals)
    print(list(results))