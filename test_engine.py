from dataclasses import replace
from datetime import datetime, timedelta, timezone
import math
import unittest

from p100_lab.engine import Bar, Costs, rebalance, run
from p100_lab.signals import MODES, make_signal


def bars(prices):
    start = datetime(2000, 1, 1, tzinfo=timezone.utc)
    return [Bar(start + timedelta(days=i), start + timedelta(days=i, seconds=86399),
                start + timedelta(days=i, seconds=86399), p, p) for i, p in enumerate(prices)]


class ExecutionTests(unittest.TestCase):
    def test_buy_with_costs_hand_calculation(self):
        f = rebalance(10000, 0, 100, 1, Costs(100, 50))
        self.assertAlmostEqual(f.units, 10000 / (100.5 * 1.01))
        self.assertAlmostEqual(f.cash, 0)
        self.assertAlmostEqual(f.fee, f.units * 100.5 * 0.01)

    def test_sell_with_costs_hand_calculation(self):
        f = rebalance(0, 100, 100, 0, Costs(100, 50))
        self.assertAlmostEqual(f.cash, 100 * 99.5 * 0.99)
        self.assertEqual(f.units, 0)

    def test_grid_reconciles_and_hits_post_cost_target(self):
        for cash in (0, 17, 10000):
            for units in (0, 1, 55):
                for price in (0.01, 100, 100000):
                    for target in (0, .1, .4, .7, 1):
                        for fee, slip in ((0, 0), (10, 5), (30, 5), (100, 50)):
                            with self.subTest(cash=cash, units=units, price=price, target=target, fee=fee):
                                f = rebalance(cash, units, price, target, Costs(fee, slip))
                                self.assertGreaterEqual(f.cash, 0)
                                self.assertGreaterEqual(f.units, 0)
                                self.assertAlmostEqual(f.equity_after, f.equity_before - f.fee - f.slippage, delta=max(1, f.equity_before)*1e-9)
                                if f.equity_after:
                                    self.assertAlmostEqual(f.units * price / f.equity_after, target)

    def test_next_open_not_signal_close(self):
        data = bars([100, 200, 400])
        result = run(data, lambda h: 1.0, Costs(0, 0))
        self.assertEqual(result["rows"][0]["units"], 0)
        self.assertEqual(result["fills"][0]["price"], 200)
        self.assertEqual(result["metrics"]["ending_equity"], 20000)
        self.assertEqual(result["metrics"]["pending_unfilled"], 1)

    def test_open_gap_belongs_to_existing_position(self):
        data = bars([100, 100, 200])
        result = run(data, lambda h: 1.0 if len(h) == 1 else 0.0, Costs(0, 0))
        self.assertEqual(result["metrics"]["ending_equity"], 20000)
        self.assertEqual(result["rows"][-1]["units"], 0)

    def test_cash_baseline_and_first_loss_drawdown(self):
        data = bars([100, 100])
        cash = run(data, lambda h: 0.0)
        long = run(data, lambda h: 1.0)
        self.assertEqual(cash["metrics"]["ending_equity"], 10000)
        self.assertLess(long["metrics"]["max_drawdown"], 0)

    def test_no_terminal_forced_trade(self):
        result = run(bars([100]), lambda h: 1.0)
        self.assertEqual(result["fills"], [])
        self.assertEqual(result["metrics"]["pending_unfilled"], 1)

    def test_delayed_and_duplicate_bars_rejected(self):
        data = bars([100, 101])
        with self.assertRaises(ValueError):
            run([data[0], data[0]], lambda h: 0)
        with self.assertRaises(ValueError):
            run([replace(data[0], available_at=data[1].open_time), data[1]], lambda h: 0)

    def test_invalid_inputs_rejected(self):
        for p in (0, -1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                run(bars([p]), lambda h: 0)
        for weight in (-1, 2, math.nan, math.inf, True):
            with self.assertRaises(ValueError):
                run(bars([100]), lambda h: weight)
        for fee in (-1, 10000, math.nan, True):
            with self.assertRaises(ValueError):
                Costs(fee, 0)

    def test_all_policies_prefix_and_future_invariance(self):
        data = bars([100 * math.exp(.002*i + .025*math.sin(i)) for i in range(80)])
        cut = 55
        changed = data[:cut] + [replace(b, open=b.open*7, close=b.close*.2) for b in data[cut:]]
        for mode in MODES:
            with self.subTest(mode=mode):
                original = run(data, make_signal(mode))
                short = run(data[:cut], make_signal(mode))
                altered = run(changed, make_signal(mode))
                self.assertEqual(original["rows"][:cut], short["rows"])
                self.assertEqual(original["rows"][:cut], altered["rows"][:cut])
                self.assertEqual([f for f in original["fills"] if f["index"] < cut], short["fills"])

    def test_negative_control_catches_future_leak(self):
        data = bars([100.0] * 80)
        cut = 55
        altered = data[:cut] + [replace(b, close=200) for b in data[cut:]]
        def contaminated(full):
            def signal(history):
                i = len(history) - 1
                return float(full[min(i+1, len(full)-1)].close > history[-1].close)
            return signal
        a = run(data, contaminated(data))
        b = run(altered, contaminated(altered))
        # Deliberately leaking callback has a reference outside its causal prefix.
        self.assertNotEqual(a["rows"][:cut], b["rows"][:cut])
        self.assertNotEqual(a["rows"][cut-1]["next_target"], b["rows"][cut-1]["next_target"])

    def test_constant_prices_charge_only_actual_rebalances(self):
        result = run(bars([100] * 100), lambda h: 1.0)
        self.assertEqual(result["metrics"]["trades"], 1)
        self.assertAlmostEqual(result["metrics"]["fees"], result["fills"][0]["fee"])

    def test_warmup_equal_for_all_policies(self):
        data = bars([100] * 40)
        for mode in MODES:
            r = run(data, make_signal(mode))
            self.assertEqual(r["fills"][0]["index"], 31)
            self.assertTrue(all(x["next_target"] is None for x in r["rows"][:30]))

    def test_single_roundtrip_flat_prices_closed_form(self):
        result = run(bars([100]*3), lambda h: 1.0 if len(h)==1 else 0.0, Costs(10, 5))
        expected = 10000 * (1-.0005)*(1-.001)/((1+.0005)*(1+.001))
        self.assertAlmostEqual(result["metrics"]["ending_equity"], expected)


if __name__ == "__main__":
    unittest.main()
