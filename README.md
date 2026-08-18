# Football ETL

Projeto de ETL desenvolvido em Python para extração, transformação e persistência de dados do **Campeonato Brasileiro Série A**, utilizando dados fornecidos pela API football-data.org.

O projeto coleta informações dos times participantes de uma temporada e o histórico da classificação do campeonato por rodada, realiza o tratamento e validação dos dados e persiste as informações em um banco PostgreSQL.

## Objetivo

O objetivo do projeto é aplicar conceitos de Engenharia e Análise de Dados através da construção de um pipeline ETL completo:

```text
football-data.org
        ↓
     Extract
        ↓
    Transform
        ↓
    Validate
        ↓
      Load
        ↓
   PostgreSQL
```

## Tecnologias

* Python
* Pandas
* PostgreSQL
* SQLAlchemy
* Docker
* Requests
* Pytest
* Postman
* Power BI

## Fonte de Dados

Os dados são obtidos através da API football-data.org utilizando a versão `v4`.

O escopo atual do projeto utiliza o **Campeonato Brasileiro Série A**, identificado pelo código `BSA`.

### Times da temporada

```http
GET /v4/competitions/BSA/teams?season={season}
```

Utilizado para obter os times participantes da temporada.

### Classificação por rodada

```http
GET /v4/competitions/BSA/standings?season={season}&matchday={matchday}
```

Utilizado para obter a classificação do campeonato em uma determinada rodada.

Mais detalhes sobre os endpoints e os campos utilizados estão disponíveis em:

```text
docs/api-contract.md
```

## Pipeline ETL

### Extract

A camada de extração realiza as requisições HTTP para a API football-data.org.

Os payloads retornados pela API são armazenados em formato JSON na camada `data/raw` antes do processamento.

### Transform

Os dados retornados pela API são transformados utilizando Pandas.

Entre as transformações realizadas estão:

* normalização das estruturas JSON;
* seleção dos campos utilizados pelo projeto;
* padronização dos nomes das colunas;
* inclusão da temporada e rodada;
* preparação dos DataFrames para persistência.

### Validate

Antes da carga, os DataFrames passam por validações para identificar inconsistências nos dados.

### Load

Após a transformação e validação, os dados são persistidos no PostgreSQL.

O pipeline evita a inserção repetida dos times de uma mesma temporada e da classificação de uma rodada já processada.

## Modelo de Dados

O banco possui duas tabelas principais.

### `tbl_teams`

Armazena os times participantes de cada temporada.

A chave primária é composta por:

```text
(season, team_id)
```

### `tbl_standings`

Armazena o histórico da classificação dos times por rodada.

Cada registro contém informações como:

* temporada;
* rodada;
* posição;
* time;
* jogos disputados;
* vitórias;
* empates;
* derrotas;
* pontos;
* gols marcados;
* gols sofridos;
* saldo de gols.

A tabela possui relacionamento com `tbl_teams` através de:

```text
(season, team_id)
```

O modelo do banco está documentado em:

```text
docs/databases.dbml
```

## Estrutura do Projeto

```text
football-etl/
│
├── data/
│   └── raw/
│
├── docs/
│   ├── api-contract.md
│   └── databases.dbml
│
├── src/
│   ├── config/
│   │   └── logger.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── database.py
│   │   ├── table_standings.py
│   │   └── table_teams.py
│   │
│   ├── extract/
│   │   └── api_extractor.py
│   │
│   ├── load/
│   │   └── standings_load.py
│   │
│   ├── transform/
│   │   ├── standings_transformer.py
│   │   └── teams_transformer.py
│   │
│   ├── validate/
│   │   └── standings_validator.py
│   │
│   └── orchestrator.py
│
├── tests/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Configuração

### 1. Clone o repositório

```bash
git clone <repository-url>
cd football-etl
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv
```

Ative o ambiente:

```bash
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie o arquivo `.env` utilizando `.env.example` como referência.

As configurações incluem:

* API Token da football-data.org;
* host do PostgreSQL;
* porta;
* banco de dados;
* usuário;
* senha.

O arquivo `.env` não deve ser versionado.

### 5. Suba o PostgreSQL

```bash
docker compose up -d
```

### 6. Execute o pipeline

```bash
python main.py
```

A temporada e a rodada processadas são definidas na execução do pipeline.

## Testes

O projeto utiliza `pytest` para execução dos testes automatizados.

Para executar:

```bash
pytest -v
```

Os testes atuais cobrem inicialmente as transformações dos dados de times e classificação.

## Dashboard

Os dados armazenados no PostgreSQL serão utilizados como fonte para construção de um dashboard no Power BI.

O dashboard será responsável pela camada de visualização e análise dos dados históricos do Campeonato Brasileiro Série A.

## Próximas Evoluções

* Dashboard analítico em Power BI;
* ampliação da cobertura de testes;
* parametrização da execução do pipeline;
* evolução das validações de qualidade dos dados;
* inclusão de novas análises e fontes de dados.

## Documentação

* `docs/api-contract.md` — contrato e endpoints utilizados da API.
* `docs/databases.dbml` — modelo e relacionamento das tabelas PostgreSQL.
