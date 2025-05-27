FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.7.7 /uv /uvx /bin/
WORKDIR /cloneugc

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

ENV UV_NO_SYNC=1

RUN uv run manage.py collectstatic

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "--workers", "5", "--bind", "0.0.0.0:8000", "--timeout", "120", "cloneugc.wsgi:application"]
