import logging

from src.database.database import create_all_databases
from src.database.table_standings import insert_standings, standings_exist_by_gameweek
from src.database.table_teams import insert_teams, teams_exist_by_season
from src.extract.api_extractor import extract_standings, extract_teams
from src.transform.standings_transformer import transform_standings
from src.transform.teams_transformer import transform_teams

logger = logging.getLogger(__name__)


def execute(season: int, matchday: int) -> None:
    logger.info("starting application...")

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

    logger.info("API Stadings")
    if standings_exist_by_gameweek(season, matchday):
        logger.info(f"{season} season, Week {matchday}, already entered into the table.")
    else:
        stadings = extract_standings(season, matchday)
        df_stadings = transform_standings(stadings, season, matchday)
        insert_standings(df_stadings)
        logger.info(f"Stadings for the {season} season, Week {matchday} already registered")
