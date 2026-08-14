from src.extract.standings_extractor import extract_standings
from src.load.standings_load import save_raw_payload
from src.transform.standings_transformer import transform_standings
from src.database.database import create_table_standings

def main() -> None:
    # season = 2026

    # payload = extract_standings(season)

    # raw_file_path = save_raw_payload(
    #     payload,
    #     season,
    # )

    # df_ranking = transform_standings(payload)

    # print(f"Arquivo bruto salvo em: {raw_file_path}")
    # print(df_ranking.dtypes)

    create_table_standings()

    # engine = create_database_engine()
    # test_database_connection(engine)
    # print("Conexão com PostgreSQL validada com sucesso.")


if __name__ == "__main__":
    main()
