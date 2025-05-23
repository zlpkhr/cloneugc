FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.7.7 /uv /uvx /bin/

WORKDIR /cloneugc

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev

COPY . .

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "gunicorn", \
     "--chdir", "/cloneugc/src", \
     "--bind", "0.0.0.0:8000", \
     "config.wsgi:application"]
