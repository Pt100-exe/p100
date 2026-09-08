"""Freeze, fetch public data and run the prespecified historical development study."""
import argparse
import csv
from dataclasses import asdict
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request

from p100_lab.engine import Costs
from .data import Instrument, parse_klines
from .execution import run
from .signals import POLICIES, make_signal

ROOT = Path(__file__).resolve().parents[1]
START = datetime(2025,1,1,tzinfo=timezone.utc)
END = datetime(2026,1,1,tzinfo=timezone.utc)
SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, obj):
    with path.open("x", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, allow_nan=False)


def public_get(params):
    url = "https://data-api.binance.vision/api/v3/klines?"+urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent":"P100-Research/0.2"})
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read()
    return url, content


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--run",default="study_002")
    args=parser.parse_args()
    if not args.run.replace("_", "").isalnum():
        raise ValueError("identificador de ejecución inválido")
    out = ROOT/"results"/args.run
    out.mkdir(exist_ok=False, parents=True)
    source_files = [ROOT/"PROTOCOL_002.md", *sorted(ROOT.glob("market_lab/*.py")),
                    *sorted(ROOT.glob("p100_lab/*.py")), *sorted(ROOT.glob("p100_foundations/*.py")), *sorted(ROOT.glob("tests/*.py"))]
    write_json(out/"PRE_DATA_FREEZE.json", dict(created_utc=datetime.now(timezone.utc).isoformat(),
        experiment="study_002", status="HISTORICAL_DEVELOPMENT_NOT_UNSEEN_HOLDOUT",
        symbols=SYMBOLS, start=START.isoformat(), end_exclusive=END.isoformat(), policies=POLICIES,
        fees_bps=[0,10,30], latency_assumed_seconds=1, band=.05,
        hashes={p.relative_to(ROOT).as_posix():sha(p) for p in source_files}))
    datasets, catalog = {}, []
    for symbol in SYMBOLS:
        raw_path=ROOT/"data"/(symbol+"_2025.raw.json")
        if raw_path.exists():
            raise FileExistsError("No sobrescribir datos existentes")
        try:
            url, content=public_get(dict(symbol=symbol,interval="1d",startTime=int(START.timestamp()*1000),
                                        endTime=int(END.timestamp()*1000)-1,limit=1000))
            raw_path.write_bytes(content)
            instrument=Instrument(symbol,"crypto_spot","USDT",365,"daily_24x7")
            bars, normalized=parse_klines(json.loads(content),instrument,START,END)
            normalized_path=ROOT/"data"/(symbol+"_2025.csv")
            with normalized_path.open("x", newline="",encoding="utf-8") as f:
                w=csv.DictWriter(f,fieldnames=list(normalized[0])); w.writeheader(); w.writerows(normalized)
            catalog.append(dict(instrument=asdict(instrument), url=url, fetched_utc=datetime.now(timezone.utc).isoformat(),
                                rows=len(bars), raw_file=raw_path.relative_to(ROOT).as_posix(), raw_sha256=sha(raw_path),
                                normalized_file=normalized_path.relative_to(ROOT).as_posix(), normalized_sha256=sha(normalized_path),
                                availability="ASSUMED_close_time_plus_1_second", license="Public endpoint; redistribution rights not independently established"))
            datasets[symbol]=instrument,bars
            print(symbol+": 365 barras reales validadas",flush=True)
        except Exception as exc:
            write_json(out/"FETCH_FAILURE.json",dict(symbol=symbol,error=repr(exc),time=datetime.now(timezone.utc).isoformat()))
            raise
    write_json(out/"DATA_CATALOG.json",catalog)
    write_json(out/"PRE_RUN_DATA_FREEZE.json",{c["raw_file"]:c["raw_sha256"] for c in catalog})
    all_metrics, quarterly=[] ,[]
    with gzip.open(out/"all_ledgers.jsonl.gz","wt",encoding="utf-8") as ledger:
        for symbol,(instrument,bars) in datasets.items():
            for fee in (0,10,30):
                for policy in POLICIES:
                    result=run(bars,make_signal(policy,instrument),Costs(fee,0 if fee==0 else 5))
                    metadata=dict(symbol=symbol,fee_bps=fee,policy=policy)
                    all_metrics.append(dict(**metadata,**result["metrics"]))
                    ledger.write(json.dumps(dict(**metadata,**result),separators=(",",":"),allow_nan=False)+"\n")
                    previous=10000.
                    for q in range(1,5):
                        block=[r for r in result["rows"] if (int(r["time"][5:7])-1)//3+1==q]
                        ending=block[-1]["equity"]
                        quarterly.append(dict(**metadata,quarter=q,starting_equity=previous,ending_equity=ending,total_return=ending/previous-1))
                        previous=ending
    for filename,rows in (("all_metrics.csv",all_metrics),("quarterly.csv",quarterly)):
        with (out/filename).open("x",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    decisions=[]
    for symbol in SYMBOLS:
        a=next(r for r in all_metrics if r["symbol"]==symbol and r["fee_bps"]==10 and r["policy"]=="core_tactical_band")
        b=next(r for r in all_metrics if r["symbol"]==symbol and r["fee_bps"]==10 and r["policy"]=="core_tactical_risk")
        h1=a["turnover"]<=b["turnover"] and a["fees"]+a["slippage"]<=b["fees"]+b["slippage"]
        h2=a["total_return"]-b["total_return"]>=-.01 and a["max_drawdown"]-b["max_drawdown"]>=-.01
        decisions.append(dict(symbol=symbol, H1_costs=h1, H2_degradation=h2,
                              return_delta=a["total_return"]-b["total_return"], drawdown_delta=a["max_drawdown"]-b["max_drawdown"],
                              turnover_delta=a["turnover"]-b["turnover"], costs_delta=a["fees"]+a["slippage"]-b["fees"]-b["slippage"]))
    conclusion=dict(promote_band=all(d["H1_costs"] and d["H2_degradation"] for d in decisions),decisions=decisions,
                    runs=len(all_metrics), status="DEVELOPMENT_RESULT_NOT_PROOF_OF_ALPHA")
    write_json(out/"HYPOTHESIS_RESULT.json",conclusion)
    print(json.dumps(conclusion),flush=True)


if __name__=="__main__":
    main()
