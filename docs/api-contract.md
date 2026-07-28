# API Contract — football-data.org

## 1. Objetivo

A API football-data.org será utilizada como fonte oficial de dados do projeto
`football-etl`.

---

## 2. Configuração da API

| Propriedade | Valor |
|-------------|-------|
| Provider | football-data.org |
| Base URL | `https://api.football-data.org` |
| API Version | `v4` |
| Response Format | `JSON` |
| HTTP Method | `GET` |

---

## 3. Autenticação

A API utiliza autenticação por API Key enviada através de um Header HTTP.

### Header obrigatório

| Header | Valor |
|---------|-------|
| `X-Auth-Token` | API Key |

Exemplo:

```http
X-Auth-Token: YOUR_API_TOKEN
```

A API Key não deve ser armazenada no código-fonte. Ela será configurada por
variável de ambiente.

---

## 4. Endpoints validados

### Listar competições

```http
GET /v4/competitions
```

Status obtido no Postman:

```text
HTTP 200 OK
```

Objetivo:

Listar todas as competições disponíveis.

---

### Classificação do Campeonato Brasileiro Série A

```http
GET /v4/competitions/BSA/standings?season=2026
```

Status obtido no Postman:

```text
HTTP 200 OK
```

Objetivo:

Obter a classificação do Campeonato Brasileiro Série A da temporada de 2026.

---

## 5. Estrutura do retorno

### Endpoint

```http
GET /v4/competitions
```

Principais campos identificados:

- id
- name
- code
- type
- area
- currentSeason
- lastUpdated

---

### Endpoint

```http
GET /v4/competitions/BSA/standings?season=2026
```

Estrutura simplificada:

```text
competition
season
standings[]
    └── table[]
            ├── position
            ├── team
            ├── playedGames
            ├── won
            ├── draw
            ├── lost
            ├── points
            ├── goalsFor
            ├── goalsAgainst
            └── goalDifference
```

Observação:

A classificação dos clubes encontra-se na coleção `standings[].table`.

---

## 6. Observações

- A API utiliza a versão `v4`.
- A autenticação é realizada através do Header `X-Auth-Token`.
- Os endpoints foram validados com sucesso no Postman.
- Os payloads retornam dados em formato JSON.