FROM python:3.13-slim

RUN apt update && apt install -y --no-install-recommends ffmpeg

COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /bin/

WORKDIR /cloneugc

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

CMD ["uv", "run", "--no-sync", "celery", "--app=cloneugc", "worker", "--loglevel=info"]
