"""
The goal here is to provide a structure and methods to handle dates.

It works by distilling operations down to the lowest level, the millisecond.
"""
from datetime import date, timezone
from assembly_client.api.util.time import (
    isoformat_to_milliseconds,
    nanoseconds_to_isoformat,
    _comparison_error,
)
from dateutil.parser import isoparse
from assembly_client.api.types.date_types import Date, DateDelta
from assembly_client.api.types.time_types import Time, TimeDelta


class DateTime:
    """Datetime object structure
    It is composed of 2 components: a date and a time
    """

    def __init__(
        self,
        year,
        month,
        day,
        hour,
        minute,
        second,
        millisecond=0,
        timestamp=None,
        check_date_fields=True,
    ):
        self._date = Date(year, month, day, check_fields=check_date_fields)
        self._time = Time(hour, minute, second, millisecond)

    @property
    def date(self):
        return self._date

    @property
    def time(self):
        return self._time

    @property
    def year(self):
        """year (1-9999)"""
        return self._date.year

    @property
    def month(self):
        """month (1-12)"""
        return self._date.month

    @property
    def day(self):
        """day (1-31)"""
        return self._date.day

    @property
    def day_of_week(self):
        """day_of_week (1-7) - Monday to Sunday"""
        return self._date.day_of_week

    @property
    def is_last_day_of_month(self):
        return self._date.is_last_day_of_month

    @property
    def hour(self):
        """hour (0-23)"""
        return self._time.hour

    @property
    def minute(self):
        """minute (0-59)"""
        return self._time.minute

    @property
    def second(self):
        """second (0-59)"""
        return self._time.second

    @property
    def millisecond(self):
        """millisecond (0-999)"""
        return self._time.millisecond

    @property
    def microsecond(self):
        """microsecond (0-999000)"""
        return self._time.microsecond

    def set_year(self, year, check_date_fields=True):
        return DateTime.from_date_and_time(
            self.date.set_year(year, check_fields=check_date_fields),
            self.time,
            check_date_fields=check_date_fields,
        )

    def set_month(self, month, check_date_fields=True):
        return DateTime.from_date_and_time(
            self.date.set_month(month, check_fields=check_date_fields),
            self.time,
            check_date_fields=check_date_fields,
        )

    def set_day(self, day, check_date_fields=True):
        return DateTime.from_date_and_time(
            self.date.set_day(day, check_fields=check_date_fields),
            self.time,
            check_date_fields=check_date_fields,
        )

    def set_hour(self, hour):
        return DateTime.from_date_and_time(self.date, self.time.set_hour(hour))

    def set_minute(self, minute):
        return DateTime.from_date_and_time(self.date, self.time.set_minute(minute))

    def set_second(self, second):
        return DateTime.from_date_and_time(self.date, self.time.set_second(second))

    def set_millisecond(self, millisecond):
        return DateTime.from_date_and_time(
            self.date, self.time.set_millisecond(millisecond)
        )

    def toisotimestamp(self):
        return self._date.toiso() + "T" + self._time.toisotimestamp()

    @classmethod
    def from_datetime_dict(cls, dct):
        return DateTime(
            int(dct["year"]),
            int(dct["month"]),
            int(dct["day"]),
            int(dct["hour"]),
            int(dct["minute"]),
            int(dct["second"]),
            int(dct["millisecond"]),
        )

    @classmethod
    def from_date_and_time(cls, date, time, check_date_fields=False):
        return DateTime(
            date.year,
            date.month,
            date.day,
            time.hour,
            time.minute,
            time.second,
            time.millisecond,
            check_date_fields=check_date_fields,
        )

    @classmethod
    def fromisodate(cls, value):
        dt = date.fromisoformat(value)
        return DateTime(dt.year, dt.month, dt.day, 0, 0, 0)

    @classmethod
    def fromisotimestamp(cls, value):
        dt = isoparse(value).astimezone(timezone.utc)
        return DateTime(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond // 1000,
        )

    def __repr__(self):
        return "%s.%s(%d, %d, %d, %d, %d, %d, %d)" % (
            self.__class__.__module__,
            self.__class__.__qualname__,
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.millisecond,
        )

    def __str__(self):
        return DateTime.toisotimestamp(self)

    def serialize(self):
        return {
            "year": str(self.year),
            "month": str(self.month),
            "day": str(self.day),
            "hour": str(self.hour),
            "minute": str(self.minute),
            "second": str(self.second),
            "millisecond": str(self.millisecond),
            "timestamp": self.toisotimestamp(),
        }

    def __lt__(self, other):
        if not isinstance(other, DateTime):
            _comparison_error(self, other)

        return (self.date, self.time) < (other.date, other.time)

    def __le__(self, other):
        if not isinstance(other, DateTime):
            _comparison_error(self, other)

        return (self.date, self.time) <= (other.date, other.time)

    def __eq__(self, other):
        if not isinstance(other, DateTime):
            return False

        return (self.date, self.time) == (other.date, other.time)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    # addition _only_ supports adding DateTimeDeltas to a DateTime
    def __add__(self, other):
        if isinstance(other, DateTimeDelta):
            d = self.date + other.date_delta
            t = self.time + other.time_delta

            # if we add some time and end up with a time on the next
            # day we need to increment the date (same thing for removing some time)
            if other.time_delta > TimeDelta(0) and t < self.time:
                d = d.add_days(1)
            elif other.time_delta < TimeDelta(0) and t > self.time:
                d = d.subtract_days(1)

            return DateTime(
                d.year, d.month, d.day, t.hour, t.minute, t.second, t.millisecond
            )

        raise ValueError("can only add a DateTimeDelta to a DateTime")

    # returns
    #   a DateTimeDelta if other is a DateTime
    #   a DateTime if other is a DateTimeDelta
    def __sub__(self, other):
        if isinstance(other, DateTime):
            return DateTimeDelta(self.date - other.date, self.time - other.time)

        if isinstance(other, DateTimeDelta):
            return self + (-other)

        raise ValueError(
            "can only subtract a DateTime, a DateTimeDelta, a DateDelta, "
            + "or a TimeDelta from a DateTime"
        )

    def add_date_delta(self, other):
        if isinstance(other, DateDelta):
            return self + DateTimeDelta(other, TimeDelta())

        raise ValueError("can only add a DateDelta to a DateTime")

    def add_time_delta(self, other):
        if isinstance(other, TimeDelta):
            return self + DateTimeDelta(DateDelta(), other)

        raise ValueError("can only add a TimeDelta to a DateTime")

    def subtract_date_delta(self, other):
        if isinstance(other, DateDelta):
            return self + (-DateTimeDelta(other, TimeDelta()))

        raise ValueError("can only subtract a DateDelta from a DateTime")

    def subtract_time_delta(self, other):
        if isinstance(other, TimeDelta):
            return self + (-DateTimeDelta(DateDelta(), other))

        raise ValueError("can only subtract a TimeDelta from a DateTime")

    def subtract_delta(self, other):
        if isinstance(other, DateTimeDelta):
            return self + (-other)

        raise ValueError("can only subtract a DateTimeDelta from a DateTime")


