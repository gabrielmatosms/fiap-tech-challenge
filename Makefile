COMPOSE = docker compose
APP_RUN = $(COMPOSE) run --rm app

app-build:
	$(COMPOSE) build app

app-run:
	$(COMPOSE) up

app-down:
	$(COMPOSE) down -v

apply-migrations:
	$(APP_RUN) alembic upgrade head

generate-migration:
	$(APP_RUN) alembic revision --autogenerate
