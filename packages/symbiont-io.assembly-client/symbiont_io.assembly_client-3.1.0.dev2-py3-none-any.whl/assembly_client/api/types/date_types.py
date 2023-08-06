"""
The goal here is to provide a structure and methods to handle dates.

It works by distilling operations down to the lowest level, the day.
"""
from datetime import datetime, date
from assembly_client.api.util.time import (
    DATETIME_FORMAT,
    _check_int_field,
    _comparison_error,
)

# utility functions stolen from datetime

MINYEAR = 1
MAXYEAR = 9999
MONTHS_IN_YEAR = 12
DAYS_IN_YEAR = 365
DAYS_IN_LEAP_YEAR = 366

# -1 is a placeholder for indexing purposes.
_DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def _is_leap(year):
    "year -> 1 if leap year, else 0."
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_in_month(month, year):
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


def _days_in_year(year):
    return DAYS_IN_LEAP_YEAR if _is_leap(year) else DAYS_IN_YEAR


class Date:
    # Date object structure
    # this is super basic on purpose
    # a year is just a list of months, a month is just a list of days
    # On creation a Date is checked for consistency. If, for example
    # it is created with month = 11 and day = 31 an exception will be thrown
    def __init__(self, year, month, day, timestamp=None, check_fields=True):
        self._year = year
        self._month_int = month
        self._day_int = day
        if check_fields:
            self.check_date_fields()

    def check_date_fields(self):
        year = _check_int_field(self._year)
        month = _check_int_field(self._month_int)
        day = _check_int_field(self._day_int)
        if not MINYEAR <= year <= MAXYEAR:
            raise ValueError(
                "year must be in %d..%d" % (MINYEAR, MAXYEAR),
                f"Date({year}, {month}, {day})",
            )
        if not 1 <= month <= MONTHS_IN_YEAR:
            raise ValueError(
                f"month must be in 1..{MONTHS_IN_YEAR}", f"Date({year}, {month}, {day})"
            )
        dim = _days_in_month(month, year)
        if not 1 <= day <= dim:
            raise ValueError(
                "day must be in 1..%d" % dim, f"Date({year}, {month}, {day})"
            )
        return year, month, day

    # convert from a standard string timestamp (ISO 8601) to Date
    # "2019-01-30T22:23:35.100Z" -> Date(2019, 1, 30)
    @classmethod
    def fromisotimestamp(cls, timestamp):
        dt = datetime.strptime(timestamp, DATETIME_FORMAT)
        date = cls(dt.year, dt.month, dt.day)
        return date

    # convert from a standard string timestamp (ISO 8601) to Date
    # "2019-01-30" -> Date(2019, 1, 30)
    @classmethod
    def fromisoformat(cls, str):
        dt = datetime.fromisoformat(str)
        date = cls(dt.year, dt.month, dt.day)
        return date

    # utility retrieval
    @classmethod
    def first_day_of_month(cls, month, year):
        return cls(year, month, 1)

    @classmethod
    def last_day_of_month(cls, month, year):
        day = _days_in_month(month, year)

        return cls(year, month, day)

    def __repr__(self):
        return "%s.%s(%d, %d, %d)" % (
            self.__class__.__module__,
            self.__class__.__qualname__,
            self._year,
            self._month_int,
            self._day_int,
        )

    def __str__(self):
        return self.toiso()

    # return a dict representation of the Date
    def serialize(self):
        return {
            "year": str(self._year),
            "month": str(self._month_int),
            "day": str(self._day_int),
            "timestamp": self.toisotimestamp(),
        }

    # convert the Date into an ISO8601 timestamp "YYYY-MM-DDT00:00:00.000Z"
    def toisotimestamp(self):
        return (
            datetime(self._year, self._month_int, self._day_int).isoformat() + ".000Z"
        )

    # convert the Date into an ISO8601 date
    def toiso(self):
        return date(self._year, self._month_int, self._day_int).isoformat()

    @property
    def year(self):
        """year (1-9999)"""
        return self._year

    @property
    def month(self):
        """month (1-12)"""
        return self._month_int

    @property
    def day(self):
        """day (1-31)"""
        return self._day_int

    def set_year(self, year, check_fields=False):
        return Date(year, self.month, self.day, check_fields=check_fields)

    def set_month(self, month, check_fields=False):
        return Date(self.year, month, self.day, check_fields=check_fields)

    def set_day(self, day, check_fields=False):
        return Date(self.year, self.month, day, check_fields=False)

    @property
    def day_of_week(self):
        # start the numbering on Monday = 1
        # this throws an exception if the Date is incorrect (November 31 for example)
        return datetime(self._year, self._month_int, self._day_int).isoweekday()

    @property
    def is_last_day_of_month(self):
        return self.day == _days_in_month(self.month, self.year)

    # comparisons

    def __lt__(self, other):
        if not isinstance(other, Date):
            _comparison_error(self, other)

        return (self.year, self.month, self.day) < (other.year, other.month, other.day)

    def __le__(self, other):
        if not isinstance(other, Date):
            _comparison_error(self, other)

        return (self.year, self.month, self.day) <= (other.year, other.month, other.day)

    def __eq__(self, other):
        if not isinstance(other, Date):
            return False

        return (self.year, self.month, self.day) == (other.year, other.month, other.day)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    # addition _only_ supports adding DateDeltas to a date
    def __add__(self, other):
        if not isinstance(other, DateDelta):
            raise ValueError("can only add a DateDelta to a Date")

        new_date = Date(self.year, self.month, self.day)
        if other.days > 0:
            return new_date.add_days(other.days)
        elif other.days < 0:
            return new_date.subtract_days(-other.days)
        elif other.months > 0:
            return new_date.add_months(other.months)
        elif other.months < 0:
            return new_date.subtract_months(-other.months)
        elif other.years > 0:
            return new_date.add_years(other.years)
        else:
            return new_date.subtract_years(-other.years)

    # returns
    #   a DateDelta with the number of days if other is a Date
    #   a Date if other is a DateDelta
    def __sub__(self, other):
        if isinstance(other, Date):
            return DateDelta.get_delta_in_days(self, other)
        elif isinstance(other, DateDelta):
            return self + (-other)
        else:
            raise ValueError("can only subtract a Date or DateDelta from a Date")

    # date shifting ops

    def add_days(self, num_days, date_rolling=False):
        _check_int_field(num_days)

        if num_days < 0:
            raise ValueError("number of days must be a positive integer")

        if num_days == 0:
            return self

        new_day = self._day_int + num_days
        new_month = self._month_int
        new_year = self._year

        dim = _days_in_month(new_month, new_year)
        overflow = new_day - dim

        while overflow > 0:
            # overflow is > 1 month, go to the next
            new_month += 1

            if new_month > MONTHS_IN_YEAR:
                new_month = new_month - MONTHS_IN_YEAR
                new_year += 1

            dim = _days_in_month(new_month, new_year)

            if overflow <= dim:
                new_day = overflow
                break

            overflow = overflow - dim

        new_date = Date(new_year, new_month, new_day)

        if date_rolling:
            return new_date.adjust_for_date_rolling()

        return new_date

    def add_months(self, num_months, date_rolling=False):
        _check_int_field(num_months)

        if num_months < 0:
            raise ValueError("number of months must be a positive integer")

        if num_months == 0:
            return self

        # what's our destination month?
        new_month = self._month_int + num_months
        new_year = self._year
        new_day = self._day_int

        # are we out of months?
        if new_month > MONTHS_IN_YEAR:
            new_year += (
                int(new_month / MONTHS_IN_YEAR) if num_months >= MONTHS_IN_YEAR else 1
            )

            # if the new month value is divisible by 12, we actually want the previous year
            if new_month % MONTHS_IN_YEAR == 0:
                new_year -= 1

            new_month = (
                new_month % MONTHS_IN_YEAR
                if (new_month % MONTHS_IN_YEAR) > 0
                else MONTHS_IN_YEAR
            )

        # handle day of month not falling on destination
        dim = _days_in_month(new_month, new_year)
        if self._day_int > dim:
            new_day = dim

        new_date = Date(new_year, new_month, new_day)

        if date_rolling:
            return new_date.adjust_for_date_rolling()

        return new_date

    def add_years(self, num_years, date_rolling=False):
        _check_int_field(num_years)

        if num_years < 0:
            raise ValueError("number of years must be a positive integer")

        if num_years == 0:
            return self

        # find out the destination
        new_year = self._year + num_years
        new_day = self._day_int

        # handle day of month not falling on destination
        dim = _days_in_month(self._month_int, new_year)
        if self._day_int > dim:
            new_day = dim

        new_date = Date(new_year, self._month_int, new_day)
        if date_rolling:
            return new_date.adjust_for_date_rolling()

        return new_date

    def subtract_days(self, num_days, date_rolling=False):
        _check_int_field(num_days)

        if num_days < 0:
            raise ValueError("number of days must be a positive integer")

        if num_days == 0:
            return self

        new_day = self._day_int - num_days
        new_month = self._month_int
        new_year = self._year

        underflow = 0

        if new_day < 0:
            underflow = new_day
        elif new_day == 0:
            underflow = -1

        while underflow < 0:
            # underflow is > 1 month, go to the previous
            new_month -= 1

            if new_month < 1:
                new_month = MONTHS_IN_YEAR - new_month
                new_year -= 1

            new_dim = _days_in_month(new_month, new_year)

            if abs(underflow) <= new_dim:

                if underflow + new_dim == 0:
                    new_month -= 1

                    # if underflow is equal to the dim, we need to go back one more month
                    if new_month < 1:
                        new_month = MONTHS_IN_YEAR - new_month
                        new_year -= 1
                    new_day = _days_in_month(new_month, new_year)
                else:
                    new_day = new_dim + underflow if new_day < 0 else new_dim

                break

            dim = new_dim
            underflow = underflow + dim

        new_date = Date(new_year, new_month, new_day)

        if date_rolling:
            return new_date.adjust_for_date_rolling()

        return new_date

    def subtract_months(self, num_months, date_rolling=False):
        _check_int_field(num_months)

        if num_months < 0:
            raise ValueError("number of months must be a positive integer")

        if num_months == 0:
            return self

        # what's our destination month?
        new_month = self._month_int - num_months
        new_year = self._year
        new_day = self._day_int

        # are we out of months?
        if new_month <= 0:
            new_year -= (
                int(abs(new_month) / MONTHS_IN_YEAR) + 1
                if num_months > MONTHS_IN_YEAR
                else 1
            )
            new_month = (
                new_month % MONTHS_IN_YEAR
                if (new_month % MONTHS_IN_YEAR) > 0
                else MONTHS_IN_YEAR
            )

        # handle day of month not falling on destination
        dim = _days_in_month(new_month, new_year)
        if self._day_int > dim:
            new_day = dim

        new_date = Date(new_year, new_month, new_day)

        if date_rolling:
            return new_date.adjust_for_date_rolling()

        return new_date

    def subtract_years(self, num_years, date_rolling=False):
        _check_int_field(num_years)

        if num_years < 0:
            raise ValueError("number of years must be a positive integer")

        if num_years == 0:
            return self

        # find out the destination
        new_year = self._year - num_years
        new_day = self._day_int

        # handle day of month not falling on destination
        dim = _days_in_month(self._month_int, new_year)
        if self._day_int > dim:
            new_day = dim

        new_date = Date(new_year, self._month_int, new_day)

        if date_rolling:
            return new_date.adjust_for_date_rolling()

        return new_date

    def subtract_delta(self, delta):
        if not isinstance(delta, DateDelta):
            raise ValueError("can only subtract DateDeltas")

        return self + (-delta)

    # when date rolling is needed, this is easy to plug-and-play with the above
    # https://en.wikipedia.org/wiki/Date_rolling
    def adjust_for_date_rolling(self):
        raise NotImplementedError("Keep rollin', rollin', rollin'")


