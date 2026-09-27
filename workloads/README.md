# Workloads

Reusable, platform-agnostic test applications for deployment experiments.

A deployment project (a top-level directory such as `cloud-run-fastapi/`) should **not** contain its own app.
It picks one workload below and adds only the platform-specific pieces: config files, IaC, CI workflows,
and Kubernetes manifests. This keeps application code in one place while every deployment stays independent.

| Workload | Kind | Covers |
| -------- | ---- | ------ |
| [`static-site`](./static-site) | Static HTML, optional zero-dependency build | All static hosts (GitHub Pages, Cloudflare, Netlify, Vercel, S3, Firebase, Azure SWA, …) |
| [`hono-api`](./hono-api) | TypeScript web API with one entry per runtime | Node / Docker, Cloudflare Workers, Deno Deploy, Bun, AWS Lambda, Vercel Functions, Netlify Functions |
| [`fastapi-app`](./fastapi-app) | Python ASGI web API | Docker, buildpacks, Procfile platforms, AWS Lambda, Hugging Face Spaces (Docker), Kubernetes, VPS |

## How a deployment project uses a workload

Pick whichever fits the platform:

- **Root directory setting** on Git-integrated platforms (Vercel, Netlify, Cloudflare, Render, Railway):
  point it at `workloads/<name>`.
- **Docker build context**: `docker build -f workloads/<name>/Dockerfile workloads/<name>`.
- **CLI with explicit config**: e.g. `wrangler deploy --config <project>/wrangler.toml`,
  `fly deploy --config <project>/fly.toml workloads/<name>` (see each workload README).
- **Copy on build** in CI when a platform insists on a specific layout.

Do not edit a workload to fit a single platform. If an adapter is missing, add it as a new entry file
(e.g. `hono-api/src/entry/<runtime>.ts`) so other deployments are unaffected.

## Probe contract

Every workload exposes the same observable behavior so that [`tools/smoke-test.sh`](../tools/smoke-test.sh)
can verify any deployment.

### API workloads (`hono-api`, `fastapi-app`)

| Endpoint | Response |
| -------- | -------- |
| `GET /` | HTML page showing the info below |
| `GET /healthz` | `200 ok` (text/plain) |
| `GET /api/info` | JSON, see fields below |
| `GET /api/echo` | JSON with method, path, query, client IP, and request headers |
| anything else | `404` |

`/api/info` fields:

| Field | Meaning | Useful for testing |
| ----- | ------- | ------------------ |
| `workload` | `hono-api` / `fastapi-app` | Routing to the right app |
| `version` | `APP_VERSION` env var, or the built-in default | Rollouts, canary, rollback |
| `runtime` | e.g. `node 22.16.0`, `workerd`, `python 3.12.7` | Which runtime actually runs |
| `target` | `DEPLOY_TARGET` env var, or auto-detected platform | Confirm where it runs |
| `region` | Region / PoP when the platform exposes it | Multi-region, edge |
| `commit` | Git commit if the platform exposes it | Deploy traceability |
| `instance` | Instance / revision / machine identifier | Scaling, load balancing |
| `startedAt` | Time the instance handled its first request | Cold starts |
| `requestCount` | Requests served by this instance | Instance reuse |
| `now` | Server time | Clock, caching |

### Static workload (`static-site`)

| Path | Response |
| ---- | -------- |
| `GET /` | HTML page that renders `info.json` |
| `GET /info.json` | JSON with `workload`, `version`, `target`, `commit`, `builtAt` (written at build time) |
| unknown path | `404`, served from `404.html` where the host supports it |

### Environment variables

All optional. Explicit values always win over auto-detection.

| Variable | Purpose |
| -------- | ------- |
| `PORT` | Listening port for server entries (default differs per entry; see each README) |
| `DEPLOY_TARGET` | Name of the deployment, e.g. `cloud-run`, `fly`, `k3s-hetzner` |
| `APP_VERSION` | Version string shown in `/api/info` |
| `GIT_COMMIT` | Commit SHA, when the platform does not provide one |
| `REGION` | Region, when the platform does not provide one |

Auto-detection (best effort; set `DEPLOY_TARGET` to be explicit):

| Field | Checked environment variables (first match wins) |
| ----- | ------------------------------------------------ |
| `target` | `AWS_LAMBDA_FUNCTION_NAME`→aws-lambda, `ECS_CONTAINER_METADATA_URI_V4`→aws-ecs, `VERCEL`→vercel, `NETLIFY`→netlify, `RENDER`→render, `FLY_APP_NAME`→fly, `RAILWAY_ENVIRONMENT`→railway, `K_SERVICE`→cloud-run, `GAE_SERVICE`→app-engine, `CONTAINER_APP_NAME`→azure-container-apps, `FUNCTIONS_WORKER_RUNTIME`→azure-functions, `WEBSITE_SITE_NAME`→azure-app-service, `SPACE_ID`→huggingface-spaces, `DENO_DEPLOYMENT_ID`→deno-deploy, `DYNO`→heroku, `KUBERNETES_SERVICE_HOST`→kubernetes |
| `region` | `REGION`, `FLY_REGION`, `VERCEL_REGION`, `AWS_REGION`, `RAILWAY_REPLICA_REGION`, `REGION_NAME`, `DENO_REGION` (Cloudflare Workers: request `cf.colo`) |
| `commit` | `GIT_COMMIT`, `VERCEL_GIT_COMMIT_SHA`, `RENDER_GIT_COMMIT`, `RAILWAY_GIT_COMMIT_SHA`, `COMMIT_REF`, `SOURCE_VERSION`, `GITHUB_SHA` |
| `instance` | `FLY_MACHINE_ID`, `K_REVISION`, `AWS_LAMBDA_LOG_STREAM_NAME`, `RENDER_INSTANCE_ID`, `DYNO`, `HOSTNAME` |

Keep these lists identical across workloads when changing them.
