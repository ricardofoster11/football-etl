import logging

from src.database.database import create_all_databases

logger = logging.getLogger(__name__)


def execute() -> None:
    logger.info("starting application...")

    season = 2026
    matchday = 1
    logger.info(f"Season: {season} | Matchday: {matchday}")

    logger.info("creating tables")
    create_all_databases()
    logger.info("tables successfully created")
