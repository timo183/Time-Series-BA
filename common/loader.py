import pandas as pd


def load_panel():
    df = pd.read_csv("../data/processed/panel.csv", sep=";")
    df["DateUTC"] = pd.to_datetime(df["DateUTC"])
    df["DateUTC"] = df["DateUTC"].dt.floor("h")
    df.set_index("DateUTC", inplace=True)
    df["Value"] = df["Value"].astype(float)

    return df
