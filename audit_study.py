"""Recompute saved cash/units/metrics without calling the execution engine."""
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results/study_002_retry"


def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7),(a,b)


def main():
    freeze=json.loads((OUT/"PRE_DATA_FREEZE.json").read_text())
    for name,value in freeze["hashes"].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==value,name
    datasets={}
    for c in json.loads((OUT/"DATA_CATALOG.json").read_text()):
        for key in ("raw", "normalized"):
            assert hashlib.sha256((ROOT/c[key+"_file"]).read_bytes()).hexdigest()==c[key+"_sha256"]
        with (ROOT/c["normalized_file"]).open(encoding="utf-8",newline="") as f:
            datasets[c["instrument"]["symbol"]]=list(csv.DictReader(f))
    with (OUT/"all_metrics.csv").open(encoding="utf-8",newline="") as f:
        expected={(r["symbol"],int(r["fee_bps"]),r["policy"]):r for r in csv.DictReader(f)}
    seen=set(); row_count=event_count=0
    with gzip.open(OUT/"all_ledgers.jsonl.gz","rt",encoding="utf-8") as f:
        for line in f:
            r=json.loads(line); key=(r["symbol"],r["fee_bps"],r["policy"])
            assert key not in seen
            seen.add(key)
            bars=datasets[key[0]]
            events={e["index"]:e for e in r["events"]}
            assert len(events)==len(r["events"])
            cash=peak=10000.; units=dd=fees=slip=turnover=exposure=0.
            for i,row in enumerate(r["rows"]):
                b=bars[i]; opening=float(b["open"])
                if i in events:
                    e=events[i]; d=e["decision_index"]
                    assert d==i-2 and e["decision_time"]==bars[d]["available_at_assumed"]
                    assert e["decision_time"] < e["fill_time"]==b["open_time"]
                    assert e["requested"]==r["rows"][d]["next_target"]
                    before=cash+units*opening; current=units*opening/before
                    target=e["requested"]
                    should_skip=target["band"]>0 and abs(current-target["weight"])<target["band"] and current<=target["cap"] and target["weight"]>0
                    assert e["skipped"]==should_skip
                    if not e["skipped"]:
                        fill=e["fill"]; delta=fill["quantity"]
                        rate=0 if key[1]==0 else .0005
                        price=opening*(1+rate if delta>=0 else 1-rate)
                        fee=abs(delta)*price*key[1]/10000
                        slippage=abs(delta)*abs(price-opening)
                        cash-=delta*price+fee; units+=delta
                        after=cash+units*opening
                        close(price,fill["price"]); close(fee,fill["fee"]); close(slippage,fill["slippage"])
                        close(before,fill["equity_before"]); close(after,fill["equity_after"])
                        close(after,before-fee-slippage); close(units*opening/after,target["weight"])
                        close(cash,fill["cash"]); close(units,fill["units"])
                        fees+=fee; slip+=slippage; turnover+=abs(delta)*opening/before
                    event_count+=1
                eq=cash+units*float(b["close"])
                close(eq,row["equity"]); close(cash,row["cash"]); close(units,row["units"])
                assert cash>=-1e-7 and units>=-1e-7
                peak=max(peak,eq); dd=min(dd,eq/peak-1)
                close(row["exposure"],units*float(b["close"])/eq)
                exposure+=row["exposure"]; row_count+=1
            metrics=dict(total_return=eq/10000-1,max_drawdown=dd,ending_equity=eq,fees=fees,slippage=slip,turnover=turnover,mean_exposure=exposure/len(bars))
            for field,value in metrics.items():
                close(value,r["metrics"][field]); close(value,float(expected[key][field]))
    assert len(seen)==45 and seen==set(expected)
    result=dict(status="PASS",runs=len(seen),states=row_count,events=event_count,source_files_verified=len(freeze["hashes"]),raw_and_normalized_datasets_verified=6)
    (OUT/"AUDIT.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result))


if __name__=="__main__":
    main()
