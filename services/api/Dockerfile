# GoodNext: one container serves the static site at / and the API at /api/* (decisions 008, 012).
# Build from the repo root:  docker build -f services/api/Dockerfile .

# Stage 1: the Next.js static export (apps/web/out). corepack reads the pnpm version from package.json.
FROM node:22-alpine AS web
RUN corepack enable
WORKDIR /web
COPY apps/web/package.json apps/web/pnpm-lock.yaml apps/web/pnpm-workspace.yaml ./
RUN --mount=type=cache,id=pnpm,target=/root/.local/share/pnpm/store pnpm install --frozen-lockfile
COPY apps/web/ ./
# The web type-check reads two live-run envelopes from docs/evidence (fixture tests, MOO-777/778).
COPY docs/evidence/*.json /docs/evidence/
RUN pnpm build

# Stage 2: FastAPI with the site files and the reviewed help routes (decision 009), nothing else.
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=/opt/venv
WORKDIR /srv
COPY services/api/pyproject.toml services/api/uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-install-project
COPY services/api/goodnext_api ./goodnext_api
COPY app/goodnext/help_routes.json /srv/data/help_routes.json
COPY --from=web /web/out /srv/site
ENV GOODNEXT_HELP_ROUTES_FILE=/srv/data/help_routes.json \
    GOODNEXT_STATIC_DIR=/srv/site \
    PATH="/opt/venv/bin:$PATH"
EXPOSE 8000
# forwarded-allow-ips: trust X-Forwarded-Proto from the load balancer so the session cookie
# is Secure exactly when the visitor arrived over HTTPS. The task's security group admits
# only the balancer, so no one else can set that header.
CMD ["uvicorn", "goodnext_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
