FROM python:3.13-slim

RUN apt update && \
    apt install -y ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /uvx /bin/

WORKDIR /cloneugc

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --compile

COPY --chown=1000:1000 . .
RUN uv sync --frozen --no-dev --no-editable --compile

WORKDIR /cloneugc/cloneugc

USER 1000

CMD ["uv", "run", "--no-sync", "celery", "--app=cloneugc", "worker", "--loglevel=INFO"]
