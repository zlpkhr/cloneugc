.PHONY: dev dev-django dev-css dev-js

dev:
	@make dev-css & \
	make dev-js & \
	make dev-django

dev-django:
	uv run manage.py runserver

dev-css:
	bun run dev:css > /dev/null 2>&1

dev-js:
	bun run dev:js > /dev/null 2>&1

celery:
	PYTHONPATH=src celery -A config worker -l INFO