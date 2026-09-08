"""Simulador spot long/cash con señales de cierre y fills a próxima apertura."""
from dataclasses import dataclass, asdict
from datetime import datetime
import math
from typing import Callable

from p100_foundations.validation import aware_time, finite_number


@dataclass(frozen=True)
class Bar:
    open_time: datetime
    close_time: datetime
    available_at: datetime
    open: float
    close: float


@dataclass(frozen=True)
class Costs:
    fee_bps: float = 10.0
    slippage_bps: float = 5.0

    def __post_init__(self):
        for name in ("fee_bps", "slippage_bps"):
            value = finite_number(getattr(self, name), name)
            if not 0 <= value < 10000:
                raise ValueError("costes fuera de rango")


@dataclass(frozen=True)
class Fill:
    quantity: float
    price: float
    fee: float
    slippage: float
    cash: float
    units: float
    equity_before: float
    equity_after: float
    target: float


def rebalance(cash: float, units: float, price: float, target: float, costs: Costs) -> Fill:
    for name, value in (("cash", cash), ("units", units), ("price", price), ("target", target)):
        finite_number(value, name)
    if cash < 0 or units < 0 or price <= 0 or not 0 <= target <= 1:
        raise ValueError("estado o peso inválido")
    equity = cash + units * price
    finite_number(equity, "equity")
    f, s = costs.fee_bps / 10000, costs.slippage_bps / 10000
    gap = target * equity - units * price
    if gap >= 0:
        execution = price * (1 + s)
        loss_per_unit = execution * (1 + f) - price
        delta = gap / (price + target * loss_per_unit)
    else:
        execution = price * (1 - s)
        loss_per_unit = price - execution * (1 - f)
        delta = gap / (price - target * loss_per_unit)
    fee = abs(delta) * execution * f
    slip = abs(delta) * abs(execution - price)
    new_cash = cash - delta * execution - fee
    new_units = units + delta
    tolerance = max(1.0, equity) * 1e-10
    if new_cash < -tolerance or new_units * price < -tolerance:
        raise ArithmeticError("saldo negativo tras ejecución")
    new_cash, new_units = max(0.0, new_cash), max(0.0, new_units)
    after = new_cash + new_units * price
    if not math.isclose(after, equity - fee - slip, rel_tol=1e-10, abs_tol=1e-8):
        raise ArithmeticError("fallo de reconciliación")
    return Fill(delta, execution, fee, slip, new_cash, new_units, equity, after, target)


def validate_bar(bar: Bar, previous: Bar | None):
    opening = aware_time(bar.open_time, "open_time")
    closing = aware_time(bar.close_time, "close_time")
    available = aware_time(bar.available_at, "available_at")
    if not opening < closing <= available:
        raise ValueError("reloj de barra inválido")
    if previous is not None:
        if opening <= previous.close_time or opening <= previous.available_at:
            raise ValueError("barra solapada o cierre anterior aún no disponible")
    if finite_number(bar.open, "open") <= 0 or finite_number(bar.close, "close") <= 0:
        raise ValueError("precio no positivo")


def run(bars: list[Bar], signal: Callable, costs: Costs = Costs(), initial_cash=10000.0) -> dict:
    if finite_number(initial_cash, "initial_cash") <= 0 or not bars:
        raise ValueError("capital o serie vacía inválidos")
    cash, units, pending = initial_cash, 0.0, None
    rows, fills, history = [], [], []
    previous = None
    for index, bar in enumerate(bars):
        validate_bar(bar, previous)
        if pending is not None:
            fill = rebalance(cash, units, bar.open, pending, costs)
            cash, units = fill.cash, fill.units
            fills.append(dict(index=index, decision_index=index - 1,
                              decision_time=previous.available_at.isoformat(),
                              fill_time=bar.open_time.isoformat(), **asdict(fill)))
        equity = cash + units * bar.close
        finite_number(equity, "mark_to_market")
        history.append(bar)
        # Callback receives only observations whose availability has been validated.
        pending = signal(tuple(history))
        if pending is not None and not 0 <= finite_number(pending, "signal") <= 1:
            raise ValueError("señal fuera de [0,1]")
        rows.append(dict(index=index, time=bar.close_time.isoformat(), cash=cash,
                         units=units, equity=equity, exposure=units * bar.close / equity,
                         next_target=pending))
        previous = bar
    peak, drawdown = initial_cash, 0.0
    for row in rows:
        peak = max(peak, row["equity"])
        drawdown = min(drawdown, row["equity"] / peak - 1)
    metrics = dict(total_return=rows[-1]["equity"] / initial_cash - 1,
                   max_drawdown=drawdown, ending_equity=rows[-1]["equity"],
                   fees=sum(x["fee"] for x in fills), slippage=sum(x["slippage"] for x in fills),
                   turnover=sum(abs(x["quantity"]) * bars[x["index"]].open / x["equity_before"] for x in fills),
                   mean_exposure=sum(r["exposure"] for r in rows) / len(rows),
                   trades=sum(abs(x["quantity"]) > 1e-10 for x in fills),
                   pending_unfilled=int(pending is not None))
    return dict(metrics=metrics, rows=rows, fills=fills)
