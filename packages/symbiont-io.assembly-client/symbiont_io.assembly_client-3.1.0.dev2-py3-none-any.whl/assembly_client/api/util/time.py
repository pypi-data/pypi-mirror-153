from datetime import datetime, timezone

DENOM = int(1e6)
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
TIME_FORMAT = "%H:%M:%S.%f%z"
TIME_FORMAT_WITHOUT_TZ = "%H:%M:%S.%f"
DATE_FORMAT = "%Y-%m-%d"


def utc_time():
    return datetime.now(timezone.utc)


def utc_time_ns():
    return int(utc_time().timestamp() * 1e9)


def utc_time_iso():
    return utc_time().isoformat()


def _check_int_field(value):
    if isinstance(value, int):
        return value
    if not isinstance(value, float):
        try:
            value = value.__int__()
        except AttributeError:
            pass
        else:
            if isinstance(value, int):
                return value
            raise TypeError("__int__ returned non-int (type %s)" % type(value).__name__)
        raise TypeError("an integer is required (got type %s)" % type(value).__name__)
    raise TypeError("integer argument expected, got float")


def _comparison_error(x, y):
    raise TypeError("can't compare '%s' to '%s'" % (type(x).__name__, type(y).__name__))


def nanoseconds_to_isoformat(ns):
    micros = ns // 1000
    s = micros // DENOM
    num_micros = micros % DENOM
    ts = datetime.utcfromtimestamp(s).replace(microsecond=num_micros).isoformat()
    # make millisecond precision and add timezone
    if num_micros == 0:
        ts += ".000000"

    return ts[:-3] + "Z"


def isoformat_to_milliseconds(ts):
    dt = datetime.strptime(ts, DATETIME_FORMAT)
    return int(dt.timestamp()) * 1000 + dt.microsecond // 1000
