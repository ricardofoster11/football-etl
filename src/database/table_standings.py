import pandas as pd
from sqlalchemy import text

from src.database.connection import create_database_engine


def standings_exist_by_gameweek(season: int, gameweek: int) -> bool:
    engine = create_database_engine()

    query = """
        SELECT EXISTS (
            SELECT 1
            FROM tbl_standings
            WHERE season = :season
            and gameweek= :gameweek
        );
    """

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(query),
                {
                    "season": season,
                    "gameweek": gameweek
                }
            )

            return result.scalar_one()

    finally:
        engine.dispose()


def insert_standings(df_stadings: pd.DataFrame) -> None:
    engine = create_database_engine()

    try:
        df_stadings.to_sql(
            name="tbl_standings",
            con=engine,
            if_exists="append",
            index=False
        )

    finally:
        engine.dispose()
