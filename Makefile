HOST ?= 0.0.0.0
PORT ?= 8000

.PHONY: install
install:
	@poetry install
	@poetry run alembic upgrade head

.PHONY: check_migrations
check_migrations:
	 @echo "Checking if there are any unapplied migrations..."
	 @if ! command_output=$$(poetry run alembic current | tail -n 1); then \
			 echo "ERROR: Command failed"; \
			 exit 1; \
	 fi; \
	 if ! echo $$command_output | grep -q "head"; then \
			 echo "ALERT: There are unapplied migrations! Please run: 'make migrate'"; \
			 exit 0; \
	 fi; \
	 echo "SUCCESS: No migrations to run. DB up to date!"

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

.PHONY: server
server:
	@uvicorn how2meet.main:app --reload --log-level info --port ${PORT} --host ${HOST}

.PHONY: client
client:
	@cd client && yarn dev
