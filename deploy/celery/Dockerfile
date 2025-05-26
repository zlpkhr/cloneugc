FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.7.7 /uv /uvx /bin/
WORKDIR /cloneugc

RUN apt update && apt install -y --no-install-recommends ffmpeg

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev

COPY . .

ENV UV_NO_SYNC=1

CMD ["uv", "run", "celery", "-A", "config", "worker", "--loglevel=info"]
