from src.extract.standings_extractor import extract_standings
from src.load.standings_load import save_raw_payload
from src.transform.standings_transformer import transform_standings
from src.config.logger import setup_logging
from src.orchestrator import execute


def main() -> None:
    setup_logging()
    execute()


    # payload = extract_standings(season, matchday)

    # raw_file_path = save_raw_payload(
    #     payload,
    #     season,
    # )

    # df_ranking = transform_standings(payload, matchday)

    # print(f"Arquivo bruto salvo em: {raw_file_path}")
    # print(df_ranking.head())


    # engine = create_database_engine()
    # test_database_connection(engine)
    # print("Conexão com PostgreSQL validada com sucesso.")


if __name__ == "__main__":
    main()
