FROM oven/bun:1.2.14-slim AS build
WORKDIR /cloneugc

COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun run postcss ./static/*.css -u @tailwindcss/postcss -d ./static/dist

FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.7.7 /uv /uvx /bin/
WORKDIR /cloneugc

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .
COPY --from=build /cloneugc/static/dist/ ./static/dist/

ENV UV_NO_SYNC=1

RUN uv run manage.py collectstatic

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "--workers", "5", "--bind", "0.0.0.0:8000", "--timeout", "120", "config.wsgi:application"]
