.PHONY: dev shell celery ngrok fmt

install:
	uv sync --frozen
	bun install --frozen-lockfile

dev:
	docker compose up -d
	uv run manage.py runserver

shell:
	uv run manage.py shell

celery:
	uv run celery -A cloneugc worker -l INFO

fmt:
	uv run ruff format
	uv run ruff check --fix

ngrok:
	ngrok http --url=main-flounder-genuine.ngrok-free.app 8000
