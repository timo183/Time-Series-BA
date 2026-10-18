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
        "2023-01-01",
        periods=8 * 24,
        freq="h",
        tz="UTC",
        name="DateUTC",
    )
    return pd.DataFrame(
        {"Value": np.arange(len(timestamps), dtype=float)},
        index=timestamps,
    )


def fit_model(model: GradientBoostingModel, panel: DataFrame) -> GradientBoostingModel:
    return model.fit(df=panel)


def test_model_training(
    model: GradientBoostingModel,
    panel: pd.DataFrame,
) -> None:
    model.fit(panel)

    assert model.fit(panel) is model
    assert set(model.models) == set(range(24))


def test_lag_features(model, panel):
    # Reverse order also checks that target ordering is preserved.
    targets = panel.index[[180, 168]]

    actual = model._build_lag_features(panel["Value"], targets)

    expected = pd.DataFrame(
        {
            "lag_24": [156.0, 144.0],
            "lag_48": [132.0, 120.0],
            "lag_168": [12.0, 0.0],
        },
        index=targets,
    )
    pd.testing.assert_frame_equal(actual, expected)


def test_ma_features(model, panel):
    targets = panel.index[[168, 180]]

    actual = model._build_ma_features(panel["Value"], targets)

    # Both hours use the window ending January 7 at 23:00.
    expected = pd.DataFrame(
        {
            "ma_24": [155.5, 155.5],
            "ma_168": [83.5, 83.5],
        },
        index=targets,
    )
    pd.testing.assert_frame_equal(actual, expected)
