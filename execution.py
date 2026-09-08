"""Execution from queued decisions; eligibility follows availability, not row shift."""
from dataclasses import dataclass, asdict
from datetime import timedelta
from p100_lab.engine import Costs, rebalance
from p100_foundations.validation import finite_number, aware_time


@dataclass(frozen=True)
class Target:
    weight: float
    cap: float = 1.0
    band: float = 0.0

    def __post_init__(self):
        for name in ("weight", "cap", "band"):
            if not 0 <= finite_number(getattr(self, name), name) <= 1:
                raise ValueError("objetivo inválido")
        if self.weight > self.cap:
            raise ValueError("objetivo excede límite")


def run(bars, signal, costs=Costs(), initial_cash=10000.):
    if not bars or finite_number(initial_cash, "capital") <= 0:
        raise ValueError("serie/capital inválido")
    cash, units, peak, dd = initial_cash, 0., initial_cash, 0.
    history, pending, rows, events = [], [], [], []
    for index, bar in enumerate(bars):
        op, cl, av = (aware_time(getattr(bar,n),n) for n in ("open_time","close_time","available_at"))
        if not op < cl <= av or av-cl >= timedelta(days=1):
            raise ValueError("reloj o retraso no soportado")
        if history and (op <= history[-1].close_time or av <= history[-1].available_at):
            raise ValueError("orden temporal inválido")
        if min(finite_number(bar.open,"open"), finite_number(bar.close,"close")) <= 0:
            raise ValueError("precio inválido")
        eligible = [d for d in pending if d["time"] < op]
        pending = [d for d in pending if d["time"] >= op]
        if eligible:
            decision = eligible[-1]
            target = decision["target"]
            equity = cash + units*bar.open
            current = units*bar.open/equity
            skip = (target.band>0 and abs(current-target.weight)<target.band
                    and current<=target.cap and target.weight>0)
            event = dict(index=index, decision_index=decision["index"], decision_time=decision["time"].isoformat(),
                         fill_time=op.isoformat(), current_weight=current, requested=asdict(target),
                         skipped=skip, superseded=len(eligible)-1)
            if not skip:
                fill = rebalance(cash, units, bar.open, target.weight, costs)
                cash, units = fill.cash, fill.units
                event["fill"] = asdict(fill)
            events.append(event)
        equity = cash + units*bar.close
        finite_number(equity, "equity")
        peak = max(peak, equity)
        dd = min(dd, equity/peak-1)
        history.append(bar)
        # Availability is strictly monotone: entire prefix is known at this decision time.
        target = signal(tuple(history))
        if target is not None:
            if not isinstance(target, Target):
                raise ValueError("el callback debe devolver Target o None")
            pending.append(dict(index=index, time=av, target=target))
        rows.append(dict(index=index, time=cl.isoformat(), cash=cash, units=units, equity=equity,
                         exposure=units*bar.close/equity, next_target=asdict(target) if target else None))
    fills = [e["fill"] for e in events if "fill" in e]
    metrics = dict(total_return=equity/initial_cash-1, max_drawdown=dd, ending_equity=equity,
                   fees=sum(f["fee"] for f in fills), slippage=sum(f["slippage"] for f in fills),
                   turnover=sum(abs(e["fill"]["quantity"])*bars[e["index"]].open/e["fill"]["equity_before"] for e in events if "fill" in e),
                   mean_exposure=sum(r["exposure"] for r in rows)/len(rows),
                   trades=sum(abs(f["quantity"])>1e-10 for f in fills), band_skips=sum(e["skipped"] for e in events),
                   pending_unfilled=len(pending), bars=len(bars))
    return dict(metrics=metrics, rows=rows, events=events)
