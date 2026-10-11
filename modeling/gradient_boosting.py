import pandas as pd
from xgboost import XGBRegressor

from modeling.protocols import ForecastModel


class GradientBoostingModel(ForecastModel):
    def __init__(self):
        self.models: dict[int, XGBRegressor] = {}
        self.train_set: pd.DataFrame | None = None

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

    def fit(
        self,
        df: pd.DataFrame,
    ) -> "GradientBoostingModel":
        features = self.build_features(df)
        train_set = features.join(df[["Value"]]).dropna()

        models = {}

        for hour in range(24):
            hourly_train = train_set.loc[train_set.index.hour == hour]

            model = XGBRegressor(
                objective="reg:squarederror",
                random_state=42,
            )
            model.fit(
                hourly_train[features.columns],
                hourly_train["Value"],
            )
            models[hour] = model

        self.models = models
        self.train_set = train_set
        return self

    def predict(self, df: pd.DataFrame) -> pd.Series:
        history = df[["Value"]].copy()
        daily_predictions = []

        for _ in range(7):
            target_times = pd.date_range(
                start=history.index[-1] + pd.Timedelta(hours=1),
                periods=24,
                freq="h",
                name=history.index.name,
            )

            features = self.build_features(history, target_times)

            if features.isna().any().any():
                raise ValueError(
                    "Insufficient history or missing values in forecast features."
                )

            predictions = pd.Series(
                [
                    float(
                        self.models[timestamp.hour].predict(features.loc[[timestamp]])[
                            0
                        ]
                    )
                    for timestamp in target_times
                ],
                index=target_times,
                name="prediction",
            )

            daily_predictions.append(predictions)
            history = pd.concat([history, predictions.rename("Value").to_frame()])

        return pd.concat(daily_predictions)
