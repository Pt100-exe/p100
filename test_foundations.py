import copy
import json
import math
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from p100_foundations.features import Observation, trailing_return
from p100_foundations.freeze import build_manifest, verify_manifest, write_manifest
from p100_foundations.regimes import Regime, RegimeConfig, Trend, Volatility, classify_regime
from p100_foundations.registry import BURNED_WINDOW, EvaluationWindow, candidate_holdout_status
from p100_foundations.risk import RiskPolicy, size_exposure
from p100_foundations.strategy import ExposureIntent, StrategyConfig, propose_exposure
from p100_foundations.temporal import LabeledWindow, purged_split


def day(number):
    return datetime(2024, 1, 1, tzinfo=timezone.utc) + timedelta(days=number)


class FeatureTests(unittest.TestCase):
    def setUp(self):
        self.rows = [Observation(day(i), day(i), price) for i, price in enumerate([100.0, 110.0, 121.0, 130.0])]

    def test_exact_trailing_return(self):
        self.assertAlmostEqual(trailing_return(self.rows, day(2), 2), 0.21)

    def test_future_price_changes_do_not_change_past_feature(self):
        before = trailing_return(self.rows, day(2), 2)
        for future in (1e-20, 1e100, math.nan, math.inf):
            rows = self.rows[:3] + [Observation(day(3), day(3), future)]
            with self.subTest(future=future):
                self.assertEqual(trailing_return(rows, day(2), 2), before)

    def test_delayed_observation_excluded_until_available(self):
        delayed = [Observation(day(0), day(0), 100), Observation(day(1), day(3), 900), Observation(day(2), day(2), 110)]
        self.assertAlmostEqual(trailing_return(delayed, day(2), 1), 0.1)
        self.assertAlmostEqual(trailing_return(delayed, day(3), 1), 110 / 900 - 1)

    def test_nonfinite_or_nonpositive_available_prices_rejected(self):
        for bad in (math.nan, math.inf, -math.inf, 0, -1, True, "100"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                trailing_return([self.rows[0], Observation(day(1), day(1), bad)], day(1), 1)

    def test_duplicate_available_events_rejected(self):
        with self.assertRaises(ValueError):
            trailing_return(self.rows + [self.rows[0]], day(2), 2)

    def test_insufficient_history_and_bad_lookback(self):
        with self.assertRaises(ValueError):
            trailing_return(self.rows, day(0), 1)
        for lookback in (0, -1, True, 1.5):
            with self.subTest(lookback=lookback), self.assertRaises(ValueError):
                trailing_return(self.rows, day(2), lookback)

    def test_naive_time_and_impossible_availability_rejected(self):
        with self.assertRaises(ValueError):
            trailing_return(self.rows, datetime(2024, 1, 3), 1)
        with self.assertRaises(ValueError):
            trailing_return([Observation(day(1), day(0), 100)], day(2), 1)

    def test_overflow_return_rejected(self):
        with self.assertRaises(ValueError):
            trailing_return([Observation(day(0), day(0), 1e-300), Observation(day(1), day(1), 1e300)], day(1), 1)


class RegimeTests(unittest.TestCase):
    def test_all_nine_axis_combinations_remain_distinct(self):
        results = set()
        for score, trend in ((0.10, Trend.UP), (-0.10, Trend.DOWN), (0.0, Trend.FLAT)):
            for vol, regime_vol in ((0.10, Volatility.LOW), (0.40, Volatility.NORMAL), (0.80, Volatility.HIGH)):
                with self.subTest(trend=trend, vol=vol):
                    actual = classify_regime(score, vol)
                    self.assertEqual(actual, Regime(trend, regime_vol))
                    results.add(actual)
        self.assertEqual(len(results), 9)

    def test_threshold_equalities_are_flat_and_normal(self):
        self.assertEqual(classify_regime(0.02, 0.2), Regime(Trend.FLAT, Volatility.NORMAL))
        self.assertEqual(classify_regime(-0.02, 0.6), Regime(Trend.FLAT, Volatility.NORMAL))

    def test_nonfinite_signals_and_invalid_thresholds_rejected(self):
        for bad in (math.nan, math.inf, -math.inf, True):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    classify_regime(bad, 0.3)
                with self.assertRaises(ValueError):
                    classify_regime(0.1, bad)
                with self.assertRaises(ValueError):
                    RegimeConfig(trend_threshold=bad)
        for config in ({"low_vol": 0.6}, {"high_vol": 0.1}, {"trend_threshold": -0.1}):
            with self.subTest(config=config), self.assertRaises(ValueError):
                RegimeConfig(**config)
        with self.assertRaises(ValueError):
            classify_regime(0.1, -0.01)


class StrategyRiskTests(unittest.TestCase):
    def test_up_and_high_vol_retains_trend_intent_then_caps_risk_once(self):
        regime = classify_regime(0.10, 0.80)
        intent = propose_exposure(regime, confidence=0.70)
        self.assertEqual(regime, Regime(Trend.UP, Volatility.HIGH))
        self.assertAlmostEqual(intent.core + intent.tactical, 0.7)
        decision = size_exposure(intent, 0.80)
        self.assertTrue(decision.allowed)
        self.assertAlmostEqual(decision.target_exposure, 0.25)
        self.assertAlmostEqual(decision.risk_cap, 0.25)

    def test_direction_changes_overlay_even_under_high_vol(self):
        up = propose_exposure(classify_regime(0.1, 0.8))
        down = propose_exposure(classify_regime(-0.1, 0.8))
        self.assertGreater(up.tactical, 0)
        self.assertLess(down.tactical, 0)
        self.assertAlmostEqual(size_exposure(down, 0.8).target_exposure, 0.1)

    def test_volatility_axis_does_not_apply_second_strategy_discount(self):
        low = propose_exposure(classify_regime(0.1, 0.1))
        high = propose_exposure(classify_regime(0.1, 0.8))
        self.assertEqual(low, high)

    def test_low_confidence_blocks_positive_overlay_keeps_explicit_core(self):
        decision = size_exposure(ExposureIntent(0.4, 0.3, 0.49), 0.1)
        self.assertAlmostEqual(decision.target_exposure, 0.4)
        self.assertEqual(decision.reason, "core_only_low_confidence")
        self.assertAlmostEqual(size_exposure(ExposureIntent(0.4, 0.3, 0.5), 0.1).target_exposure, 0.7)

    def test_low_confidence_does_not_prevent_negative_risk_reducing_overlay(self):
        decision = size_exposure(ExposureIntent(0.4, -0.3, 0.01), 0.1)
        self.assertAlmostEqual(decision.target_exposure, 0.1)

    def test_no_short_no_leverage_and_explicit_exposure_cap(self):
        cases = [
            (ExposureIntent(0.9, 0.9), 0.1, RiskPolicy(), 1.0),
            (ExposureIntent(0.1, -0.9), 0.1, RiskPolicy(), 0.0),
            (ExposureIntent(0.9, 0.9), 0.1, RiskPolicy(max_exposure=0.6), 0.6),
            (ExposureIntent(0.4, 0.3), 0.1, RiskPolicy(max_exposure=0), 0.0),
            (ExposureIntent(0.4, 0.3), 5e-324, RiskPolicy(), 0.7),
        ]
        for intent, vol, policy, expected in cases:
            with self.subTest(expected=expected):
                decision = size_exposure(intent, vol, policy)
                self.assertTrue(math.isfinite(decision.target_exposure))
                self.assertAlmostEqual(decision.target_exposure, expected)

    def test_budget_invariant_for_parameter_grid(self):
        cases = 0
        for core in (0, 0.4, 1):
            for tactical in (-1, -0.3, 0, 0.3, 1):
                for confidence in (0, 0.49, 0.5, 1):
                    for vol in (0.01, 0.2, 0.8, 3):
                        for maximum in (0, 0.5, 1):
                            policy = RiskPolicy(max_exposure=maximum)
                            decision = size_exposure(ExposureIntent(core, tactical, confidence), vol, policy)
                            self.assertTrue(decision.allowed)
                            self.assertGreaterEqual(decision.target_exposure, 0)
                            self.assertLessEqual(decision.target_exposure, maximum)
                            self.assertLessEqual(decision.target_exposure * vol, policy.target_annual_vol + 1e-14)
                            cases += 1
        self.assertEqual(cases, 720)

    def test_runtime_invalid_inputs_fail_closed_in_all_fields(self):
        for bad in (math.nan, math.inf, -math.inf, True, "0.4", None):
            for field in ("core", "tactical", "confidence", "forecast_annual_vol"):
                with self.subTest(field=field, bad=bad):
                    values = {"core": 0.4, "tactical": 0.3, "confidence": 0.8, "forecast_annual_vol": 0.3}
                    values[field] = bad
                    vol = values.pop("forecast_annual_vol")
                    decision = size_exposure(ExposureIntent(**values), vol)
                    self.assertFalse(decision.allowed)
                    self.assertEqual(decision.target_exposure, 0)

    def test_invalid_ranges_and_halt_fail_closed(self):
        for intent, vol in ((ExposureIntent(-0.1, 0), 0.3), (ExposureIntent(1.1, 0), 0.3), (ExposureIntent(0.4, 1.1), 0.3), (ExposureIntent(0.4, 0, 1.1), 0.3), (ExposureIntent(0.4, 0), 0), (ExposureIntent(0.4, 0), -0.1)):
            self.assertFalse(size_exposure(intent, vol).allowed)
        self.assertEqual(size_exposure(ExposureIntent(0.4, 0.3), 0.3, halted=True).reason, "halted")
        self.assertFalse(size_exposure(ExposureIntent(0.4, 0.3), 0.3, halted="false").allowed)
        self.assertFalse(size_exposure(None, 0.3).allowed)

    def test_bad_policies_and_strategy_configs_rejected(self):
        for field in ("target_annual_vol", "max_exposure", "min_tactical_confidence"):
            for bad in (math.nan, math.inf, -1):
                with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                    RiskPolicy(**{field: bad})
        for field in ("core", "tactical_up", "tactical_down", "tactical_flat"):
            for bad in (math.nan, math.inf, 2):
                with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                    StrategyConfig(**{field: bad})

    def test_strategy_rejects_invalid_confidence_and_regime(self):
        for bad in (math.nan, math.inf, -0.1, 1.1):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                propose_exposure(classify_regime(0.1, 0.3), bad)
        with self.assertRaises(ValueError):
            propose_exposure(Regime("UP", "HIGH"))

    def test_future_perturbation_invariance_feature_regime_strategy_and_risk(self):
        history = [Observation(day(i), day(i), price) for i, price in enumerate((100, 99, 104, 106, 98, 95))]
        def run(rows, cutoff):
            feature = trailing_return(rows, cutoff, 2)
            # Volatilidad suministrada como constante de fixture, no estimador aprendido.
            regime = classify_regime(feature, 0.8)
            intent = propose_exposure(regime, 0.7)
            decision = size_exposure(intent, 0.8)
            return feature, regime, intent, decision
        for cutoff_day in (2, 3, 4):
            for future_price in (0.01, 1e6, math.nan):
                changed = [row if row.event_time <= day(cutoff_day) else Observation(row.event_time, row.available_at, future_price) for row in history]
                with self.subTest(cutoff=cutoff_day, future=future_price):
                    self.assertEqual(run(history, day(cutoff_day)), run(changed, day(cutoff_day)))

    def test_delayed_price_perturbation_is_invisible_to_all_downstream_components(self):
        def run(delayed_price):
            rows = [Observation(day(0), day(0), 100), Observation(day(1), day(5), delayed_price), Observation(day(2), day(2), 110)]
            feature = trailing_return(rows, day(2), 1)
            regime = classify_regime(feature, 0.8)
            intent = propose_exposure(regime)
            return feature, regime, intent, size_exposure(intent, 0.8)
        self.assertEqual(run(1), run(100000))

    def test_example_config_is_executable_and_changes_behavior(self):
        config = json.loads((Path(__file__).resolve().parents[1] / "config" / "example.json").read_text(encoding="utf-8"))
        regime = classify_regime(0.1, 0.8, RegimeConfig(**config["regime"]))
        intent = propose_exposure(regime, 0.8, StrategyConfig(**config["strategy"]))
        decision = size_exposure(intent, 0.8, RiskPolicy(**config["risk"]))
        self.assertAlmostEqual(decision.target_exposure, 0.25)
        changed = copy.deepcopy(config)
        changed["risk"]["target_annual_vol"] = 0.08
        self.assertAlmostEqual(size_exposure(intent, 0.8, RiskPolicy(**changed["risk"])).target_exposure, 0.1)


class TemporalTests(unittest.TestCase):
    def test_purges_horizons_touching_or_crossing_validation(self):
        rows = [LabeledWindow(day(i), day(i + 2)) for i in range(10)]
        split = purged_split(rows, day(5), day(10))
        self.assertEqual(split.train, (0, 1, 2))
        self.assertEqual(split.validation, (5, 6, 7))
        self.assertEqual(split.excluded, (3, 4, 8, 9))
        self.assertTrue(all(rows[i].label_end < day(5) for i in split.train))
        self.assertTrue(all(rows[i].label_end < day(10) for i in split.validation))

    def test_pre_validation_gap_further_purges_training(self):
        rows = [LabeledWindow(day(i), day(i + 1)) for i in range(10)]
        split = purged_split(rows, day(5), day(10), pre_validation_gap=timedelta(days=2))
        self.assertEqual(split.train, (0, 1))

    def test_appending_future_rows_does_not_change_selected_fold(self):
        rows = [LabeledWindow(day(i), day(i + 1)) for i in range(10)]
        first = purged_split(rows, day(5), day(10))
        extended = purged_split(rows + [LabeledWindow(day(i), day(i + 50)) for i in range(10, 15)], day(5), day(10))
        self.assertEqual(first.train, extended.train)
        self.assertEqual(first.validation, extended.validation)

    def test_bad_times_order_duplicates_and_horizon_rejected(self):
        cases = [
            [LabeledWindow(day(2), day(1))],
            [LabeledWindow(day(2), day(3)), LabeledWindow(day(1), day(2))],
            [LabeledWindow(day(1), day(2)), LabeledWindow(day(1), day(3))],
            [LabeledWindow(datetime(2024, 1, 1), day(1))],
        ]
        for rows in cases:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                purged_split(rows, day(5), day(10))
        with self.assertRaises(ValueError):
            purged_split([], day(5), day(5))
        with self.assertRaises(ValueError):
            purged_split([], day(5), day(10), pre_validation_gap=timedelta(days=-1))

    def test_timezone_equivalence_and_partition_completeness(self):
        rows = [LabeledWindow(day(i), day(i + 1)) for i in range(10)]
        zone = timezone(timedelta(hours=-6))
        split = purged_split(rows, day(5).astimezone(zone), day(10).astimezone(zone))
        self.assertEqual(split, purged_split(rows, day(5), day(10)))
        self.assertEqual(sorted(split.train + split.validation + split.excluded), list(range(10)))


class RegistryFreezeTests(unittest.TestCase):
    def test_burned_dates_and_overlap_enforced(self):
        self.assertEqual(BURNED_WINDOW.start.isoformat(), "2024-09-01T00:00:00+00:00")
        self.assertEqual(BURNED_WINDOW.end.isoformat(), "2024-11-09T00:00:00+00:00")
        for start, end in ((BURNED_WINDOW.start, BURNED_WINDOW.end), (BURNED_WINDOW.start - timedelta(days=1), BURNED_WINDOW.start + timedelta(seconds=1)), (BURNED_WINDOW.end - timedelta(seconds=1), BURNED_WINDOW.end + timedelta(days=1))):
            with self.subTest(start=start), self.assertRaises(ValueError):
                candidate_holdout_status(EvaluationWindow(start, end))

    def test_nonoverlap_never_certifies_unseen_data(self):
        self.assertEqual(candidate_holdout_status(None), "NOT_SELECTED")
        later = EvaluationWindow(BURNED_WINDOW.end, BURNED_WINDOW.end + timedelta(days=10))
        earlier = EvaluationWindow(BURNED_WINDOW.start - timedelta(days=10), BURNED_WINDOW.start)
        for candidate in (later, earlier):
            self.assertEqual(candidate_holdout_status(candidate), "CANDIDATE_NOT_VERIFIED_UNSEEN")

    def test_invalid_registry_window_rejected(self):
        with self.assertRaises(ValueError):
            EvaluationWindow(day(1), day(1))
        with self.assertRaises(ValueError):
            EvaluationWindow(datetime(2024, 1, 1), day(2))

    def test_hashes_deterministic_and_detect_code_data_and_config_changes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "code.py").write_text("answer = 1\n", encoding="utf-8")
            (root / "fixture.csv").write_text("synthetic_test_only\n1\n", encoding="utf-8")
            manifest = build_manifest(root, ["code.py"], ["fixture.csv"], {"a": 1, "b": 2})
            self.assertEqual(manifest, build_manifest(root, ["code.py"], ["fixture.csv"], {"b": 2, "a": 1}))
            self.assertEqual(verify_manifest(root, manifest), [])
            (root / "code.py").write_text("answer = 2\n", encoding="utf-8")
            self.assertIn("code_files_mismatch", verify_manifest(root, manifest))
            (root / "fixture.csv").write_text("synthetic_test_only\n2\n", encoding="utf-8")
            self.assertIn("data_files_mismatch", verify_manifest(root, manifest))
            changed = copy.deepcopy(manifest)
            changed["config"]["a"] = 3
            self.assertIn("config_digest_mismatch", verify_manifest(root, changed))
            self.assertIn("manifest_digest_mismatch", verify_manifest(root, changed))

    def test_missing_data_remains_explicit_and_existing_freeze_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "code.py").write_text("pass\n", encoding="utf-8")
            manifest = build_manifest(root, ["code.py"], [], {})
            self.assertEqual(manifest["data_status"], "NO_MARKET_DATA_PROVIDED")
            self.assertEqual(manifest["holdout_status"], "NOT_SELECTED")
            self.assertEqual(manifest["data"], [])
            destination = root / "freeze.json"
            write_manifest(destination, manifest)
            with self.assertRaises(FileExistsError):
                write_manifest(destination, manifest)

    def test_freeze_rejects_burned_candidate_and_nonfinite_config(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "code.py").write_text("pass\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                build_manifest(root, ["code.py"], [], {}, candidate_holdout=BURNED_WINDOW)
            with self.assertRaises(ValueError):
                build_manifest(root, ["code.py"], [], {"threshold": math.nan})

    def test_paths_cannot_escape_root_and_duplicates_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            root = outer / "project"
            root.mkdir()
            (outer / "outside.py").write_text("pass\n", encoding="utf-8")
            (root / "inside.py").write_text("pass\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                build_manifest(root, ["../outside.py"], [], {})
            with self.assertRaises(ValueError):
                build_manifest(root, ["inside.py", "./inside.py"], [], {})
            with self.assertRaises(ValueError):
                build_manifest(root, [], [], {})

    def test_missing_file_verification_reports_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "code.py").write_text("pass\n", encoding="utf-8")
            manifest = build_manifest(root, ["code.py"], [], {})
            (root / "code.py").unlink()
            self.assertTrue(verify_manifest(root, manifest))


if __name__ == "__main__":
    unittest.main()