# utility class to manage deltas
# can only handle one type of delta at a time -> days OR months OR years
class DateDelta:
    def __init__(self, days=0, months=0, years=0, str=None):
        # enforcing only one type
        if (
            (days and months)
            or (days and years)
            or (months and years)
            or (days and months and years)
        ):
            raise ValueError("DateDeltas can only hold one type of duration at a time")

        self._days = days
        self._months = months
        self._years = years

    def __repr__(self):
        args = []
        if self._days:
            args.append("days=%d" % self._days)
        if self._months:
            args.append("months=%d" % self._months)
        if self._years:
            args.append("years=%d" % self._years)
        if not args:
            args.append("0")
        return "%s.%s(%s)" % (
            self.__class__.__module__,
            self.__class__.__qualname__,
            ", ".join(args),
        )

    def __str__(self):
        args = []
        if self._days:
            args.append("%d days" % self._days)
        if self._months:
            args.append("%d months" % self._months)
        if self._years:
            args.append("%d years" % self._years)
        if not args:
            args.append("0")
        return "%s" % (", ".join(args))

    def as_str(self):
        """Return a string representing this delta
        the order on as_str(delta) should be compatible with the order on delta
        as_str(d1) <= as_str(d2) <=> d1 <= d2.

        For negative values we take the complement to 1000000000 (1 billion)
        This means that we can only properly deal with date delta where
        the number of days is < 1000000000 which means 2.7 million years
        """

        def if_neg(v):
            return -(1000000000 + v) if v < 0 else v

        return "%010d/%010d/%010d" % (
            if_neg(self.years),
            if_neg(self.months),
            if_neg(self.days),
        )

    def serialize(self):
        return {
            "years": str(self._years),
            "months": str(self._months),
            "days": str(self._days),
            "as_str": self.as_str(),
        }

    def __eq__(self, other):
        if not isinstance(other, DateDelta):
            return False

        return (
            self.days == other.days
            and self.months == other.months
            and self.years == other.years
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, DateDelta):
            _comparison_error(self, other)

        return (
            self._days < other.days
            or self._months < other.months
            or self._years < other.years
        )

    def __le__(self, other):
        if not isinstance(other, DateDelta):
            _comparison_error(self, other)

        return self < other or self == other

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __neg__(self):
        return DateDelta(-self._days, -self._months, -self._years)

    def __add__(self, other):
        return DateDelta(
            self._days + other._days,
            self._months + other._months,
            self._years + other._years,
        )

    def __sub__(self, other):
        return self + (-other)

    @property
    def days(self):
        return self._days

    @property
    def months(self):
        return self._months

    @property
    def years(self):
        return self._years

    # will only return a delta in days
    @classmethod
    def get_delta_in_days(cls, date_1, date_2):
        if not date_1 or not date_2:
            raise ValueError("object to compare against cannot be null")

        if not isinstance(date_1, Date) or not isinstance(date_2, Date):
            raise ValueError("can only compare two Date objects")

        if date_1 == date_2:
            return cls()

        start_date = date_2 if date_2 < date_1 else date_1
        end_date = date_1 if start_date == date_2 else date_2

        num_days = 0
        is_lookback = start_date.year != end_date.year

        if is_lookback:
            # try to just go forward in years and subtract the diff
            for y in range(start_date.year, end_date.year):
                diy = _days_in_year(y)
                num_days += diy

            # now that we've made it from the start to the target year, we can just handle the difference

            # remove start_date month from the start
            for m in range(1, start_date.month):
                dim = _days_in_month(m, start_date.year)
                num_days -= dim

            # remove start_date day
            num_days -= start_date.day

            # add the end_date month range to the end
            for m in range(1, end_date.month):
                dim = _days_in_month(m, end_date.year)
                num_days += dim

            # add the end_date day
            num_days += end_date.day
        else:
            if start_date.month != end_date.month:
                for m in range(start_date.month, end_date.month):
                    dim = _days_in_month(m, end_date.year)

                    if m == start_date.month:
                        num_days += dim - start_date.day
                    else:
                        num_days += dim

                num_days += end_date.day
            else:
                num_days = end_date.day - start_date.day

        return cls(num_days)
