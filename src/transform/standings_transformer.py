import pandas as pd

from src.validate.standings_validator import validate_ranking


def transform_standings(payload: dict, season: int, matchday: int) -> pd.DataFrame:
    standings = payload["standings"]

    total_standings = None

    for standing in standings:

        if standing["type"] == "TOTAL":
            total_standings = standing
            break

    if total_standings is None:
        raise ValueError("Classificação TOTAL não encontrada.")

    ranking = total_standings["table"]

    df_ranking = pd.json_normalize(ranking)

    df_ranking = df_ranking.rename(
        columns={
            "team.id": "team_id",
            "team.name": "team_name",
            "team.shortName": "team_short_name",
            "team.tla": "team_tla",
            "team.crest": "team_crest",
            "playedGames": "played_games",
            "goalsFor": "goals_for",
            "goalsAgainst": "goals_against",
            "goalDifference": "goal_difference",
        }
    )

    df_ranking["season"] = season
    df_ranking["gameweek"] = matchday

    df_ranking = df_ranking[
        [
            "season",
            "gameweek",
            "position",
            "team_id",
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
    ]

    validate_ranking(df_ranking)

    return df_ranking
