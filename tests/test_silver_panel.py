import pandas as pd

from common.loader import load_panel


def test_silver_schema_and_values() -> None:
    panel = load_panel(type="silver")
    assert panel.index.name == "DateUTC"
    assert {"Value", "TimeFrom", "TimeTo"}.issubset(panel.columns)
    assert not pd.to_datetime(panel.index, utc=True, errors="coerce").isna().any()
    assert not panel.isna().any().any()
