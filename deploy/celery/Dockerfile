FROM python:3.13-slim

RUN --mount=type=cache,target=/var/cache/apt \
    apt update && apt install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /bin/

WORKDIR /cloneugc

ENV UV_CACHE_DIR=/root/.cache/uv

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=${UV_CACHE_DIR} uv sync --frozen --no-dev --no-install-project --compile-bytecode

COPY . .
RUN --mount=type=cache,target=${UV_CACHE_DIR} uv sync --frozen --no-dev --no-editable --compile-bytecode

CMD ["uv", "run", "--no-sync", "celery", "--app=cloneugc", "worker", "--loglevel=info"]
