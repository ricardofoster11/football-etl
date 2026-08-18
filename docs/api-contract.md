# API Contract — football-data.org

## 1. Objetivo

A API `football-data.org` é utilizada como fonte externa de dados do projeto `football-etl`.

Na versão atual, o projeto possui como escopo o **Campeonato Brasileiro Série A**, identificado na API pelo código:

```text
BSA
```

O pipeline realiza a extração de dados de times e classificação, transformação e validação dos dados e carga das informações tratadas no PostgreSQL.

---

## 2. Configuração da API

| Propriedade      | Valor                           |
| ---------------- | ------------------------------- |
| Provider         | football-data.org               |
| Base URL         | `https://api.football-data.org` |
| API Version      | `v4`                            |
| Competition      | Campeonato Brasileiro Série A   |
| Competition Code | `BSA`                           |
| Response Format  | `JSON`                          |
| HTTP Method      | `GET`                           |

---

## 3. Autenticação

A API utiliza autenticação por API Key enviada através de um Header HTTP.

### Header obrigatório

| Header         | Valor                                    |
| -------------- | ---------------------------------------- |
| `X-Auth-Token` | API Key fornecida pela football-data.org |

Exemplo:

```http
X-Auth-Token: YOUR_API_TOKEN
```

A API Key não deve ser armazenada no código-fonte ou versionada no Git.

No projeto, a chave de acesso é configurada através de variável de ambiente.

---

## 4. Endpoints utilizados pelo pipeline

A versão atual do ETL utiliza dois endpoints:

1. Times participantes da temporada;
2. Classificação do campeonato por rodada.

---

### 4.1 Times do Campeonato Brasileiro Série A

```http
GET /v4/competitions/BSA/teams
```

### Query Parameters

| Parâmetro | Tipo   | Exemplo | Descrição            |
| --------- | ------ | ------- | -------------------- |
| `season`  | String | `2026`  | Temporada consultada |

Exemplo:

```http
GET /v4/competitions/BSA/teams?season=2026
```

### Objetivo

Obter os times participantes do Campeonato Brasileiro Série A na temporada informada.

Os dados relevantes são transformados e persistidos na tabela:

```text
tbl_teams
```

### Campos utilizados

| Campo da API | Campo tratado     |
| ------------ | ----------------- |
| `id`         | `team_id`         |
| `name`       | `team_name`       |
| `shortName`  | `team_short_name` |
| `tla`        | `team_tla`        |
| `crest`      | `team_crest`      |

O campo `season` é acrescentado pelo pipeline para identificar a temporada à qual o time está associado.

A identificação única de um time no contexto do projeto é composta por:

```text
season + team_id
```

---

### 4.2 Classificação por rodada

```http
GET /v4/competitions/BSA/standings
```

### Query Parameters

| Parâmetro  | Tipo    | Exemplo | Descrição            |
| ---------- | ------- | ------- | -------------------- |
| `season`   | String  | `2026`  | Temporada consultada |
| `matchday` | Integer | `1`     | Rodada consultada    |

Exemplo:

```http
GET /v4/competitions/BSA/standings?season=2026&matchday=1
```

### Objetivo

Obter a classificação do Campeonato Brasileiro Série A em uma determinada rodada.

O pipeline realiza consultas por `matchday`, permitindo armazenar o histórico da classificação ao longo das rodadas do campeonato.

Os dados tratados são persistidos na tabela:

```text
tbl_standings
```

---

## 5. Estrutura da classificação

O payload do endpoint de classificação contém a propriedade:

```json
{
  "standings": []
}
```

A API retorna diferentes tipos de classificação.

Para o projeto é utilizada somente a classificação:

```json
{
  "type": "TOTAL"
}
```

Após identificar o registro do tipo `TOTAL`, a classificação dos times é obtida através de:

```text
standings[].table
```

Exemplo de um item retornado:

```json
{
  "position": 1,
  "team": {
    "id": 1769,
    "name": "SE Palmeiras",
    "shortName": "Palmeiras",
    "tla": "PAL",
    "crest": "https://crests.football-data.org/1769.png"
  },
  "playedGames": 20,
  "form": "L,W,W,W,D",
  "won": 13,
  "draw": 5,
  "lost": 2,
  "points": 44,
  "goalsFor": 34,
  "goalsAgainst": 16,
  "goalDifference": 18
}
```

---

## 6. Transformação dos dados de classificação

Para a tabela de classificação, são utilizados os seguintes dados:

| Campo da API     | Campo tratado     |
| ---------------- | ----------------- |
| `position`       | `position`        |
| `team.id`        | `team_id`         |
| `playedGames`    | `played_games`    |
| `form`           | `form`            |
| `won`            | `won`             |
| `draw`           | `draw`            |
| `lost`           | `lost`            |
| `points`         | `points`          |
| `goalsFor`       | `goals_for`       |
| `goalsAgainst`   | `goals_against`   |
| `goalDifference` | `goal_difference` |

O pipeline acrescenta também:

```text
season
gameweek
```

`season` identifica a temporada processada.

`gameweek` identifica a rodada (`matchday`) correspondente à classificação armazenada.

Os dados cadastrais do time, como nome, nome abreviado, sigla e escudo, não são duplicados em `tbl_standings`.

Essas informações permanecem centralizadas em `tbl_teams`.

---

## 7. Relacionamento dos dados

As tabelas são relacionadas através da temporada e do identificador do time:

```text
tbl_teams
    season
    team_id
       │
       │
       ▼
tbl_standings
    season
    team_id
```

A chave primária de `tbl_teams` é composta por:

```text
(season, team_id)
```

`tbl_standings` referencia essa combinação através dos campos:

```text
(season, team_id)
```

Dessa forma, os dados cadastrais dos times são mantidos em `tbl_teams`, enquanto `tbl_standings` armazena os dados históricos de classificação de cada rodada.

---

## 8. Fluxo do pipeline

O fluxo implementado na versão atual é:

```text
football-data.org
        │
        ├── /teams
        │      ↓
        │   Transform
        │      ↓
        │   Validate
        │      ↓
        │   tbl_teams
        │
        └── /standings
               ↓
            Transform
               ↓
            Validate
               ↓
          tbl_standings
```

Destino:

```text
PostgreSQL
├── tbl_teams
└── tbl_standings
```

---

## 9. Modelo de dados

O modelo físico do banco de dados está documentado separadamente através do arquivo DBML do projeto.

O modelo possui:

* `tbl_teams`: cadastro dos times participantes por temporada;
* `tbl_standings`: histórico da classificação dos times por rodada;
* relacionamento entre as tabelas através de `(season, team_id)`.

---

## 10. Observações

* O escopo atual contempla exclusivamente o **Campeonato Brasileiro Série A**.
* O código da competição utilizado pela API é `BSA`.
* A API utilizada está na versão `v4`.
* A autenticação é realizada através do Header `X-Auth-Token`.
* A API Key é configurada através de variável de ambiente e não deve ser versionada.
* Os payloads são retornados em formato JSON.
* O endpoint `/teams` fornece os times participantes da temporada.
* O endpoint `/standings` fornece a classificação para a temporada e rodada consultadas.
* A classificação utilizada pelo pipeline é do tipo `TOTAL`.
* O histórico da classificação é armazenado rodada a rodada.
* Os dados cadastrais dos times são centralizados em `tbl_teams`, evitando sua duplicação em `tbl_standings`.
