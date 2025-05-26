.PHONY: dev shell celery ngrok fmt

install:
	uv sync --frozen
	bun install --frozen-lockfile

dev:
	docker compose up -d
	bun run postcss ./static/*.css -u @tailwindcss/postcss -d ./static/dist -w > /dev/null 2>&1 & \
	uv run manage.py runserver

shell:
	uv run manage.py shell

celery:
	uv run celery -A config worker -l INFO

fmt:
	bun run prettier --write ./**/*.{js,css}
	uv run ruff format
	uv run ruff check --fix

ngrok:
	ngrok http --url=main-flounder-genuine.ngrok-free.app 8000
