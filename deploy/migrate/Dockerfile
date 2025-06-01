FROM python:3.13

COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /bin/

WORKDIR /cloneugc

ENV UV_CACHE_DIR=/root/.cache/uv

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=${UV_CACHE_DIR} uv sync --frozen --no-dev --no-install-project --compile-bytecode

COPY . .
RUN --mount=type=cache,target=${UV_CACHE_DIR} uv sync --frozen --no-dev --no-editable --compile-bytecode

CMD ["uv", "run", "--no-sync", "manage.py", "migrate", "--noinput"]
