import logging

from common.loader import load_panel
from common.logging_config import configure_logging
from modeling.gradient_boosting import GradientBoostingModel

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()
    panel = load_panel(type="gold").sort_index()
    logger.info("Training on %s observations through %s", len(panel), panel.index[-1])

    model: GradientBoostingModel = GradientBoostingModel().fit(panel)
    predictions = model.predict(panel)
    logger.info("Next 24 hours:\n%s", predictions.to_string())


if __name__ == "__main__":
    main()
