import pandas as pd
from xgboost import XGBRegressor

from modeling.protocols import ForecastModel


class GradientBoostingModel(ForecastModel):
    FEATURE_COLUMNS = [
        "lag_24",
        "lag_48",
        "lag_168",
        "ma_24",
        "ma_168",
    ]

    def __init__(self):
        self.models: dict[int, XGBRegressor] = {}
        self.train_set: pd.DataFrame | None = None

    def build_features(
        self,
        df: pd.DataFrame,
        target_times: pd.DatetimeIndex | None = None,
    ) -> pd.DataFrame:

        if target_times is None:
            target_times = df.index

        values = df["Value"]
        features = pd.DataFrame(index=target_times)

        for lag in (24, 48, 168):
            source_times = target_times - pd.Timedelta(hours=lag)
            features[f"lag_{lag}"] = values.reindex(source_times).to_numpy()

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

    def fit(
        self,
        df: pd.DataFrame,
    ) -> "GradientBoostingModel":
        features = self.build_features(df)
        train_set = features.join(df[["Value"]]).dropna()

        if set(train_set.index.hour) != set(range(24)):
            raise ValueError(
                "Nach der Feature-Berechnung fehlen Trainingsdaten "
                "für mindestens eine Tagesstunde."
            )

        models = {}

        for hour in range(24):
            hourly_train = train_set.loc[train_set.index.hour == hour]

            model = XGBRegressor(
                objective="reg:squarederror",
                random_state=42,
            )
            model.fit(
                hourly_train[self.FEATURE_COLUMNS],
                hourly_train["Value"],
            )
            models[hour] = model

        self.models = models
        self.train_set = train_set
        return self

    def predict(self, df: pd.DataFrame) -> pd.Series:
        if len(self.models) != 24:
            raise ValueError("Das Modell muss zuerst trainiert werden.")

        target_times = pd.date_range(
            start=df.index[-1] + pd.Timedelta(hours=1),
            periods=24,
            freq="h",
            name=df.index.name,
        )

        features = self.build_features(df, target_times)

        if features.isna().any().any():
            raise ValueError(
                "Für die Prognose fehlen historische Werte; "
                "mindestens 168 vollständige Stunden sind erforderlich."
            )

        predictions = [
            float(
                self.models[timestamp.hour].predict(
                    features.loc[[timestamp], self.FEATURE_COLUMNS]
                )[0]
            )
            for timestamp in target_times
        ]

        return pd.Series(
            predictions,
            index=target_times,
            name="prediction",
        )
