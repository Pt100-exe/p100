"""Ejecutar con python -B -m p100_lab.experiment; resultados nuevos, sin sobrescribir."""
import argparse
import csv
from datetime import datetime, timedelta, timezone
import gzip
import hashlib
import json
import math
from pathlib import Path
import random
from statistics import mean, median
import sys

from .engine import Bar, Costs, run
from .signals import MODES, make_signal

SCENARIOS = ("rally", "bear", "sideways", "whipsaw", "crash_recovery", "high_vol")


def generate(scenario, seed, count=360):
    rng = random.Random(seed)
    start = datetime(2000, 1, 1, tzinfo=timezone.utc)
    previous = 100.0
    data = []
    for i in range(count):
        drift, sigma = {
            "rally": (.002, .012), "bear": (-.002, .012),
            "sideways": (0, .012), "whipsaw": (.004 if (i//15)%2==0 else -.004, .012),
            "crash_recovery": (.001 if i<150 else (-.014 if i<175 else .002), .016),
            "high_vol": (.001, .05),
        }[scenario]
        # Independent overnight and intraday log increments; no observed market prices.
        opening = previous * math.exp(drift*.25 + sigma*.5*rng.gauss(0, 1))
        closing = opening * math.exp(drift*.75 + sigma*math.sqrt(.75)*rng.gauss(0, 1))
        t = start + timedelta(days=i)
        data.append(Bar(t, t+timedelta(seconds=86399), t+timedelta(seconds=86399), opening, closing))
        previous = closing
    return data


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/run_001", help="Carpeta nueva, relativa al laboratorio")
    args = parser.parse_args()
    out = (root / args.output).resolve()
    if not out.is_relative_to(root):
        raise ValueError("la salida debe permanecer dentro del laboratorio")
    out.mkdir(parents=True, exist_ok=False)
    inputs = {}
    for scenario in SCENARIOS:
        for seed in range(30):
            inputs[scenario, seed] = generate(scenario, seed)
    with (out/"synthetic_bars.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["scenario", "seed", "index", "open_time", "close_time", "available_at", "open", "close"])
        for (scenario, seed), data in inputs.items():
            for i, b in enumerate(data):
                writer.writerow([scenario, seed, i, b.open_time.isoformat(), b.close_time.isoformat(), b.available_at.isoformat(), repr(b.open), repr(b.close)])
    files = [root/"PROTOCOL.md", *sorted(root.glob("p100_lab/*.py")), *sorted(root.glob("p100_foundations/*.py")), *sorted(root.glob("tests/*.py")), *sorted(root.glob("config/*.json"))]
    freeze = dict(created_utc=datetime.now(timezone.utc).isoformat(), python=sys.version,
                  status="SYNTHETIC_ENGINEERING_ONLY_NO_REAL_HOLDOUT", seeds=list(range(30)), bars=360,
                  fees_bps=[0, 10, 30], slippage_bps=[0, 5, 5], scenarios=SCENARIOS, policies=MODES,
                  inputs={p.relative_to(root).as_posix(): digest(p) for p in files},
                  dataset_sha256=digest(out/"synthetic_bars.csv"))
    (out/"PRE_RUN_FREEZE.json").write_text(json.dumps(freeze, indent=2), encoding="utf-8")
    metrics = []
    with gzip.open(out/"all_ledgers.jsonl.gz", "wt", encoding="utf-8", compresslevel=1) as ledger:
        for (scenario, seed), data in inputs.items():
            for fee in (0, 10, 30):
                for mode in MODES:
                    r = run(data, make_signal(mode), Costs(fee, 0 if fee==0 else 5))
                    metadata = dict(scenario=scenario, seed=seed, fee_bps=fee, policy=mode)
                    metrics.append(dict(**metadata, **r["metrics"]))
                    ledger.write(json.dumps(dict(**metadata, **r), separators=(",", ":"), allow_nan=False)+"\n")
            if seed == 29:
                print(f"{scenario}: completado ({len(metrics)} simulaciones acumuladas)", flush=True)
    with (out/"all_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(metrics[0]))
        w.writeheader()
        w.writerows(metrics)
    grouped = []
    for scenario in SCENARIOS:
        for fee in (0, 10, 30):
            for mode in MODES:
                rows = [r for r in metrics if r["scenario"]==scenario and r["fee_bps"]==fee and r["policy"]==mode]
                grouped.append(dict(scenario=scenario, fee_bps=fee, policy=mode,
                                    median_return=median(r["total_return"] for r in rows),
                                    median_drawdown=median(r["max_drawdown"] for r in rows),
                                    mean_exposure=mean(r["mean_exposure"] for r in rows),
                                    median_cost=median(r["fees"]+r["slippage"] for r in rows)))
    (out/"summary.json").write_text(json.dumps(grouped, indent=2), encoding="utf-8")
    paired = []
    lookup = {(r["scenario"], r["seed"], r["fee_bps"], r["policy"]): r for r in metrics}
    for scenario in SCENARIOS:
        for fee in (0, 10, 30):
            for lhs, rhs in (("core_tactical_risk", "core_risk"), ("core_tactical_risk", "core_tactical"), ("core_tactical_risk", "buy_hold")):
                pairs = [(lookup[scenario, seed, fee, lhs], lookup[scenario, seed, fee, rhs]) for seed in range(30)]
                paired.append(dict(scenario=scenario, fee_bps=fee, lhs=lhs, rhs=rhs,
                    median_return_difference=median(a["total_return"]-b["total_return"] for a,b in pairs),
                    median_drawdown_difference=median(a["max_drawdown"]-b["max_drawdown"] for a,b in pairs),
                    return_wins=sum(a["total_return"]>b["total_return"] for a,b in pairs), n=30))
    (out/"paired.json").write_text(json.dumps(paired, indent=2), encoding="utf-8")
    print(json.dumps(dict(runs=len(metrics), dataset_rows=sum(map(len, inputs.values())))), flush=True)


if __name__ == "__main__":
    main()
