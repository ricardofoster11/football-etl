from src.transform.teams_transformer import transform_teams


def test_transform_teams():
    payload = {
        "teams": [
            {
                "id": 1769,
                "name": "SE Palmeiras",
                "shortName": "Palmeiras",
                "tla": "PAL",
                "crest": "https://example.com/palmeiras.png",
            }
        ]
    }

    df = transform_teams(payload, 2026)

    assert len(df) == 1
    assert df.iloc[0]["season"] == 2026
    assert df.iloc[0]["team_id"] == 1769
    assert df.iloc[0]["team_name"] == "SE Palmeiras"
