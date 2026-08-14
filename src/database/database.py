from sqlalchemy import text

from src.database.connection import create_database_engine


def create_table_standings() -> None:
    engine = create_database_engine()

    query = """
    CREATE TABLE IF NOT EXISTS tbl_standings (
        id SERIAL PRIMARY KEY,
        position INTEGER,
        team_id INTEGER,
        team_name VARCHAR(100),
        team_short_name VARCHAR(50),
        team_tla VARCHAR(3),
        team_crest VARCHAR(100),
        played_games INTEGER,
        form VARCHAR(20),
        won INTEGER,
        draw INTEGER,
        lost INTEGER,
        points INTEGER,
        goals_for INTEGER,
        goals_against INTEGER,
        goal_difference INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        with engine.begin() as connection:
            connection.execute(text(query))
    finally:
        engine.dispose()
