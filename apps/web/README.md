# GoodNext website

The Food today screen. Next.js 16 static export, Tailwind 4, pnpm.

```bash
pnpm install
pnpm dev          # http://localhost:3000, proxies /api/* to http://127.0.0.1:8000
pnpm test         # Vitest render tests and the never-list scan
pnpm typecheck
pnpm build        # static files in out/
```

The API must be running for a real plan: see the repo `HANDOFF.md` ("Local
dev"). Set `GOODNEXT_API_ORIGIN` if the API is not on port 8000. The demo
clock is set on the API, not here.

The site and the API share one hostname (decision 008): browser code only
calls the relative path `/api/plans`.
