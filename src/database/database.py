from sqlalchemy import text

from src.database.connection import create_database_engine


def create_table_teams() -> None:
    engine = create_database_engine()

    query = """
    CREATE TABLE IF NOT EXISTS tbl_teams (
        season INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        team_name VARCHAR(100),
        team_short_name VARCHAR(50),
        team_tla VARCHAR(3),
        team_crest VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT pk_teams
            PRIMARY KEY (season, team_id)
    );
    """

    try:
        with engine.begin() as connection:
            connection.execute(text(query))
    finally:
        engine.dispose()


def create_table_standings() -> None:
    engine = create_database_engine()

    query = """
    CREATE TABLE IF NOT EXISTS tbl_standings (
        id SERIAL PRIMARY KEY,
        season INTEGER NOT NULL,
        gameweek INTEGER NOT NULL,
        position INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        played_games INTEGER,
        form VARCHAR(20),
        won INTEGER,
        draw INTEGER,
        lost INTEGER,
        points INTEGER,
        goals_for INTEGER,
        goals_against INTEGER,
        goal_difference INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_standings_team
            FOREIGN KEY (season, team_id)
            REFERENCES tbl_teams (season, team_id)
    );
    """

    try:
        with engine.begin() as connection:
            connection.execute(text(query))
    finally:
        engine.dispose()


def create_all_databases() -> None:
    create_table_teams()
    create_table_standings()
