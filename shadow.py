"""One-shot observation of closed public bars; persistent intentions, no broker or orders."""
from dataclasses import asdict
from contextlib import closing
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sqlite3

from .data import Instrument,parse_klines
from .signals import make_signal
from .study import public_get, ROOT, SYMBOLS


def record_intention(database, key, payload, observed_at):
    canonical=json.dumps(payload,sort_keys=True,separators=(",",":"),allow_nan=False)
    digest=hashlib.sha256(canonical.encode()).hexdigest()
    with closing(sqlite3.connect(database)) as db, db:
        db.execute("CREATE TABLE IF NOT EXISTS intentions (key TEXT PRIMARY KEY, payload TEXT NOT NULL, hash TEXT NOT NULL, observed_at TEXT NOT NULL)")
        db.execute("BEGIN IMMEDIATE")
        row=db.execute("SELECT payload, hash FROM intentions WHERE key=?",(key,)).fetchone()
        if row:
            if row!=(canonical,digest):
                raise ValueError("conflicto: misma decisión con contenido diferente")
            return "duplicate"
        db.execute("INSERT INTO intentions VALUES (?,?,?,?)",(key,canonical,digest,observed_at))
    return "recorded"


def closed_history(raw, observed_at, symbol):
    # Local acquisition time records when this research process actually saw the data.
    completed=[r for r in raw if type(r[6]) is int and r[6]/1000+1<=observed_at.timestamp()]
    if len(completed)<31:
        raise ValueError("historial cerrado insuficiente")
    end_ms=completed[-1][6]+1
    end=datetime.fromtimestamp(end_ms/1000,timezone.utc)
    start=datetime.fromtimestamp(completed[0][0]/1000,timezone.utc)
    if observed_at-end>timedelta(days=2):
        raise ValueError("datos demasiado antiguos para observación actual")
    instrument=Instrument(symbol,"crypto_spot","USDT",365,"daily_24x7")
    bars,_=parse_klines(completed,instrument,start,end)
    return instrument,bars,completed


def main():
    root=ROOT/"results/shadow"
    root.mkdir(exist_ok=True,parents=True)
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    capture=root/stamp
    capture.mkdir(exist_ok=False)
    code_files=[*sorted((ROOT/"market_lab").glob("*.py")), *sorted((ROOT/"p100_foundations").glob("*.py"))]
    code_hash=hashlib.sha256(b"".join(p.name.encode()+p.read_bytes() for p in code_files)).hexdigest()
    summary=[]
    for symbol in SYMBOLS:
        url,content=public_get(dict(symbol=symbol,interval="1d",limit=65))
        observed=datetime.now(timezone.utc)
        (capture/(symbol+".raw.json")).write_bytes(content)
        instrument,bars,completed=closed_history(json.loads(content),observed,symbol)
        data_hash=hashlib.sha256(json.dumps(completed,separators=(",",":")).encode()).hexdigest()
        for policy in ("core_risk","core_tactical_band"):
            target=make_signal(policy,instrument)(tuple(bars))
            payload=dict(symbol=symbol,policy=policy,bar_close=bars[-1].close_time.isoformat(),
                         target=asdict(target),data_sha256=data_hash,code_sha256=code_hash,
                         execution_enabled=False,type="RESEARCH_INTENTION_ONLY")
            key=symbol+"|"+policy+"|"+payload["bar_close"]
            status=record_intention(root/"intentions.sqlite",key,payload,observed.isoformat())
            summary.append(dict(**payload,status=status,observed_at=observed.isoformat(),
                                earliest_execution="NOT_EXECUTED; any future simulation must use an opening strictly after observed_at",source_url=url))
    (capture/"SNAPSHOT.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(dict(capture=str(capture),intentions=len(summary),statuses=[r["status"] for r in summary],execution_enabled=False)))


if __name__=="__main__":
    main()
