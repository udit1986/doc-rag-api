
# Document RAG API

- [Document RAG API](#document-rag-api)
  - [Quickstart](#quickstart)
    - [1. Clone repository](#1-clone-repository)
    - [2. Install dependecies with Poetry](#2-install-dependecies-with-poetry)
    - [3. Setup database and migrations](#3-setup-database-and-migrations)
    - [4. Now you can run app](#4-now-you-can-run-app)
    - [5. Running tests](#6-running-tests)
  - [Step by step example - POST and GET endpoints](#step-by-step-example---post-and-get-endpoints)
  - [Design](#design)
    - [Deployment strategies - via Docker image](#deployment-strategies---via-docker-image)
    - [Docs URL](#docs-url)



## Quickstart

### 1. Clone repository

```bash
git clone repo_name
```

### 2. Install dependencies with [Poetry](https://python-poetry.org/docs/)

```bash
cd your_project_name

### Poetry install (python3.13)
poetry install
```

### 3. Setup database and migrations

```bash
### Setup database
docker-compose up -d

### Run Alembic migrations
poetry run alembic upgrade head
```

### 4. Now you can run app

```bash
### And this is it:
poetry run uvicorn app.main:app --reload

```

### 5. Running tests

Note, it will create databases for session and run tests in many processes by default (using pytest-xdist) to speed up execution, based on how many CPU are available in environment.

For more details about initial database setup, see logic `app/tests/conftest.py` file, `fixture_setup_new_test_database` function.

Moreover, there is coverage pytest plugin with required code coverage level 100%.

```bash
# see all pytest configuration flags in pyproject.toml
pytest
```

<br>


## POST and GET endpoints

I have created three endpoints:

- `POST` endpoint `/documents/ingest` for uploading documents
- `GET` endpoint `/documents/select` for selecting document
- `POST` endpoint `/documents/chat` for asking question from particular document.

## Design

### Deployment strategies - via Docker image

This repo has included `Dockerfile` with [Uvicorn](https://www.uvicorn.org/) webserver, because it's simple and just for showcase purposes, with direct relation to FastAPI and great ease of configuration. You should be able to run container(s) (over :8000 port) and then need to setup the proxy, loadbalancer, with https enabled, so the app stays behind it.

### Docs URL

There are some **opinionated** default settings in `/app/main.py` for documentation, CORS and allowed hosts.

1. Docs

    ```python
    app = FastAPI(
        title="Document RAG API",
        version="0.1.0",
        description="DOC-RAG-API",
        openapi_url="/openapi.json",
        docs_url="/",
    )
    ```

   Docs page is simply `/docs`.
