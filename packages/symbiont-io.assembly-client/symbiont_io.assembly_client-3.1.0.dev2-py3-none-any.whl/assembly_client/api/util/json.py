# MISNOMER: supports reading / writing of all supported Content-Types
#           not just (legacy) JSON.

from collections import OrderedDict
from typing import Union, Optional

import msgpack
import simplejson
from assembly_client.api.contracts import ContractRef


def unparse_unsupported_types(o):
    if isinstance(o, ContractRef):
        od = OrderedDict()
        od["__is_custom__"] = "contract_ref"
        od["val"] = o.__dict__
        return od
    # hack because this is shared between language versions but Decimal is introduced in lang3
    elif getattr(getattr(o, "__class__", None), "__name__", None) in [
        "Decimal",
        "CronExpression",
        "Date",
        "DateDelta",
        "DateTime",
        "DateTimeDelta",
        "Time",
        "TimeDelta",
        "KeyAlias",
        "ChannelName",
    ]:
        return o.serialize()
    else:
        raise ValueError("JSON: Can't encode {} of type {}".format(o, type(o)))


def parse_unsupported_types(o):
    if "__is_custom__" in o:
        if o["__is_custom__"] == "contract_ref":
            contract_ref = ContractRef("foo", "1.0.0", 8)
            contract_ref.__dict__ = o["val"]
            return contract_ref
        else:
            raise ValueError(
                "Unsupported type in parse_unsupported_types: {}".format(
                    o["__is_custom__"]
                )
            )
    else:
        return dict(sorted(o.items())) if type(o) is dict else o


def dumps(x, sort_keys=False):
    return simplejson.dumps(
        x, default=unparse_unsupported_types, sort_keys=sort_keys, tuple_as_array=False
    )


def loads(x):
    return simplejson.loads(x, object_hook=parse_unsupported_types)


def dump_msgpack(x):
    return msgpack.packb(x, use_bin_type=True, default=unparse_unsupported_types)


def load_msgpack(x):
    return msgpack.unpackb(x, raw=False, object_hook=parse_unsupported_types)


def to_unicode(value: Union[None, str, bytes]) -> Optional[str]:  # noqa: F811
    """Converts a string argument to a unicode string.
    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(value, (str, type(None))):
        return value
    if not isinstance(value, bytes):
        raise TypeError("Expected bytes, unicode, or None; got %r" % type(value))
    return value.decode("utf-8")
