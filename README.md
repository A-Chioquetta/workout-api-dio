# Workout API 🏋️‍♀️

API REST para gerenciamento de **atletas**, **categorias** e **centros de treinamento**, desenvolvida como desafio de projeto da DIO no bootcamp  **Luizalabs - Back-end com Python**.

A API foi construída com **FastAPI**, **SQLAlchemy 2 (async)**, **PostgreSQL**, **Alembic** para migrações e **Poetry** para gerenciamento de dependências.  
Também inclui **paginação** com `fastapi-pagination` e validações de dados com **Pydantic v2**.

---

## ✨ Funcionalidades

- CRUD de **Atletas**
  - Cadastro de atleta com:
    - Nome, CPF (único), idade, peso, altura, sexo
    - Categoria associada
    - Centro de treinamento associado
  - Atualização parcial (`PATCH`)
- CRUD de **Categorias**
- CRUD de **Centros de Treinamento**
- **Busca de atletas com filtros**:
  - Por **ID** ou **CPF** (`/atletas/search`)
- **Paginação** em listagens (limit/offset) com `fastapi-pagination`

---

## 🛠️ Stack 

- **Linguagem**: Python `>= 3.12, < 4.0`
- **Framework web**: [FastAPI](https://fastapi.tiangolo.com/)
- **Banco de dados**: PostgreSQL
- **ORM**: SQLAlchemy 2 (modo assíncrono)
- **Migrações**: Alembic
- **Validação**: Pydantic v2
- **Gerenciador de dependências**: Poetry
- **Paginação**: fastapi-pagination (`LimitOffsetPage`)
- **Servidor ASGI**: Uvicorn
- **Containers**: Docker / Docker Compose

---

## 📁 Estrutura do Projeto
```bash
workout-api/
├── workout_api/
│   ├── atleta/
│   ├── categorias/
│   ├── centro_treinamento/
│   ├── contrib/
│   ├── configs/
│   ├── routers.py
│   └── main.py
├── alembic/
├── pyproject.toml
├── docker-compose.yml
└── README.md
```

## 📌 Pré-requisitos

- Python 3.12+
- Poetry
- Docker (opcional)
- PostgreSQL (caso não use Docker)


## 📚 Principais EndPoints

### Atletas
- POST /atletas/
- GET /atletas/           → paginado
- GET /atletas/search     → buscar por ID ou CPF
- PATCH /atletas/{id}
- DELETE /atletas/{id}

### Categorias
- POST /categorias/
- GET /categorias/
- GET /categorias/{id}
- PUT /categorias/{id}
- DELETE /categorias/{id}

### Centros de Treinamento
- POST /centros-treinamento/
- GET /centros-treinamento/
- GET /centros-treinamento/{id}
- PUT /centros-treinamento/{id}
- DELETE /centros-treinamento/{id}

## 📄 Sobre o projeto
Este repositório faz parte de um desafio da DIO em parceria com a Luiza Labs para prática de FastAPI com banco de dados, migrações, validações e boas práticas backend.