class DateTimeDelta:
    def __init__(self, date_delta, time_delta, as_str=None):
        self._date_delta = date_delta
        self._time_delta = time_delta

    @property
    def date_delta(self):
        return self._date_delta

    @property
    def time_delta(self):
        return self._time_delta

    @classmethod
    def from_nanos(cls, nanos):
        return DateTime.fromisotimestamp(
            nanoseconds_to_isoformat(nanos)
        ) - DateTime.fromisotimestamp(nanoseconds_to_isoformat(0))

    def to_nanos(self):
        return 10**6 * isoformat_to_milliseconds(
            (
                DateTime.fromisotimestamp("1970-01-01T00:00:00.000Z") + self
            ).toisotimestamp()
        )

    def __repr__(self):
        return "%s.%s(%s, %s)" % (
            self.__class__.__module__,
            self.__class__.__qualname__,
            repr(self._date_delta),
            repr(self._time_delta),
        )

    def __str__(self):
        return "%s, %s" % (str(self._date_delta), str(self._time_delta))

    def as_str(self):
        """Return a string representing this delta
        the order on as_str(delta) should be compatible with the order on delta
        as_str(d1) <= as_str(d2) <=> d1 <= d2.
        """
        return "%s_%s" % (self.date_delta.as_str(), self.time_delta.as_str())

    def serialize(self):
        dd = self._date_delta.serialize()
        del dd["as_str"]

        td = self._time_delta.serialize()
        del td["as_str"]

        return {"date_delta": dd, "time_delta": td, "as_str": self.as_str()}

    def __lt__(self, other):
        if not isinstance(other, DateTimeDelta):
            _comparison_error(self, other)

        return (self.date_delta, self.time_delta) < (other.date_delta, other.time_delta)

    def __le__(self, other):
        if not isinstance(other, DateTimeDelta):
            _comparison_error(self, other)

        return (self.date_delta, self.time_delta) <= (
            other.date_delta,
            other.time_delta,
        )

    def __eq__(self, other):
        if not isinstance(other, DateTimeDelta):
            return False

        return (self.date_delta, self.time_delta) == (
            other.date_delta,
            other.time_delta,
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __neg__(self):
        return DateTimeDelta(-self.date_delta, -self.time_delta)

    # addition _only_ supports adding DateTimeDeltas to a DateTime
    def __add__(self, other):
        if not isinstance(other, DateTimeDelta):
            raise ValueError("can only add a DateTimeDelta to a DateTimeDelta")

        d = self.date_delta + other.date_delta
        t = self.time_delta + other.time_delta

        self._date_delta = d
        self._time_delta = t

        return self

    def __sub__(self, other):
        if not isinstance(other, DateTimeDelta):
            raise ValueError("can only subtract a DateTimeDelta from a DateTimeDelta")

        d = self.date_delta - other.date_delta
        t = self.time_delta - other.time_delta

        self._date_delta = d
        self._time_delta = t

        return self
