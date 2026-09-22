from pathlib import Path

import pandas as pd


PANEL_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "panel.csv"


def load_panel():
    df = pd.read_csv(PANEL_PATH, sep=";")
    df["DateUTC"] = pd.to_datetime(df["DateUTC"])
    df["DateUTC"] = df["DateUTC"].dt.floor("h")
    df.set_index("DateUTC", inplace=True)
    df["Value"] = df["Value"].astype(float)

    return df
