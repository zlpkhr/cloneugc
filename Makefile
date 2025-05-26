.PHONY: dev celery ngrok fmt

dev:
	bun run postcss ./static/*.css -u @tailwindcss/postcss -d ./static/dist -w > /dev/null 2>&1 & \
	uv run manage.py runserver

celery:
	uv run celery -A config worker -l INFO

ngrok:
	ngrok http --url=main-flounder-genuine.ngrok-free.app 8000

fmt:
	bun run prettier --write ./**/*.{js,css}
	uv run ruff format
	uv run ruff check --fix
