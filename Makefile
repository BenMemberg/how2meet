HOST ?= 0.0.0.0
PORT ?= 8000

.PHONY: install
install:
	@poetry install
	@poetry run alembic upgrade head

.PHONY: migrate
migrate:
	@poetry run alembic upgrade head

.PHONY: reset-db
reset-db:
	@poetry run alembic downgrade base

# USAGE: make makemigrations MSG="migration name"
.PHONY: create_migration
create_migration:
	@poetry run alembic revision --autogenerate -m "$(MSG)"

.PHONY: run_server
run_server:
	@uvicorn how2meet.main:app --reload --log-level info --port ${PORT} --host ${HOST}
