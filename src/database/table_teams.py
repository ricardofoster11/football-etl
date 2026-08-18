import pandas as pd
from sqlalchemy import text

from src.database.connection import create_database_engine


def teams_exist_by_season(season: int) -> bool:
    engine = create_database_engine()

    query = """
        SELECT EXISTS (
            SELECT 1
            FROM tbl_teams
            WHERE season = :season
        );
    """

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(query),
                {"season": season}
            )

            return result.scalar_one()

    finally:
        engine.dispose()


def insert_teams(df_teams: pd.DataFrame) -> None:
    engine = create_database_engine()

    try:
        df_teams.to_sql(
            name="tbl_teams",
            con=engine,
            if_exists="append",
            index=False
        )

    finally:
        engine.dispose()
