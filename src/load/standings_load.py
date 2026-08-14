import json
from pathlib import Path


def save_raw_payload(payload: dict, season: str) -> Path:
    raw_directory = Path("data/raw")

    raw_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = raw_directory / f"standings_{season}.json"

    with file_path.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        json.dump(
            payload,
            file,
            ensure_ascii=False,
            indent=4,
        )

    return file_path
