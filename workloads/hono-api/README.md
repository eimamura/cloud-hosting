# hono-api

TypeScript web API built with [Hono](https://hono.dev). One shared app (`src/app.ts`) and one thin entry file per
runtime, so the same code can be deployed to servers, containers, serverless functions, and edge runtimes.

## Layout

```
src/
  app.ts               # Routes (probe contract)
  info.ts              # Environment detection
  entry/
    node.ts            # Node.js server  -> Docker, container PaaS, VPS, Kubernetes
    cloudflare.ts      # Cloudflare Workers
    deno.ts            # Deno / Deno Deploy
    bun.ts             # Bun
    aws-lambda.ts      # AWS Lambda (API Gateway, Function URL, ALB)
    vercel.ts          # Vercel Functions
    netlify.ts         # Netlify Functions (v2)
Dockerfile             # Node.js server image
deno.json              # Import map for Deno
```

## Local development

```bash
npm install
npm run dev            # Node.js server with reload on http://localhost:8080
npm run typecheck
npm run build          # dist/node.mjs and dist/aws-lambda.mjs (single-file bundles)
```

## Entry points by platform

| Platform | Entry | How to wire it up in a deployment project |
| -------- | ----- | ----------------------------------------- |
| Docker / Cloud Run / Fly.io / Render / Railway / Azure Container Apps / Kubernetes / VPS | `node.ts` | Build `Dockerfile` with this directory as context. Listens on `PORT` (default 8080). |
| Container PaaS without Docker (buildpacks, Nixpacks) | `node.ts` | Build command `npm ci && npm run build`, start command `npm start`. |
| Cloudflare Workers | `cloudflare.ts` | `wrangler.toml` with `main = "<path>/workloads/hono-api/src/entry/cloudflare.ts"`. |
| Deno Deploy | `deno.ts` | Entrypoint `workloads/hono-api/src/entry/deno.ts`. Default port 8000 locally. |
| Bun | `bun.ts` | `bun run src/entry/bun.ts`. Default port 3000. |
| AWS Lambda | `aws-lambda.ts` | Deploy `dist/aws-lambda.mjs` (after `npm run build:lambda`), handler `aws-lambda.handler`, Node.js 20+ runtime. |
| Vercel Functions | `vercel.ts` | `api/[[...route]].ts` containing `export * from "<path>/src/entry/vercel.ts"`, plus a rewrite of `/(.*)` to `/api/$1`. |
| Netlify Functions | `netlify.ts` | `netlify/functions/api.ts` containing `export { default, config } from "<path>/src/entry/netlify.ts"`. |

Verified locally: Node server, Docker image, Lambda handler (invoked with a Function URL event),
and Cloudflare Workers (`wrangler dev`). Bun, Vercel, and Netlify entries are type-checked only;
the Deno entry is excluded from `tsc` and has not been run yet.

See [../README.md](../README.md) for the probe contract and environment variables.
