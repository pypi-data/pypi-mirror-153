from datetime import datetime, timezone
from dateutil.parser import parse as parse_time

def convert_from_utc_epoch(time, tz_aware=True):
    if tz_aware:
        return datetime.utcfromtimestamp(time).replace(tzinfo=timezone.utc)
    else:
        return datetime.utcfromtimestamp(time)

def convert_to_utc_datetime(time):
    d = time
    if type(time) == str:
        d = parse_time(time)
    if not d.tzinfo:
        return d.replace(tzinfo=timezone.utc)
    elif d.tzinfo == timezone.utc:
        return d
    else:
        return convert_from_utc_epoch(d.timestamp())

def convert_to_utc_epoch(time):
    return convert_to_utc_datetime(time).timestamp()

def current_utc_epoch():
    return datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()

