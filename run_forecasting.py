import logging

from common.loader import load_panel
from modeling.gradient_boosting import GradientBoostingModel


def main() -> None:
    """Fit on the Gold panel and forecast the next 24 hourly observations."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    panel = load_panel(type="gold").sort_index()
    logging.info("Training on %s observations through %s", len(panel), panel.index[-1])

    model = GradientBoostingModel().fit(panel)
    predictions = model.predict(panel)
    logging.info("Next 24 hours:\n%s", predictions.to_string())


if __name__ == "__main__":
    main()
