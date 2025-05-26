.PHONY: dev dev-django dev-css

dev:
	@make dev-css & \
	make dev-django

dev-django:
	uv run manage.py runserver

dev-css:
	bun run dev:css > /dev/null 2>&1

celery:
	uv run celery -A config worker -l INFO