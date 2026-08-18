from src.transform.standings_transformer import transform_standings


def test_transform_standings():
    payload = {
        "standings": [
            {
                "type": "TOTAL",
                "table": [
                    {
                        "position": 1,
                        "team": {
                            "id": 1769,
                        },
                        "playedGames": 1,
                        "form": "W",
                        "won": 1,
                        "draw": 0,
                        "lost": 0,
                        "points": 3,
                        "goalsFor": 2,
                        "goalsAgainst": 0,
                        "goalDifference": 2,
                    }
                ],
            }
        ]
    }

    df = transform_standings(payload, 2026, 1)

    assert len(df) == 1
    assert df.iloc[0]["season"] == 2026
    assert df.iloc[0]["gameweek"] == 1
    assert df.iloc[0]["team_id"] == 1769
    assert df.iloc[0]["position"] == 1
    assert df.iloc[0]["points"] == 3
