FROM oven/bun:1.2.14-slim AS assets

WORKDIR /cloneugc

COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun run build

FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /uvx /bin/

WORKDIR /cloneugc

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --compile

COPY . .
RUN uv sync --frozen --no-dev --no-editable --compile

COPY --from=assets /cloneugc/static/dist ./static/dist

RUN uv run --no-sync manage.py collectstatic --noinput

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "gunicorn", "--bind", "0.0.0.0:8000", "cloneugc.wsgi:application"]
