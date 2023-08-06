from datetime import datetime, timezone, time

from assembly_client.api.util.time import (
    TIME_FORMAT,
    TIME_FORMAT_WITHOUT_TZ,
    _check_int_field,
    _comparison_error,
)


class Time:
    """Time object structure
    It is tracking a time of the day up to the millisecond
    """

    def __init__(self, hour, minute, second, millisecond=0, timestamp=None):
        _check_time_fields(hour, minute, second, millisecond)

        self._hour = hour
        self._minute = minute
        self._second = second
        self._millisecond = millisecond

    @property
    def hour(self):
        """hour (0-23)"""
        return self._hour

    @property
    def minute(self):
        """minute (0-59)"""
        return self._minute

    @property
    def second(self):
        """second (0-59)"""
        return self._second

    @property
    def millisecond(self):
        """millisecond (0-999)"""
        return self._millisecond

    def set_hour(self, hour):
        return Time(hour, self.minute, self.second, self.millisecond)

    def set_minute(self, minute):
        return Time(self.hour, minute, self.second, self.millisecond)

    def set_second(self, second):
        return Time(self.hour, self.minute, second, self.millisecond)

    def set_millisecond(self, millisecond):
        return Time(self.hour, self.minute, self.second, millisecond)

    # convert the Date into an ISO8601 timestamp "00:00:00.000Z"
    def toisotimestamp(self):
        return (
            time(
                hour=self.hour,
                minute=self.minute,
                second=self.second,
                microsecond=self.millisecond * 1000,
            ).strftime(TIME_FORMAT_WITHOUT_TZ)[:-3]
            + "Z"
        )

    @classmethod
    def fromisotimestamp(cls, value):
        dt = datetime.strptime(value, TIME_FORMAT).astimezone(timezone.utc)
        hour = dt.hour
        minute = dt.minute
        second = dt.second
        millisecond = dt.microsecond // 1000

        return Time(hour, minute, second, millisecond)

    @classmethod
    def first_time_of_day(cls):
        return Time(0, 0, 0, 0)

    @classmethod
    def last_time_of_day(cls):
        return Time(23, 59, 59, 999)

    def __repr__(self):
        return "%s.%s(%d, %d, %d, %d)" % (
            self.__class__.__module__,
            self.__class__.__qualname__,
            self._hour,
            self._minute,
            self._second,
            self._millisecond,
        )

    def __str__(self):
        return self.toisotimestamp()

    def serialize(self):
        return {
            "hour": str(self._hour),
            "minute": str(self._minute),
            "second": str(self._second),
            "millisecond": str(self._millisecond),
            "timestamp": self.toisotimestamp(),
        }

    def __lt__(self, other):
        if not isinstance(other, Time):
            _comparison_error(self, other)

        return (self.hour, self.minute, self.second, self.millisecond) < (
            other.hour,
            other.minute,
            other.second,
            other.millisecond,
        )

    def __le__(self, other):
        if not isinstance(other, Time):
            _comparison_error(self, other)

        return (self.hour, self.minute, self.second, self.millisecond) <= (
            other.hour,
            other.minute,
            other.second,
            other.millisecond,
        )

    def __eq__(self, other):
        if not isinstance(other, Time):
            return False

        return (self.hour, self.minute, self.second, self.millisecond) == (
            other.hour,
            other.minute,
            other.second,
            other.millisecond,
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def to_milliseconds(self):
        return (
            self._hour * 60 * 60 * 1000
            + self._minute * 60 * 1000
            + self._second * 1000
            + self._millisecond
        )

    @classmethod
    def from_millisecond(cls, millis):
        if millis < 0:
            return Time.from_millisecond(
                24 * 60 * 60 * 1000 - (abs(millis) % (24 * 60 * 60 * 1000))
            )

        remaining_seconds, milliseconds = divmod(millis, 1000)
        remaining_minutes, seconds = divmod(remaining_seconds, 60)
        remaining_hours, minutes = divmod(remaining_minutes, 60)
        _, hours = divmod(remaining_hours, 24)
        return Time(hours, minutes, seconds, milliseconds)

    def add_milliseconds(self, m):
        return Time.from_millisecond(self.to_milliseconds() + m)

    def add_seconds(self, s):
        return Time.from_millisecond(self.to_milliseconds() + s * 1000)

    def add_minutes(self, m):
        return Time.from_millisecond(self.to_milliseconds() + m * 60 * 1000)

    def add_hours(self, h):
        return Time.from_millisecond(self.to_milliseconds() + h * 60 * 60 * 1000)

    def subtract_milliseconds(self, m):
        return Time.from_millisecond(self.to_milliseconds() - m)

    def subtract_seconds(self, s):
        return Time.from_millisecond(self.to_milliseconds() - s * 1000)

    def subtract_minutes(self, m):
        return Time.from_millisecond(self.to_milliseconds() - m * 60 * 1000)

    def subtract_hours(self, h):
        return Time.from_millisecond(self.to_milliseconds() - h * 60 * 60 * 1000)

    def subtract_delta(self, other):
        if isinstance(other, TimeDelta):
            return Time.from_millisecond(self.to_milliseconds() - other.milliseconds)
        else:
            raise ValueError("can only subtract a TimeDelta from a Time")

    # addition _only_ supports adding TimeDeltas to a Time
    def __add__(self, other):
        if not isinstance(other, TimeDelta):
            raise ValueError("can only add a TimeDelta to a Time")
        return self.add_milliseconds(other.milliseconds)

    # returns
    #   a TimeDelta computed from the difference in milliseconds between the 2 times if other is a Time
    #   a Time if other is a TimeDelta
    def __sub__(self, other):
        if isinstance(other, Time):
            return TimeDelta(
                milliseconds=self.to_milliseconds() - other.to_milliseconds()
            )

        if isinstance(other, TimeDelta):
            return self.subtract_milliseconds(other.milliseconds)

        raise ValueError("can only subtract a Time from a Time")


# The rounding of negative values is done such that, for 2 different times
#   t1 - t2 = -(t2 - t1)
class TimeDelta:
    def __init__(self, hours=0, minutes=0, seconds=0, milliseconds=0, str=None):
        milliseconds = hours * 3600000 + minutes * 60000 + seconds * 1000 + milliseconds

        if milliseconds > 86400000:
            raise ValueError(
                "a TimeDelta can only represent the difference of two Times of the day."
                + f" Got a total number of milliseconds > 86400000: {milliseconds}"
            )

        self._milliseconds = milliseconds

    @property
    def hours(self):
        """round the time delta to the nearest number of hours"""
        if self.minutes >= 0:
            return self.minutes // 60
        else:
            return -(-self.minutes // 60)

    @property
    def minutes(self):
        """round the time delta to the nearest number of minutes"""
        if self.seconds >= 0:
            return self.seconds // 60
        else:
            return -(-self.seconds // 60)

    # round the time delta to the nearest number of seconds
    @property
    def seconds(self):
        """round the time delta to the nearest number of seconds"""
        if self.milliseconds >= 0:
            return self.milliseconds // 1000
        else:
            return -(-self.milliseconds // 1000)

    @property
    def milliseconds(self):
        """return the time delta in milliseconds"""
        return self._milliseconds

    def __repr__(self):
        args = []
        if self._milliseconds < 0:
            total_milliseconds = -self._milliseconds
            sign = "-"
        else:
            total_milliseconds = self._milliseconds
            sign = ""

        hours, r1 = divmod(total_milliseconds, 3600000)
        minutes, r2 = divmod(r1, 60000)
        seconds, milliseconds = divmod(r2, 1000)

        if hours != 0:
            args.append("hours=%s%d" % (sign, hours))
        if minutes != 0:
            args.append("minutes=%s%d" % (sign, minutes))
        if self.seconds != 0:
            args.append("seconds=%s%d" % (sign, seconds))
        if self.milliseconds != 0:
            args.append("milliseconds=%s%d" % (sign, milliseconds))
        if not args:
            args.append("milliseconds=0")
        return "%s.%s(%s)" % (
            self.__class__.__module__,
            self.__class__.__qualname__,
            ", ".join(args),
        )

    def __str__(self):
        args = []
        if self._milliseconds < 0:
            total_milliseconds = -self._milliseconds
        else:
            total_milliseconds = self._milliseconds

        hours, r1 = divmod(total_milliseconds, 3600000)
        minutes, r2 = divmod(r1, 60000)
        seconds, milliseconds = divmod(r2, 1000)

        def plural(n):
            return "s" if n > 1 else ""

        if hours != 0:
            args.append("%d hour%s" % (hours, plural(hours)))
        if minutes != 0:
            args.append("%d minute%s" % (minutes, plural(minutes)))
        if seconds != 0:
            args.append("%d second%s" % (seconds, plural(seconds)))
        if milliseconds != 0:
            args.append("%d millisecond%s" % (milliseconds, plural(milliseconds)))
        if not args:
            args.append("0 milliseconds")

        if self._milliseconds < 0:
            sign = "-("
            end_sign = ")"
        else:
            sign = ""
            end_sign = ""

        return "%s%s%s" % (sign, ", ".join(args), end_sign)

    def as_str(self):
        """Return a string representing this delta
        the order on as_str(delta) should be compatible with the order on delta
        as_str(d1) <= as_str(d2) <=> d1 <= d2.

        For negative values we take the complement to 86400000 which is the maximum
        number of milliseconds in a day
        the number of days is < 1000000000 which means 2.7 million years
        """

        def if_neg(v):
            return -(86400000 + v) if v < 0 else v

        return "%09d" % if_neg(self.milliseconds)

    def serialize(self):
        return {"milliseconds": str(self.milliseconds), "as_str": self.as_str()}

    def __eq__(self, other):
        return self.milliseconds == other.milliseconds

    def __ne__(self, other):
        return not self.__eq__(other)

    def __neg__(self):
        return TimeDelta(milliseconds=-self._milliseconds)

    def __lt__(self, other):
        if not isinstance(other, TimeDelta):
            _comparison_error(self, other)

        return self.milliseconds < other.milliseconds

    def __le__(self, other):
        if not isinstance(other, TimeDelta):
            _comparison_error(self, other)

        return self.milliseconds <= other.milliseconds

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __add__(self, other):
        return TimeDelta(milliseconds=self._milliseconds + other._milliseconds)

    def __sub__(self, other):
        return self + (-other)


def _check_time_fields(hour, minute, second, millisecond):
    hour = _check_int_field(hour)
    minute = _check_int_field(minute)
    second = _check_int_field(second)
    millisecond = _check_int_field(millisecond)

    if not 0 <= hour <= 23:
        raise ValueError(
            "hour must be in %d..%d" % (0, 23),
            f"Time({hour}, {minute}, {second}, {millisecond})",
        )
    if not 0 <= minute <= 59:
        raise ValueError(
            "minute must be in %d..%d" % (0, 59),
            f"Time({hour}, {minute}, {second}, {millisecond})",
        )
    if not 0 <= second <= 59:
        raise ValueError(
            "second must be in %d..%d" % (0, 59),
            f"Time({hour}, {minute}, {second}, {millisecond})",
        )
    if not 0 <= millisecond <= 999:
        raise ValueError(
            "millisecond must be in %d..%d" % (0, 999),
            f"Time({hour}, {minute}, {second}, {millisecond})",
        )
    return hour, minute, second, millisecond
