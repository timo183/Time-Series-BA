from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
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

from config import DATA_SPLIT
from ingestion import LoadPanel
from modeling.dynamic_harmonic_regression import DynamicHarmonicRegressionModel
from modeling.gradient_boosting import GradientBoostingModel

HORIZON = 168  # Hours: seven days.
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
    """Return [start, end) of the evaluation period in naive UTC (see config)."""
    periods = DATA_SPLIT.periods()
    if period not in ("validation", "test"):
        raise ValueError(f"Unknown evaluation period: {period!r}")
    start, end = periods[period]
    return (
        pd.Timestamp(start).tz_convert(None),
        pd.Timestamp(end).tz_convert(None),
    )


def load_series(start: pd.Timestamp, end: pd.Timestamp) -> pd.Series:
    """Load the cleaned load series on a complete hourly grid in naive UTC."""
    return LoadPanel().series(start, end)


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


def main() -> None:

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


if __name__ == "__main__":
    main()
