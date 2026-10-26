import numpy as np
import pandas as pd
from sktime.forecasting.model_evaluation import evaluate
from sktime.performance_metrics.forecasting import (
    MeanAbsoluteError,
    MeanSquaredError,
)
from sktime.split import ExpandingWindowSplitter

from common.loader import load_panel
from modeling.gradient_boosting import GradientBoostingModel

TEST_START = pd.Timestamp("2026-01-01")
TEST_END = pd.Timestamp("2026-04-01")  # Exclusive.
HORIZON = 168  # Hours: seven days.


def main() -> None:
    panel = load_panel(type="gold")
    y = panel["Value"].copy()

    y.index = pd.to_datetime(y.index, utc=True).tz_convert(None)
    y = y.sort_index()

    if y.index.has_duplicates:
        raise ValueError("Duplicate timestamps found.")

    y = y.loc[y.index < TEST_END].asfreq("h")

    if not np.isfinite(y.to_numpy()).all():
        raise ValueError("Missing hours or invalid load values found.")

    expected_test_index = pd.date_range(
        TEST_START,
        TEST_END,
        freq="h",
        inclusive="left",
        name=y.index.name,
    )
    if not y.loc[y.index >= TEST_START].index.equals(expected_test_index):
        raise ValueError("The complete evaluation period is required.")

    initial_window = int((y.index < TEST_START).sum())
    if initial_window < 8 * 24:
        raise ValueError("At least eight days of training history are required.")

    cv = ExpandingWindowSplitter(
        initial_window=initial_window,
        fh=np.arange(1, HORIZON + 1),
        step_length=HORIZON,
    )

    results = evaluate(
        forecaster=GradientBoostingModel(),
        y=y,
        cv=cv,
        strategy="refit",
        scoring=[
            MeanAbsoluteError(),
            MeanSquaredError(),
        ],
        return_data=True,
        error_score="raise",
    )

    # Each fold contains HORIZON hours, so folds have equal weight.
    mae = results["test_MeanAbsoluteError"].mean()
    rmse = np.sqrt(results["test_MeanSquaredError"].mean())

    evaluated_hours = len(results) * HORIZON

    print(f"Forecast horizon: {HORIZON} hours")
    print(f"Evaluated forecast blocks: {len(results)}")
    print(f"Evaluated hours: {evaluated_hours}")
    print(f"Evaluated days: {evaluated_hours / 24:.1f}")
    print(f"MAE:  {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")


if __name__ == "__main__":
    main()
