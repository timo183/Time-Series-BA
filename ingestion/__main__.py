"""Rebuild the panel cache: ``uv run python -m ingestion``."""

from ingestion.panel import LoadPanel


if __name__ == "__main__":
    panel = LoadPanel()
    path = panel.build_cache()
    df = panel.clean()
    print(
        f"Wrote {df.height} rows ({df['DateUTC'].min()} – {df['DateUTC'].max()}), "
        f"{df['timestamp_corrected'].sum()} corrected timestamps, to {path}"
    )
