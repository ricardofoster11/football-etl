import pandas as pd


def transform_teams(payload: dict, season: int) -> pd.DataFrame:
    teams = payload["teams"]

    if teams is None:
        raise ValueError("Times não encontrados.")

    df_teams = pd.json_normalize(teams)

    df_teams = df_teams.rename(
        columns={
            "id": "team_id",
            "name": "team_name",
            "shortName": "team_short_name",
            "tla": "team_tla",
            "crest": "team_crest"
        }
    )

    df_teams["season"] = season

    df_teams = df_teams[
        [
            "season",
            "team_id",
            "team_name",
            "team_short_name",
            "team_tla",
            "team_crest"
        ]
    ]

    df_teams = df_teams.sort_values(by="team_name")

    return df_teams
