"""Contratos comunes: números finitos y tiempos explícitos."""

from datetime import datetime, timezone
from math import isfinite
from numbers import Real


def finite_number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name}: se exige un número real finito")
    try:
        result = float(value)
    except (ValueError, OverflowError) as exc:
        raise ValueError(f"{name}: no representable") from exc
    if not isfinite(result):
        raise ValueError(f"{name}: no finito")
    return result


def aware_time(value: datetime, name: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name}: se exige datetime con zona horaria")
    return value.astimezone(timezone.utc)
