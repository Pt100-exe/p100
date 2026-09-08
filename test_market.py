from dataclasses import replace
from datetime import datetime, timedelta, timezone
import math
import unittest
from p100_lab.engine import Bar, Costs
from market_lab.data import Instrument, parse_klines
from market_lab.execution import Target, run
from market_lab.signals import make_signal, POLICIES

START = datetime(2025,1,1,tzinfo=timezone.utc)
CRYPTO = Instrument("BTCUSDT", "crypto_spot", "USDT", 365, "daily_24x7")


def data(n=100):
    out = []
    for i in range(n):
        t = START + timedelta(days=i)
        p = 100*math.exp(.001*i+.04*math.sin(i))
        out.append([int(t.timestamp()*1000),str(p),str(p*1.05),str(p*.95),str(p),"10",int((t+timedelta(days=1)).timestamp()*1000)-1,"10",10,"5","5","0"])
    return out


class MarketTests(unittest.TestCase):
    def test_parse_full_schema_and_assumed_availability(self):
        bars, rows = parse_klines(data(3), CRYPTO, START, START+timedelta(days=3))
        self.assertEqual(bars[0].available_at, START+timedelta(days=1,microseconds=999000))
        self.assertEqual(len(rows), 3)

    def test_gap_duplicate_microseconds_and_ohlc_rejected(self):
        for mutate in (lambda r: r[1].__setitem__(0, r[0][0]),
                       lambda r: r[0].__setitem__(0, r[0][0]*1000),
                       lambda r: r[0].__setitem__(2, "1"),
                       lambda r: r[0].__setitem__(5, "-1"),
                       lambda r: r[0].__setitem__(4, "nan")):
            rows=data(3)
            mutate(rows)
            with self.assertRaises(ValueError):
                parse_klines(rows, CRYPTO, START, START+timedelta(days=3))

    def test_missing_coverage_rejected(self):
        with self.assertRaises(ValueError):
            parse_klines(data(2), CRYPTO, START, START+timedelta(days=3))

    def test_latency_one_second_fills_at_t_plus_two(self):
        bars,_=parse_klines(data(4), CRYPTO, START, START+timedelta(days=4))
        r=run(bars, lambda h: Target(1), Costs(0,0))
        self.assertEqual(r["events"][0]["index"],2)
        self.assertEqual(r["events"][0]["decision_index"],0)
        self.assertEqual(r["metrics"]["pending_unfilled"],2)

    def test_zero_latency_model_fills_at_t_plus_one(self):
        bars,_=parse_klines(data(4), CRYPTO, START, START+timedelta(days=4),latency_seconds=0)
        self.assertEqual(run(bars,lambda h:Target(1))["events"][0]["index"],1)

    def test_band_skips_small_change(self):
        bars,_=parse_klines(data(4),CRYPTO,START,START+timedelta(days=4))
        bars=[replace(b,open=100,close=100) for b in bars]
        r=run(bars,lambda h:Target(.4 if len(h)==1 else .42,1,.05),Costs(0,0))
        self.assertTrue(r["events"][1]["skipped"])
        self.assertAlmostEqual(r["rows"][-1]["exposure"],.4)

    def test_band_cannot_bypass_risk_cap(self):
        bars,_=parse_klines(data(4),CRYPTO,START,START+timedelta(days=4))
        bars=[replace(b,open=100,close=100) for b in bars]
        r=run(bars,lambda h:Target(.4,1,.05) if len(h)==1 else Target(.39,.39,.05),Costs(0,0))
        self.assertFalse(r["events"][1]["skipped"])
        self.assertAlmostEqual(r["rows"][-1]["exposure"],.39)

    def test_band_zero_target_exits_even_small_position(self):
        bars,_=parse_klines(data(4),CRYPTO,START,START+timedelta(days=4))
        bars=[replace(b,open=100,close=100) for b in bars]
        r=run(bars,lambda h:Target(.03,1,.05) if len(h)==1 else Target(0,1,.05),Costs(0,0))
        # Seed position must be bigger than band to create it; use zero band first.
        r=run(bars,lambda h:Target(.03,1,0) if len(h)==1 else Target(0,1,.05),Costs(0,0))
        self.assertEqual(r["rows"][-1]["units"],0)
        self.assertFalse(r["events"][1]["skipped"])

    def test_future_invariance_with_delays_and_band(self):
        bars,_=parse_klines(data(),CRYPTO,START,START+timedelta(days=100))
        cut=60
        changed=bars[:cut]+[replace(b,open=b.open*.2,close=b.close*5) for b in bars[cut:]]
        for policy in POLICIES:
            a=run(bars,make_signal(policy,CRYPTO))
            b=run(changed,make_signal(policy,CRYPTO))
            c=run(bars[:cut],make_signal(policy,CRYPTO))
            self.assertEqual(a["rows"][:cut],b["rows"][:cut])
            self.assertEqual(a["rows"][:cut],c["rows"])
            self.assertEqual([e for e in a["events"] if e["index"]<cut],c["events"])

    def test_unsupported_contracts_and_calendar_rejected(self):
        with self.assertRaises(ValueError):
            Instrument("ES", "future", "USD",252,"explicit_sessions")
        equity=Instrument("EXAMPLE", "equity_spot", "USD",252,"explicit_sessions")
        with self.assertRaises(ValueError):
            parse_klines(data(2),equity,START,START+timedelta(days=2))

    def test_targets_and_bad_clock_rejected(self):
        for w,cap,band in ((1,.5,0),(.4,1,-1),(math.nan,1,0)):
            with self.assertRaises(ValueError):
                Target(w,cap,band)
        bars,_=parse_klines(data(2),CRYPTO,START,START+timedelta(days=2))
        bars[0]=replace(bars[0],available_at=bars[0].close_time+timedelta(days=2))
        with self.assertRaises(ValueError):
            run(bars,lambda h:Target(0))


if __name__=="__main__":
    unittest.main()
