import pandas as pd

REQUIRED_COLUMNS = [
    "position",
    "team_id",
    "team_name",
    "team_short_name",
    "team_tla",
    "team_crest",
    "played_games",
    "form",
    "won",
    "draw",
    "lost",
    "points",
    "goals_for",
    "goals_against",
    "goal_difference",
]


def validate_ranking(df: pd.DataFrame) -> None:

    missing_columns = []

    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            missing_columns.append(column)

    if missing_columns:
        raise ValueError(
            f"Colunas obrigatórias ausentes: {missing_columns}"
        )

    if df.empty:
        raise ValueError("O ranking está vazio")

    if df["team_id"].isnull().any():
        raise ValueError("Existem times sem team_id.")

    if df["team_id"].duplicated().any():
        raise ValueError("Existem times duplicados no ranking.")
