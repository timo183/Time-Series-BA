import pandas as pd

from config import DATA_DIR


def save_panel(panel: pd.DataFrame):
    panel_path = DATA_DIR / "gold" / "panel.csv"
    panel_path.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(panel_path, sep=";", index=panel.index.name == "DateUTC")
