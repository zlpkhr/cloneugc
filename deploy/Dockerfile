FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /bin/

WORKDIR /cloneugc

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

RUN uv run --no-sync manage.py collectstatic --noinput

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "gunicorn", "--bind", "0.0.0.0:8000", "cloneugc.wsgi:application"]
