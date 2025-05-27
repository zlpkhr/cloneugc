FROM oven/bun:1.2.14-slim AS build
WORKDIR /cloneugc

COPY package.json bun.lock ./
COPY ./site/package.json ./site/package.json
RUN bun install --frozen-lockfile

COPY ./site/ ./site/
RUN bun run --filter=cloneugc-site build
