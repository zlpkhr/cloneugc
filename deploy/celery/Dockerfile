FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.7.7 /uv /uvx /bin/

WORKDIR /cloneugc

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev

COPY . .

ENV PYTHONPATH=src

CMD ["uv", "run", "--no-sync", "celery", "-A", "config", "worker", "--loglevel=info"]
