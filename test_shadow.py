from datetime import datetime, timedelta, timezone
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from market_lab.shadow import closed_history, record_intention
from test_market import data, START


class ShadowTests(unittest.TestCase):
    def test_duplicate_intention_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"log.sqlite"
            self.assertEqual(record_intention(path,"one",{"weight":.4},"2025-02-02"),"recorded")
            self.assertEqual(record_intention(path,"one",{"weight":.4},"2025-02-03"),"duplicate")
            with closing(sqlite3.connect(path)) as db:
                self.assertEqual(db.execute("SELECT COUNT(*) FROM intentions").fetchone()[0],1)
                self.assertEqual(db.execute("SELECT observed_at FROM intentions").fetchone()[0],"2025-02-02")

    def test_conflict_and_nan_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"log.sqlite"
            record_intention(path,"one",{"weight":.4},"t")
            with self.assertRaises(ValueError):
                record_intention(path,"one",{"weight":.5},"t2")
            with self.assertRaises(ValueError):
                record_intention(path,"two",{"weight":float("nan")},"t2")

    def test_forming_bar_is_excluded_and_unavailable_close_waits(self):
        rows=data(40)
        now=START+timedelta(days=39,hours=12)
        _,bars,_=closed_history(rows,now,"BTCUSDT")
        self.assertEqual(len(bars),39)
        now=START+timedelta(days=39)
        _,bars,_=closed_history(rows,now,"BTCUSDT")
        self.assertEqual(len(bars),38)

    def test_stale_or_short_feed_rejected(self):
        with self.assertRaises(ValueError):
            closed_history(data(40),START+timedelta(days=45),"BTCUSDT")
        with self.assertRaises(ValueError):
            closed_history(data(20),START+timedelta(days=20,hours=1),"BTCUSDT")


if __name__=="__main__":
    unittest.main()
