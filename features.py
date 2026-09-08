"""Feature mínima causal: retorno simple disponible al cierre de la decisión."""

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .validation import aware_time, finite_number


@dataclass(frozen=True)
class Observation:
    event_time: datetime
    available_at: datetime
    close: float


def trailing_return(observations: Iterable[Observation], as_of: datetime, lookback: int) -> float:
    """Usa las últimas lookback+1 observaciones conocidas; no rellena huecos.

    lookback cuenta observaciones, no duración ni sesiones. El resultado se
    conoce en as_of y NO implica que se pueda ejecutar al mismo precio.
    """
    cutoff = aware_time(as_of, "as_of")
    if isinstance(lookback, bool) or not isinstance(lookback, int) or lookback < 1:
        raise ValueError("lookback debe ser un entero positivo")
    eligible = []
    for row in observations:
        event = aware_time(row.event_time, "event_time")
        available = aware_time(row.available_at, "available_at")
        if available < event:
            raise ValueError("available_at no puede preceder event_time")
        if event <= cutoff and available <= cutoff:
            close = finite_number(row.close, "close")
            if close <= 0:
                raise ValueError("close debe ser positivo")
            eligible.append((event, close))
    eligible.sort(key=lambda pair: pair[0])
    if len({event for event, _ in eligible}) != len(eligible):
        raise ValueError("event_time duplicado entre observaciones disponibles")
    if len(eligible) <= lookback:
        raise ValueError("historial disponible insuficiente")
    return finite_number(eligible[-1][1] / eligible[-1 - lookback][1] - 1, "trailing_return")
