"""Kurzer Modelltest: uv run python -m modeling.test_gradient_boosting."""

import numpy as np
import pandas as pd

from common.loader import load_panel
from modeling.gradient_boosting import GradientBoostingModel

# Alle Angaben in UTC: Beginn inklusive, Ende exklusive.
TRAIN_START = "2015-01-01 01:00"
TRAIN_END = "2020-03-31"
TEST_START = "2020-04-01"
TEST_END = "2020-04-02"


def run_daily_forecast() -> None:
    """Trainiert einmal und prognostiziert täglich mit verfügbarer Historie."""
    train_start = pd.Timestamp(TRAIN_START, tz="UTC")
    train_end = pd.Timestamp(TRAIN_END, tz="UTC")
    test_start = pd.Timestamp(TEST_START, tz="UTC")
    test_end = pd.Timestamp(TEST_END, tz="UTC")

    if not train_start < train_end <= test_start < test_end:
        raise ValueError(
            "Erforderlich: TRAIN_START < TRAIN_END <= TEST_START < TEST_END."
        )
    if any(t != t.floor("h") for t in (train_start, train_end)):
        raise ValueError("Trainingsgrenzen müssen auf vollen Stunden liegen.")
    if any(t != t.normalize() for t in (test_start, test_end)):
        raise ValueError("Testgrenzen müssen für ganze UTC-Tage um 00:00 liegen.")

    data = load_panel("gold")
    data.index = pd.to_datetime(data.index, utc=True)
    data = data.sort_index()

    if data.empty or not data.index.is_unique:
        raise ValueError("Das Gold-Panel ist leer oder enthält doppelte Zeiten.")

    expected_index = pd.date_range(
        data.index[0], data.index[-1], freq="h", name=data.index.name
    )
    if not data.index.equals(expected_index) or not data.index.equals(
        data.index.floor("h")
    ):
        raise ValueError("Das Gold-Panel muss lückenlos stündlich sein.")
    if not np.isfinite(data["Value"].to_numpy()).all():
        raise ValueError("Das Gold-Panel enthält fehlende oder ungültige Werte.")

    if train_start < data.index[0] or test_end > data.index[-1] + pd.Timedelta(hours=1):
        raise ValueError("Die gewählten Zeiträume liegen außerhalb des Gold-Panels.")

    train = data.loc[(data.index >= train_start) & (data.index < train_end)]
    actual = data.loc[(data.index >= test_start) & (data.index < test_end), "Value"]
    if len(train) < 192:
        raise ValueError("Für das Training sind mindestens 192 Stunden erforderlich.")

    print(f"Training: {train.index[0]} bis {train.index[-1]}")
    print(f"Test: {test_start} bis {test_end} (Ende exklusive)")

    model = GradientBoostingModel()
    model.fit(train)

    forecasts = []
    for day in pd.date_range(test_start, test_end, freq="D", inclusive="left"):
        # Frühere Testtage dürfen als beobachtete Historie eingehen.
        # Die Modelle bleiben auf dem ursprünglichen Trainingsstand.
        history = data.loc[
            (data.index >= day - pd.Timedelta(hours=168)) & (data.index < day)
        ]
        daily_forecast = model.predict(history)
        forecasts.append(daily_forecast)

        features = model.build_features(history, daily_forecast.index)
        for lag in (24, 48, 168):
            expected = history["Value"].reindex(
                daily_forecast.index - pd.Timedelta(hours=lag)
            )
            np.testing.assert_allclose(features[f"lag_{lag}"], expected)

        for window in (24, 168):
            np.testing.assert_allclose(
                features[f"ma_{window}"], history["Value"].iloc[-window:].mean()
            )

    forecast = pd.concat(forecasts)

    assert set(model.models) == set(range(24))
    assert model.train_set is not None
    assert not model.train_set.empty
    pd.testing.assert_index_equal(forecast.index, actual.index)
    assert np.isfinite(forecast.to_numpy()).all()

    print(pd.DataFrame({"actual": actual, "prediction": forecast}).round(2))
    print(f"\nMAE (Gold-Panel): {(forecast - actual).abs().mean():.2f}")
    print(f"Trainingszeilen: {len(model.train_set)}, Modelle: {len(model.models)}")


if __name__ == "__main__":
    run_daily_forecast()
