# Usage: make makemigrations MSG="migration name"
.PHONY: makemigrations
makemigrations:
	@poetry run alembic revision --autogenerate -m "$(MSG)"

.PHONY: install
install:
	@poetry install
	@poetry run alembic upgrade head


.PHONY: run_server
run_server:
	@uvicorn how2meet.main:app --reload --log-level info --port ${PORT} --host ${HOST}
