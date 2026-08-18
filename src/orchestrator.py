import logging

from src.database.database import create_all_databases
from src.database.table_teams import insert_teams, teams_exist_by_season
from src.extract.api_extractor import extract_teams
from src.transform.teams_transformer import transform_teams

logger = logging.getLogger(__name__)


def execute() -> None:
    logger.info("starting application...")

    season = 2026
    matchday = 1
    logger.info(f"Season: {season} | Matchday: {matchday}")

    logger.info("creating tables")
    create_all_databases()
    logger.info("tables successfully created")

    logger.info("API Teams")
    if teams_exist_by_season(season):
        logger.info(f"Teams for the {season} season already registered")
    else:
        teams = extract_teams(season)
        df_teams = transform_teams(teams, season)
        insert_teams(df_teams)
        logger.info("Teams successfully added")
