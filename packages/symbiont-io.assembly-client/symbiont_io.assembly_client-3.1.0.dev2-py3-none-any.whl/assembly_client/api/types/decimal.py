import decimal as decimal

# IEEE 754 decimal128 Format
DEC_PREC = 34
DEC_EMAX = 6144
DEC_EMIN = -DEC_EMAX + 1
DEC_ETOP = DEC_EMAX - DEC_PREC + 1
DEC_ETINY = DEC_EMIN - DEC_PREC + 1
DEC_TRAPS = [
    decimal.InvalidOperation,
    decimal.DivisionByZero,
    decimal.FloatOperation,
    decimal.Underflow,
    decimal.Overflow,
]
DEC_CTX = decimal.Context(
    rounding=decimal.ROUND_HALF_EVEN,
    traps=DEC_TRAPS,
    Emax=DEC_EMAX,
    Emin=DEC_EMIN,
    clamp=1,
    prec=DEC_PREC,
)

Overflow = decimal.Overflow
Underflow = decimal.Underflow
InvalidOperation = decimal.InvalidOperation


class Decimal:
    def __init__(self, dec):
        # always round and normalize the decimal
        x = DEC_CTX.create_decimal(dec)
        self._val = DEC_CTX.normalize(x)

    @staticmethod
    def sum(ns):
        # no folds in Python
        sum = Decimal(0)
        for summand in ns:
            sum += summand
        return sum

    def __repr__(self):
        return repr(self._val)

    def round(self, n):
        return self._op(DEC_CTX.quantize, Decimal(f"1E-{n}"))

    def round_half_even(self, n):
        return self._round_with_method(n, decimal.ROUND_HALF_EVEN)

    def round_half_up(self, n):
        return self._round_with_method(n, decimal.ROUND_HALF_UP)

    def round_half_down(self, n):
        return self._round_with_method(n, decimal.ROUND_HALF_DOWN)

    def _round_with_method(self, n, rounding_method):
        ctx = DEC_CTX.copy()
        ctx.rounding = rounding_method
        return self._op(ctx.quantize, Decimal(f"1e-{n}"))

    def serialize(self):
        return str(self)

    def __str__(self):
        return str(self._val)

    def __int__(self):
        return int(self._val)

    def __eq__(self, n):
        return self._val == n._val

    def __lt__(self, n):
        return self._val < n._val

    def __le__(self, n):
        return self._val <= n._val

    def __gt__(self, n):
        return self._val > n._val

    def __ge__(self, n):
        return self._val >= n._val

    def __neg__(self):
        return self._op(DEC_CTX.minus)

    def __abs__(self):
        return self._op(DEC_CTX.abs)

    def __add__(self, n):
        return self._op(DEC_CTX.add, n)

    def __sub__(self, n):
        return self._op(DEC_CTX.subtract, n)

    def __mul__(self, n):
        return self._op(DEC_CTX.multiply, n)

    def __truediv__(self, n):
        return self._op(DEC_CTX.divide, n)

    def __floordiv__(self, n):
        return self._op(DEC_CTX.divide_int, n)

    def __pow__(self, n):
        return self._op(DEC_CTX.power, n)

    def __mod__(self, n):
        return self._op(DEC_CTX.remainder, n)

    # Helper function for operations that return a new Decimal.
    # In initialize, DEC_CTX.create_decimal creates a Decimal
    # with our rounding options, rather than the Python's global options
    # in getcontext(). It also automatically rounds, unlike Python's
    # Decimal() initializer. Then, we also immediately normalize.
    def _op(self, op, *args):
        return Decimal(op(self._val, *map(lambda x: x._val, args)))
