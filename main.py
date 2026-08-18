from src.config.logger import setup_logging
from src.orchestrator import execute


def main() -> None:
    setup_logging()
    execute(season=2026, matchday=10)


if __name__ == "__main__":
    main()
