# GoodNext single container (decision 008): FastAPI serves /api/* and the static
# site at /. Build from the repo root so the web export and the shared
# help_routes.json are in the context.
#
#   docker build -t goodnext-web .

# 1. Build the static site (Next.js static export -> apps/web/out).
FROM node:22-slim AS web
RUN corepack enable
WORKDIR /web
COPY apps/web/ ./
RUN pnpm install --frozen-lockfile && pnpm build

# 2. The API image. Serves the site and bridges to the AgentCore runtime.
FROM python:3.12-slim AS api
WORKDIR /srv
RUN pip install --no-cache-dir uv
COPY services/api/pyproject.toml services/api/uv.lock ./
RUN uv export --frozen --no-dev --no-emit-project --format requirements-txt -o requirements.txt \
  && pip install --no-cache-dir -r requirements.txt
COPY services/api/goodnext_api ./goodnext_api
COPY --from=web /web/out ./web
# Decision 009: the API reads the same reviewed help routes the agent reads.
COPY app/goodnext/help_routes.json ./help_routes.json
ENV GOODNEXT_WEB_ROOT=/srv/web \
    GOODNEXT_HELP_ROUTES_FILE=/srv/help_routes.json
EXPOSE 8000
CMD ["uvicorn", "goodnext_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
