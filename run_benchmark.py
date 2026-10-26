"""Empirical comparison of DHR and XGBoost with sktime's ForecastingBenchmark.

Design (fixed before looking at test results):
- Rolling origin with a fixed-length training window, so the comparison is a
  comparison of forecasting methods in the sense of Giacomini & White (2006).
- Non-overlapping weekly forecast blocks (fh = 1..168 h, step = 168 h).
- Primary hypothesis: equal expected weekly MAE of DHR and the XGBoost seed
  ensemble, two-sided, alpha = 0.05. All other comparisons are exploratory.

Run the validation period for model selection; run the test period once:
    uv run python run_benchmark.py --period validation
    uv run python run_benchmark.py --period test
"""

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sktime.benchmarking.forecasting import ForecastingBenchmark
from sktime.forecasting.compose import EnsembleForecaster
from sktime.forecasting.naive import NaiveForecaster
from sktime.performance_metrics.forecasting import (
    MeanAbsoluteError,
    MeanAbsolutePercentageError,
    MeanAbsoluteScaledError,
    MeanSquaredError,
)
from sktime.split import SlidingWindowSplitter
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf

from common.loader import load_panel
from modeling.dynamic_harmonic_regression import DynamicHarmonicRegressionModel
from modeling.gradient_boosting import GradientBoostingModel

TEST_END = pd.Timestamp("2026-04-01")  # Exclusive; naive UTC.
HORIZON = 168  # Hours: seven days.
TEST_WEEKS = 52
VALIDATION_WEEKS = 13
TRAINING_WEEKS = 104  # Fixed rolling training window.
XGB_SEEDS = (0, 1, 2, 3, 4)
PRIMARY_COMPARISON = ("dhr", "xgb_ensemble")
BASELINE = "snaive_168"
CONFIDENCE = 0.95

RESULTS_DIR = Path(__file__).resolve().parent / "data" / "results"


@dataclass(frozen=True)
class PairedLossTest:
    n_origins: int
    horizon: int
    mean_difference: float
    ci_lower: float
    ci_upper: float
    statistic: float
    p_value: float


