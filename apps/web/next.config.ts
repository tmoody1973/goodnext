import type { NextConfig } from "next";

// Decision 008: the site and the API share one hostname. In production a
// path rule at the edge sends /api/* to the API. In development the Next dev
// server does the same job; the rewrite is defined only then because
// `output: "export"` warns about rewrites at build time.
const isDev = process.env.NODE_ENV === "development";
const apiOrigin = process.env.GOODNEXT_API_ORIGIN ?? "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  output: "export",
  ...(isDev
    ? {
        rewrites: async () => [
          { source: "/api/:path*", destination: `${apiOrigin}/api/:path*` },
        ],
      }
    : {}),
};

export default nextConfig;
