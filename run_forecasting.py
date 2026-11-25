import numpy as np
import pandas as pd
from sktime.forecasting.model_evaluation import evaluate
from sktime.performance_metrics.forecasting import (
    MeanAbsoluteError,
    MeanSquaredError,
)
from sktime.split import ExpandingWindowSplitter

from config import DATA_SPLIT
from ingestion import LoadPanel
from modeling.gradient_boosting import GradientBoostingModel

# Naive UTC, matching LoadPanel.series(); TEST_END is exclusive.
TEST_START = pd.Timestamp(DATA_SPLIT.test_start).tz_convert(None)
TEST_END = pd.Timestamp(DATA_SPLIT.test_end).tz_convert(None)
HORIZON = 168  # Hours: seven days.


def main() -> None:
    # series() raises unless every hour up to TEST_END is present.
    y = LoadPanel().series(end=TEST_END)

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
