import pytz
import datetime
from lantern_sl.utils.logger import logger

def current_ts(tz=pytz.utc):
    """ returns the current timestamp for the specified timezone """
    return int(datetime.datetime.now(tz).timestamp()*1000)

def get_ttl(ts=current_ts(), year=0, month=0, day=0, hour=0, minute=0, return_mode='s'):
    delta_time_minutes = (year * 525600) + (month * 43800) + (day * 1440) + (hour * 60) + minute
    if delta_time_minutes <= 0:
        raise Exception('At least 1 parameter is required (year, month, day, hour, minute')
    if return_mode == 's':
        return int(ts/1000 + delta_time_minutes*60)
    elif return_mode == 'ms':
        return int(ts/1000 + delta_time_minutes*60) * 1000
    else:
        raise Exception('return_mode param has to be s: second or ms: millisecond')

def ts_to_datetime(ts, timezone):
    """ Convert timestamp (UTC) to datetime in timezone in parameters
    Returns
        datetime localized to tiemzone
    """
    ts = int(int(ts)/1000) if len(str(ts)) >= 13 else int(ts) # to seconds and to int
    py_zone = pytz.timezone(timezone)
    dt = datetime.datetime.utcfromtimestamp(ts)
    dt = pytz.utc.localize(dt, is_dst=None).astimezone(py_zone)
    return dt

def datetime_to_ts(dt):
    """ convert any datetime to timestamp """
    return int(dt.timestamp())

def ts_to_str(ts, timezone, strftime="%b %d %Y %H:%M:%S"):
    """ from ts (UTC), it converts date to timezone and return string using strftime
    """
    dt_local = ts_to_datetime(ts, timezone)
    return dt_local.strftime(strftime)

def datetime_to_str(dt, timezone, strftime="%b %d %Y %H:%M:%S"):
    """ convert from datetime to string using defined format """
    ts = datetime_to_ts(dt)
    return ts_to_str(ts, timezone, strftime)

class TimeMeter:
    """Helpus to measure time takes for each function."""
    __counter = 0

    def __init__(self, prefix="TIME MEASURE: ", tz="America/Costa_Rica") -> None:
        self.prefix = prefix
        self.tz = tz
        self.start_at = current_ts()
        self.previous_at = current_ts()
        self.tick(desc="Starts")

    def tick(self, desc):
        self.__counter += 1
        _now = current_ts()
        diff_from_start = round((_now - self.start_at)/1000, 2)
        diff_from_prev = round((_now - self.previous_at)/1000, 2)
        logger.info(f" -- {self.__counter} -- {self.prefix}{desc}({diff_from_start} sec (diff: {diff_from_prev})) - {ts_to_str(ts=_now, timezone=self.tz)}")
        self.previous_at = _now
