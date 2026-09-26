"""Structural interface for point-forecast models; see modeling/README.md.

These contracts describe required behavior, not runtime validation. Concrete
implementations must validate inputs and enforce information availability.
"""

from typing import Protocol, Self

import pandas as pd


class ForecastModel(Protocol):
    def fit(
        self,
        df: pd.DataFrame,
    ) -> Self:
        pass

    def predict(
        self,
        df: pd.DataFrame,
    ) -> pd.Series:
        pass
