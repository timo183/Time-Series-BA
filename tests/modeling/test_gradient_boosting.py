import numpy as np
import pandas as pd
import pytest
from pandas import DataFrame

from modeling.gradient_boosting import GradientBoostingModel


@pytest.fixture(scope="module")
def model() -> GradientBoostingModel:
    return GradientBoostingModel()


@pytest.fixture
def panel() -> pd.DataFrame:
    timestamps = pd.date_range(
        start="2023-01-01",
        periods=14 * 24,
        freq="h",
        tz="UTC",
        name="DateUTC",
    )
    rng = np.random.default_rng(42)

    values = (
        1000
        + 200 * np.sin(2 * np.pi * timestamps.hour.to_numpy() / 24)
        - 100 * (timestamps.dayofweek.to_numpy() >= 5)
        + rng.normal(0, 10, len(timestamps))
    )

    return pd.DataFrame({"Value": values}, index=timestamps)


def fit_model(model: GradientBoostingModel, panel: DataFrame) -> GradientBoostingModel:
    return model.fit(panel)


def test_model_training(
    model: GradientBoostingModel,
    panel: pd.DataFrame,
) -> None:
    model.fit(panel)

    assert model.fit(panel) is model
    assert set(model.models) == set(range(24))
