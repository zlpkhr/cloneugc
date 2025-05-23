FROM oven/bun:1.2.14-slim AS build
WORKDIR /cloneugc

COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun run build:css && bun run build:js

FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.7.7 /uv /uvx /bin/

WORKDIR /cloneugc

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev

COPY . .
COPY --from=build /cloneugc/src/static/dist/ ./src/static/dist/

EXPOSE 8000

RUN uv run --no-sync manage.py collectstatic --clear --noinput

CMD ["uv", "run", "--no-sync", "gunicorn", \
     "--chdir", "/cloneugc/src", \
     "--bind", "0.0.0.0:8000", \
     "config.wsgi:application"]