def evaluation_period(period: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    """Return [start, end) of the evaluation period in naive UTC."""
    test_start = TEST_END - pd.Timedelta(hours=TEST_WEEKS * HORIZON)

    if period == "test":
        return test_start, TEST_END

    validation_start = test_start - pd.Timedelta(hours=VALIDATION_WEEKS * HORIZON)
    return validation_start, test_start


def load_series(start: pd.Timestamp, end: pd.Timestamp) -> pd.Series:
    """Load the gold load series on a complete hourly grid in naive UTC."""
    y = load_panel(type="gold")["Value"].copy()

    y.index = pd.to_datetime(y.index, utc=True).tz_convert(None)
    y = y.sort_index()

    if y.index.has_duplicates:
        raise ValueError("Duplicate timestamps found.")

    y = y.loc[(y.index >= start) & (y.index < end)].asfreq("h")

    if not np.isfinite(y.to_numpy()).all():
        raise ValueError("Missing hours or invalid load values found.")
    if y.index[0] != start or y.index[-1] != end - pd.Timedelta(hours=1):
        raise ValueError("Data does not cover the requested period.")

    return y


def build_estimators() -> dict[str, object]:
    # Hyperparameters must be chosen on the validation period only.
    estimators = {
        "snaive_168": NaiveForecaster(strategy="last", sp=168),
        "snaive_24": NaiveForecaster(strategy="last", sp=24),
        "dhr": DynamicHarmonicRegressionModel(),
        "xgb_ensemble": EnsembleForecaster(
            forecasters=[
                (f"seed_{seed}", GradientBoostingModel(random_state=seed))
                for seed in XGB_SEEDS
            ],
            aggfunc="mean",
        ),
    }
    for seed in XGB_SEEDS:
        estimators[f"xgb_seed_{seed}"] = GradientBoostingModel(random_state=seed)

    return estimators


def diebold_mariano_test(
    loss_a: np.ndarray,
    loss_b: np.ndarray,
    horizon: int = 1,
    confidence: float = CONFIDENCE,
) -> PairedLossTest:
    """Unconditional Diebold-Mariano / Giacomini-White test of equal loss.

    `loss_a` and `loss_b` hold one loss per forecast origin, in time order.
    `horizon` is the dependence length of the loss differential in origins:
    1 for non-overlapping forecast blocks, which reduces the test to a paired
    t-test. The long-run variance uses horizon - 1 unweighted autocovariances
    as in Diebold & Mariano (1995), which the Harvey, Leybourne & Newbold
    (1997) correction assumes; inference uses t(n - 1).

    A positive mean difference means that B has the lower loss.
    """
    loss_a = np.asarray(loss_a, dtype=float)
    loss_b = np.asarray(loss_b, dtype=float)

    if loss_a.shape != loss_b.shape or loss_a.ndim != 1:
        raise ValueError("Losses must be one-dimensional and of equal length.")

    differential = loss_a - loss_b
    n = len(differential)

    if not np.isfinite(differential).all():
        raise ValueError("Losses must be finite.")
    if not 1 <= horizon < n:
        raise ValueError("Horizon must be at least 1 and smaller than n.")

    mean_difference = float(differential.mean())
    centered = differential - mean_difference
    autocovariances = [
        np.sum(centered[lag:] * centered[: n - lag]) / n for lag in range(horizon)
    ]
    long_run_variance = autocovariances[0] + 2 * sum(autocovariances[1:])

    if long_run_variance <= 0:
        raise ValueError("Non-positive long-run variance of the loss differential.")

    correction = np.sqrt((n + 1 - 2 * horizon + horizon * (horizon - 1) / n) / n)
    standard_error = np.sqrt(long_run_variance / n) / correction
    statistic = mean_difference / standard_error
    critical_value = stats.t.ppf(1 - (1 - confidence) / 2, df=n - 1)

    return PairedLossTest(
        n_origins=n,
        horizon=horizon,
        mean_difference=mean_difference,
        ci_lower=float(mean_difference - critical_value * standard_error),
        ci_upper=float(mean_difference + critical_value * standard_error),
        statistic=float(statistic),
        p_value=float(2 * stats.t.sf(abs(statistic), df=n - 1)),
    )


def differential_diagnostics(differential: np.ndarray, lags: int = 4) -> dict[str, float]:
    """Autocorrelations and Ljung-Box p-value of a loss differential."""
    autocorrelations = acf(differential, nlags=lags, fft=False)
    ljung_box = acorr_ljungbox(differential, lags=[lags])

    diagnostics = {
        f"acf_lag_{lag}": float(autocorrelations[lag]) for lag in range(1, lags + 1)
    }
    diagnostics["ljung_box_p_value"] = float(ljung_box["lb_pvalue"].iloc[0])

    return diagnostics


def forecasts_from_benchmark(results: pd.DataFrame) -> pd.DataFrame:
    """Reshape `ForecastingBenchmark(return_data=True)` output to long format."""
    folds = sorted(
        int(column.removeprefix("predictions_fold_"))
        for column in results.columns
        if column.startswith("predictions_fold_")
    )
    frames = []

    for _, row in results.iterrows():
        for fold in folds:
            y_pred = row[f"predictions_fold_{fold}"]
            y_true = row[f"ground_truth_fold_{fold}"]

            if not y_pred.index.equals(y_true.index):
                raise ValueError("Predictions and ground truth are not aligned.")

            frames.append(
                pd.DataFrame(
                    {
                        "model_id": row["model_id"],
                        "fold": fold,
                        "origin": y_true.index[0] - pd.Timedelta(hours=1),
                        "horizon": np.arange(1, len(y_true) + 1),
                        "timestamp": y_true.index,
                        "y_true": y_true.to_numpy(dtype=float),
                        "y_pred": y_pred.to_numpy(dtype=float),
                    }
                )
            )

    forecasts = pd.concat(frames, ignore_index=True)
    error = forecasts["y_true"] - forecasts["y_pred"]

    return forecasts.assign(
        abs_error=error.abs(),
        squared_error=error**2,
        abs_percentage_error=(error / forecasts["y_true"]).abs() * 100,
    )


def accuracy_summary(forecasts: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    """Pooled MAE, RMSE, MAPE (%) and mean MASE per model."""
    grouped = forecasts.groupby("model_id")
    mase = results.set_index("model_id")["MeanAbsoluteScaledError_mean"]
    fit_time = results.set_index("model_id")["fit_time_mean"]

    summary = pd.DataFrame(
        {
            "MAE": grouped["abs_error"].mean(),
            "RMSE": np.sqrt(grouped["squared_error"].mean()),
            "MAPE": grouped["abs_percentage_error"].mean(),
            "MASE_168": mase,
            "fit_time_s": fit_time,
        }
    )
    summary[f"MAE_skill_vs_{BASELINE}"] = 1 - summary["MAE"] / summary.loc[BASELINE, "MAE"]

    return summary.sort_values("MAE")


def compare(
    origin_mae: pd.DataFrame,
    model_a: str,
    model_b: str,
    role: str,
) -> dict[str, object]:
    differential = (origin_mae[model_a] - origin_mae[model_b]).to_numpy()
    test = diebold_mariano_test(origin_mae[model_a], origin_mae[model_b])

    return {
        "role": role,
        "model_a": model_a,
        "model_b": model_b,
        **asdict(test),
        "relative_difference": test.mean_difference / origin_mae[model_a].mean(),
        "weeks_b_better": int((differential > 0).sum()),
        **differential_diagnostics(differential),
    }


def git_state() -> dict[str, object]:
    def run(*args: str) -> str:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, check=False
        ).stdout.strip()

    return {"commit": run("rev-parse", "HEAD"), "dirty": bool(run("status", "--porcelain"))}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--period", choices=["validation", "test"], default="validation")
    args = parser.parse_args()

    start, end = evaluation_period(args.period)
    window = TRAINING_WEEKS * HORIZON
    y = load_series(start - pd.Timedelta(hours=window), end)

    cv = SlidingWindowSplitter(
        window_length=window,
        fh=np.arange(1, HORIZON + 1),
        step_length=HORIZON,
    )

    benchmark = ForecastingBenchmark(return_data=True)
    for estimator_id, estimator in build_estimators().items():
        benchmark.add_estimator(estimator, estimator_id=estimator_id)

    benchmark.add_task(
        dataset_loader=lambda: y,
        cv_splitter=cv,
        scorers=[
            MeanAbsoluteError(),
            MeanSquaredError(square_root=True),
            MeanAbsolutePercentageError(),
            MeanAbsoluteScaledError(sp=168),
        ],
        task_id=f"de_load_{args.period}_h{HORIZON}",
        strategy="refit",
        error_score="raise",
    )
    results = benchmark.run()

    forecasts = forecasts_from_benchmark(results)
    origins = forecasts["origin"].drop_duplicates()
    expected_weeks = TEST_WEEKS if args.period == "test" else VALIDATION_WEEKS

    if len(origins) != expected_weeks or forecasts["timestamp"].min() != start:
        raise ValueError("Folds do not match the evaluation period.")

    origin_mae = forecasts.pivot_table(
        index="origin", columns="model_id", values="abs_error", aggfunc="mean"
    )
    horizon_mae = forecasts.pivot_table(
        index="horizon", columns="model_id", values="abs_error", aggfunc="mean"
    )
    summary = accuracy_summary(forecasts, results)

    comparisons = [compare(origin_mae, *PRIMARY_COMPARISON, role="primary")]
    for model_id in ["dhr", "xgb_ensemble", "snaive_24"]:
        comparisons.append(compare(origin_mae, BASELINE, model_id, role="exploratory"))
    for seed in XGB_SEEDS:
        comparisons.append(
            compare(origin_mae, "dhr", f"xgb_seed_{seed}", role="exploratory")
        )
    tests = pd.DataFrame(comparisons)

    output_dir = RESULTS_DIR / f"benchmark_{args.period}"
    output_dir.mkdir(parents=True, exist_ok=True)

    data_columns = [
        column
        for column in results.columns
        if column.startswith(("predictions_", "ground_truth_", "train_data_"))
    ]
    results.drop(columns=data_columns).to_csv(output_dir / "scores.csv", index=False)
    forecasts.to_csv(output_dir / "forecasts.csv", index=False)
    origin_mae.to_csv(output_dir / "origin_mae.csv")
    horizon_mae.to_csv(output_dir / "horizon_mae.csv")
    summary.to_csv(output_dir / "summary.csv")
    tests.to_csv(output_dir / "tests.csv", index=False)

    metadata = {
        "period": args.period,
        "evaluation_start": str(start),
        "evaluation_end_exclusive": str(end),
        "training_window_hours": window,
        "horizon_hours": HORIZON,
        "n_origins": len(origins),
        "xgb_seeds": list(XGB_SEEDS),
        "primary_comparison": list(PRIMARY_COMPARISON),
        "confidence": CONFIDENCE,
        "estimators": {
            estimator_id: repr(estimator)
            for estimator_id, estimator in build_estimators().items()
        },
        "git": git_state(),
        "versions": {
            package: version(package)
            for package in ["sktime", "xgboost", "statsmodels", "pandas", "numpy", "scipy"]
        },
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))

    primary = tests.iloc[0]
    with pd.option_context("display.width", 140, "display.precision", 3):
        print(f"Period: {args.period} [{start}, {end}), {len(origins)} weekly origins")
        print(f"Training window: {TRAINING_WEEKS} weeks, horizon: {HORIZON} h\n")
        print(summary, "\n")
        print(f"Primary test: weekly MAE {primary.model_a} - {primary.model_b}")
        print(
            f"  mean difference {primary.mean_difference:.3f} "
            f"({primary.relative_difference:+.2%}), "
            f"{CONFIDENCE:.0%} CI [{primary.ci_lower:.3f}, {primary.ci_upper:.3f}]"
        )
        print(f"  t = {primary.statistic:.3f}, p = {primary.p_value:.4f}")
        print(
            f"  {primary.model_b} better in {primary.weeks_b_better}/"
            f"{primary.n_origins} weeks; ACF lag 1 = {primary.acf_lag_1:.3f}, "
            f"Ljung-Box p = {primary.ljung_box_p_value:.3f}"
        )
        print(f"\nResults written to {output_dir}")


if __name__ == "__main__":
    main()
