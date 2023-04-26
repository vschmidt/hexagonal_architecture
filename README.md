# Python Hagonal Architecture Template

## :coffee: Introduction

This Test API was created to solve a fake business rule using Hexagonal Architecture.

## :octopus: Run with Docker Compose

### 1. Run Docker compose

- If necessary, set environment variables like `docker compose up -d`
- Run `docker exec api python3 -m alembic upgrade head` command to perform migrations
- Access the docs from `127.0.0.1:8000/docs`

## :office: Run on HOST machine

### 1. Infrastructure Requirements

- You need a postgres server running

### 2. Install requirements

- Install pipenv: `pip install pipenv`
- Install requirements: `pipenv install --dev`
- If necessary, set environment variables like `app/settings/environment.py`
- Run `alembic upgrade head` command to perform migrations

### 2. Run app

- Start `pipenv run uvicorn main:app --host 0.0.0.0 --port 80 --reload` file.
- It runs an uvicorn server at `127.0.0.1:8000`
- Access the docs from `127.0.0.1:8000/docs`

## :bug: Run Tests

To run the tests just follow the steps:

- Run `pip install -r requirements/test.txt` command
- Run `pytest` command

## :twisted_rightwards_arrows: Run Migrations

### Add new migration

- Add/Remove import model in `src\infrastructure\postgres\metadata_agregation.py` file
- Run `alembic revision --autogenerate -m "my_migration_name"` command

### Upgrade migration

- Run `alembic upgrade head` command
- Alternative, you can upgrate by steps with `alembic upgrade +1`

### Downgrade migration

- Run `alembic downgrade -1` command

# Latest releases

- v0.0.1 - First Release
