"""Offline replay of captured observations, including duplicate detection in the real ledger."""
from contextlib import closing
from dataclasses import asdict
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sqlite3

from market_lab.shadow import closed_history,record_intention
from market_lab.signals import make_signal

root=Path(__file__).resolve().parent
shadow=root/"results/shadow"
capture=sorted(p for p in shadow.iterdir() if p.is_dir())[-1]
snapshot=json.loads((capture/"SNAPSHOT.json").read_text())
fields=("symbol","policy","bar_close","target","data_sha256","code_sha256","execution_enabled","type")
count=0
for item in snapshot:
    raw=json.loads((capture/(item["symbol"]+".raw.json")).read_text())
    instrument,bars,completed=closed_history(raw,datetime.fromisoformat(item["observed_at"]),item["symbol"])
    assert item["target"]==asdict(make_signal(item["policy"],instrument)(tuple(bars)))
    assert item["data_sha256"]==hashlib.sha256(json.dumps(completed,separators=(",",":")).encode()).hexdigest()
    assert item["bar_close"]==bars[-1].close_time.isoformat()
    assert item["execution_enabled"] is False
    payload={f:item[f] for f in fields}
    key=item["symbol"]+"|"+item["policy"]+"|"+item["bar_close"]
    assert record_intention(shadow/"intentions.sqlite",key,payload,item["observed_at"])=="duplicate"
    count+=1
with closing(sqlite3.connect(shadow/"intentions.sqlite")) as db:
    assert db.execute("SELECT COUNT(*) FROM intentions").fetchone()[0]==6
result=dict(status="PASS",snapshot_replays=count,duplicates_detected=count,unique_intentions=6,orders_sent=0)
(shadow/"AUDIT.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result))
