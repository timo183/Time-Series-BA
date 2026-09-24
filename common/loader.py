from pathlib import Path

import pandas as pd


def load_panel(type: str) -> pd.DataFrame:
    panel_path = Path(__file__).resolve().parents[1] / "data" / type / "panel.csv"
    df = pd.read_csv(panel_path, sep=";")
    df["DateUTC"] = pd.to_datetime(df["DateUTC"])
    df.set_index("DateUTC", inplace=True)
    df["Value"] = df["Value"].astype(float)

    return df
