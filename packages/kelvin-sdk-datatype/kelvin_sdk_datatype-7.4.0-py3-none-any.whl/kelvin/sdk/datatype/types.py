"""Standard types."""

from __future__ import annotations

from sys import float_info

from pydantic import ConstrainedFloat, ConstrainedInt


class UInt8_(ConstrainedInt):
    """Unsigned 8-bit integer."""

    strict = True
    ge = 0
    le = (1 << 8) - 1


class UInt16_(ConstrainedInt):
    """Unsigned 16-bit integer."""

    strict = True
    ge = 0
    le = (1 << 16) - 1


class UInt32_(ConstrainedInt):
    """Unsigned 32-bit integer."""

    strict = True
    ge = 0
    le = (1 << 32) - 1


class UInt64_(ConstrainedInt):
    """Unsigned 64-bit integer."""

    strict = True
    ge = 0
    le = (1 << 64) - 1


class Int8_(ConstrainedInt):
    """Signed 8-bit integer."""

    strict = True
    ge = -1 << 7
    le = (1 << 7) - 1


class Int16_(ConstrainedInt):
    """Signed 16-bit integer."""

    strict = True
    ge = -1 << 15
    le = (1 << 15) - 1


class Int32_(ConstrainedInt):
    """Signed 32-bit integer."""

    strict = True
    ge = -1 << 31
    le = (1 << 31) - 1


class Int64_(ConstrainedInt):
    """Signed 64-bit integer."""

    strict = True
    ge = (-1 << 63) + 1  # off-by one to deal with C++ issue
    le = (1 << 63) - 1


class Float32_(ConstrainedFloat):
    """32-bit floating-point number."""

    ge = -3.4028235e38
    le = 3.4028235e38


class Float64_(ConstrainedFloat):
    """64-bit floating-point number."""

    ge = -float_info.max
    le = float_info.max
