import numpy as np
import pandas as pd
from sktime.forecasting.base import BaseForecaster
from xgboost import XGBRegressor


class GradientBoostingModel(BaseForecaster):
    _tags = {
        "y_inner_mtype": "pd.Series",
        "scitype:y": "univariate",
        "capability:exogenous": False,
        "requires-fh-in-fit": False,
    }

    def __init__(
        self,
        n_lags=12,
        period=12,
        K=3,
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    ):
        self.n_lags = n_lags
        self.period = period
        self.K = K
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.random_state = random_state

        super().__init__()

    def _build_lag_features(
        self,
        values: pd.Series,
        target_times: pd.DatetimeIndex,
    ) -> pd.DataFrame:
        features = pd.DataFrame(index=target_times)

        for lag in (24, 48, 168):
            source_times = target_times - pd.Timedelta(hours=lag)
            features[f"lag_{lag}"] = values.reindex(source_times).to_numpy()

        return features

    def _build_ma_features(
        self,
        values: pd.Series,
        target_times: pd.DatetimeIndex,
    ) -> pd.DataFrame:
        features = pd.DataFrame(index=target_times)
        last_observed_times = target_times.normalize() - pd.Timedelta(hours=1)

        for window in (24, 168):
            rolling_mean = values.rolling(
                window=window,
                min_periods=window,
            ).mean()

            features[f"ma_{window}"] = rolling_mean.reindex(
                last_observed_times
            ).to_numpy()

        return features

    def build_features(
        self,
        df: pd.DataFrame,
        target_times: pd.DatetimeIndex | None = None,
    ) -> pd.DataFrame:
        if target_times is None:
            target_times = df.index

        values = df["Value"]

        return pd.concat(
            [
                self._build_lag_features(values, target_times),
                self._build_ma_features(values, target_times),
            ],
            axis=1,
        )

    def _fit(
        self,
        y: pd.Series,
        X: pd.DataFrame | None = None,
        fh=None,
    ) -> "GradientBoostingModel":
        features = self.build_features(y.to_frame(name="Value"))

        valid_rows = features.notna().all(axis=1) & y.notna()
        train_features = features.loc[valid_rows]
        train_targets = y.loc[valid_rows]

        if train_features.empty:
            raise ValueError("Insufficient history to build training features.")

        self.model_ = XGBRegressor(
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            max_depth=self.max_depth,
            subsample=self.subsample,
            colsample_bytree=self.colsample_bytree,
            objective="reg:squarederror",
            tree_method="hist",
            random_state=self.random_state,
        )
        self.model_.fit(train_features, train_targets)

        self.history_ = y.copy()
        self.target_name_ = y.name

        return self

    def _predict(self, fh, X=None) -> pd.Series:
        steps = fh.to_relative(self.cutoff).to_numpy().astype(int)

        if np.any(steps <= 0):
            raise ValueError("Only future forecasts supported.")

        history = self.history_.to_frame(name="Value").astype(float)

        target_times = pd.date_range(
            start=history.index[-1] + pd.Timedelta(hours=1),
            periods=int(steps.max()),
            freq="h",
            name=history.index.name,
        )

        predictions = []

        for timestamp in target_times:
            features = self.build_features(
                history,
                target_times=pd.DatetimeIndex([timestamp]),
            )

            if features.isna().any().any():
                raise ValueError("Insufficient history or missing forecast features.")

            prediction = float(self.model_.predict(features)[0])
            predictions.append(prediction)

            history.loc[timestamp, "Value"] = prediction

        return pd.Series(
            np.asarray(predictions)[steps - 1],
            index=fh.to_absolute_index(self.cutoff),
            name=self.target_name_,
        )
