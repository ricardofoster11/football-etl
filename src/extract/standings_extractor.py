import os

import requests
from dotenv import load_dotenv

load_dotenv()


def extract_standings(season: str, matchday: int) -> dict:
    api_token = os.getenv("FOOTBALL_DATA_API_TOKEN")

    if not api_token:
        raise RuntimeError(
            "A variavel FOOTBALL_DATA_API_TOKEN não foi configurada"
        )

    url = "https://api.football-data.org/v4/competitions/BSA/standings"

    headers = {
        "X-Auth-Token": api_token
    }

    params = {
        "season": season,
        "matchday": matchday
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()
