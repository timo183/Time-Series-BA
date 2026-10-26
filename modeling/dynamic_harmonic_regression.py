"""Fourier regression with non-seasonal ARIMA errors for hourly UTC data."""

from typing import Self

import numpy as np
import pandas as pd
from sktime.forecasting.base import BaseForecaster, ForecastingHorizon
from statsmodels.tsa.statespace.sarimax import SARIMAX

# hier steht wie man dhr für stromverbrauch anwendet: https://otexts.com/fpp3/advanced.html#example-electricity-demand


class DynamicHarmonicRegressionModel(BaseForecaster):
    _tags = {
        "y_inner_mtype": "pd.Series",
        "scitype:y": "univariate",
        "capability:exogenous": False,
        "capability:insample": False,
        "requires-fh-in-fit": False,
    }

    def __init__(
        self,
        periods: tuple[float, ...] = (24, 168),
        harmonics: tuple[int, ...] = (3, 3),
        order: tuple[int, int, int] = (1, 0, 1),
        minimum_history: int = 168,
        maxiter: int = 200,
    ) -> None:
        self.periods = periods
        self.harmonics = harmonics
        self.order = order
        self.minimum_history = minimum_history
        self.maxiter = maxiter

        super().__init__()

    def _build_features(
        self,
        index: pd.DatetimeIndex,
    ) -> pd.DataFrame:
        utc_index = pd.to_datetime(index, utc=True)
        reference = pd.Timestamp("2000-01-01", tz="UTC")
        hours = np.asarray((utc_index - reference) / pd.Timedelta(hours=1))

        features = pd.DataFrame(index=index)

        if self.order[1] == 0:
            features["constant"] = np.ones(len(index))

        for number, frequency in enumerate(self.frequencies_):
            phase = 2 * np.pi * np.remainder(hours * frequency, 1)

            # At the Nyquist frequency, the sine term is always zero
            # for this hourly grid.
            if not np.isclose(frequency, 0.5, rtol=1e-12, atol=1e-15):
                features[f"sin_{number}"] = np.sin(phase)

            features[f"cos_{number}"] = np.cos(phase)

        return features

    def _fit(
        self,
        y: pd.Series,
        X: pd.DataFrame | None = None,
        fh: ForecastingHorizon | None = None,
    ) -> Self:

        frequencies: list[float] = []

        for period, count in zip(self.periods, self.harmonics):
            for harmonic in range(1, count + 1):
                frequency = harmonic / period

                if not any(
                    np.isclose(frequency, existing, rtol=1e-12, atol=1e-15)
                    for existing in frequencies
                ):
                    frequencies.append(frequency)

        self.frequencies_ = tuple(frequencies)
        self.target_name_ = y.name
        self.index_name_ = y.index.name

        # Scaling improves optimization for load values measured in MW.
        self.scale_ = max(float(y.abs().max()), 1.0)

        model = SARIMAX(
            y / self.scale_,
            exog=self._build_features(y.index),
            order=self.order,
            seasonal_order=(0, 0, 0, 0),
            trend="n",
        )
        self.result_ = model.fit(
            disp=False,
            maxiter=self.maxiter,
        )

        return self

    def _predict(
        self,
        fh: ForecastingHorizon,
        X: pd.DataFrame | None = None,
    ) -> pd.Series:
        steps = fh.to_relative(self.cutoff).to_numpy().astype(int)

        if np.any(steps <= 0):
            raise ValueError("Only future forecasts are supported.")

        target_times = pd.date_range(
            start=self.cutoff[0] + pd.Timedelta(hours=1),
            periods=int(steps.max()),
            freq="h",
            name=self.index_name_,
        )

        forecast = self.result_.get_forecast(
            steps=len(target_times),
            exog=self._build_features(target_times),
        )
        predictions = forecast.predicted_mean.to_numpy() * self.scale_

        return pd.Series(
            predictions[steps - 1],
            index=fh.to_absolute_index(self.cutoff),
            name=self.target_name_,
        )
