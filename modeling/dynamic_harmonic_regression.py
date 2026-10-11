"""Fourier regression with non-seasonal ARIMA errors for hourly UTC data."""

from typing import Self

import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

from modeling.protocols import ForecastModel


class DynamicHarmonicRegressionModel(ForecastModel):
    def __init__(
        self,
        periods: tuple[float, ...] = (24, 168),
        harmonics: tuple[int, ...] = (3, 3),
        order: tuple[int, int, int] = (1, 0, 1),
        minimum_history: int = 168,
        maxiter: int = 200,
    ) -> None:
        self.periods = tuple(periods)
        self.harmonics = tuple(harmonics)
        self.order = tuple(order)
        self.minimum_history = minimum_history
        self.maxiter = maxiter
        frequencies: list[float] = []
        for period, count in zip(periods, harmonics):
            for harmonic in range(1, count + 1):
                frequency = harmonic / period
                if not any(
                    np.isclose(frequency, existing, rtol=1e-12, atol=1e-15)
                    for existing in frequencies
                ):
                    frequencies.append(frequency)
        self._frequencies = tuple(frequencies)
        self._result = None
        self._training_end: pd.Timestamp | None = None
        self._scale = 1.0

    def _build_features(self, index: pd.DatetimeIndex) -> pd.DataFrame:
        hours = np.asarray(
            (index - pd.Timestamp("2000-01-01", tz="UTC")) / pd.Timedelta(hours=1)
        )
        features = pd.DataFrame(index=index)
        if self.order[1] == 0:
            features["constant"] = np.ones(len(index))
        for number, frequency in enumerate(self._frequencies):
            phase = 2 * np.pi * np.remainder(hours * frequency, 1)
            if not np.isclose(frequency, 0.5, rtol=1e-12, atol=1e-15):
                features[f"sin_{number}"] = np.sin(phase)
            features[f"cos_{number}"] = np.cos(phase)
        return features

    def fit(self, df: pd.DataFrame) -> Self:

        features = self._build_features(df.index)
        # Scaling improves optimization for electricity loads measured in MW.
        scale = max(float(df["Value"].abs().max()), 1.0)
        model = SARIMAX(
            df["Value"] / scale,
            exog=features,
            order=self.order,
            seasonal_order=(0, 0, 0, 0),
            trend="n",
        )
        result = model.fit(disp=False, maxiter=self.maxiter)
        self._result = result
        self._training_end = df.index[-1]
        self._scale = scale
        return self

    def predict(self, df: pd.DataFrame, horizon: int = 24) -> pd.Series:
        target_times = pd.date_range(
            df.index[-1] + pd.Timedelta(hours=1),
            periods=horizon,
            freq="h",
            name=df.index.name,
        )
        filtered = self._result.apply(
            df["Value"] / self._scale,
            exog=self._build_features(df.index),
            refit=False,
        )
        forecast = (
            filtered.get_forecast(
                steps=horizon, exog=self._build_features(target_times)
            ).predicted_mean.to_numpy()
            * self._scale
        )
        return pd.Series(forecast, index=target_times, name="prediction")
