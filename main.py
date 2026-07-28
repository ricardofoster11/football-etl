from src.extract.standings_extractor import extract_standings


def main() -> None:
    payload = extract_standings("2026")

    standings = payload["standings"]

    total_standings = next(
        standing
        for standing in standings
        if standing["type"] == "TOTAL"
    )

    print(total_standings["type"])


if __name__ == "__main__":
    main()
