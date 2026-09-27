# Hosting Candidates and Deployment Methods

A catalog of hosting targets and deployment techniques to experiment with in this workspace:
a recommended order for trying them, complexity, usage domain and popularity, commercial-use terms,
and a record of what has actually been tried.

> Free tiers, pricing, and product availability change often. Treat the "Free tier" column as a hint
> and check the provider's current terms before starting a project. Pricing last checked: 2026-09-27 (section 3).

## Legend

**Free tier**: ✅ usable free tier · 🟡 limited / trial credits / sleeps when idle · ❌ paid only · ⛔ closed to new customers

**Complexity** (effort to get a first deploy working):

| Level | Meaning |
| ----- | ------- |
| ★☆☆☆☆ | Minutes. Sign in, connect repo or run one CLI command. |
| ★★☆☆☆ | An hour or so. A config file, a Dockerfile, or a small platform-specific setup. |
| ★★★☆☆ | Cloud account setup: IAM / permissions, registries, custom domains, CI credentials. |
| ★★★★☆ | IaC defining many resources: networking, load balancers, databases, secrets. |
| ★★★★★ | You operate the platform yourself: clusters, servers, upgrades, TLS, monitoring. |

**Tried**: ⬜ not tried · 🔄 in progress · ✅ done (link the project directory) · ⏭ skipped (note why)

When the status of an experiment changes, update both the roadmap (section 1) and the matching row in the
catalog (section 2).

---

## 1. Roadmap (recommended order)

Ordered so that each step introduces roughly one new concept on top of the previous ones:
static → framework PaaS → containers → serverless + IaC → self-managed → orchestration.

Every row reuses one of the shared [workloads](../workloads/README.md), so each experiment only adds
platform-specific files. Verify each deployment with `tools/smoke-test.sh`.

| # | Project idea | Workload (entry) | Hosting | Method | Complexity | What you learn | Tried | Project dir |
| - | ------------ | ---------------- | ------- | ------ | ---------- | -------------- | ----- | ----------- |
| 1 | Root entry page | root `index.html` | GitHub Pages | GitHub Actions | ★☆☆☆☆ | Actions workflow, Pages artifacts | ✅ 2026-09-27 | [github-pages](../github-pages) |
| 2 | Static site | `static-site` | Cloudflare Workers Static Assets | `wrangler` CLI, then Git integration | ★☆☆☆☆ | CLI deploy vs Git deploy, edge CDN | ⬜ | |
| 3 | Serverless API + previews | `hono-api` (vercel) | Vercel | Git integration + preview deploys | ★☆☆☆☆ | Preview environments, instant rollback | ⬜ | |
| 4 | Edge API | `hono-api` (deno) | Deno Deploy | Git integration | ★☆☆☆☆ | Deno runtime, edge deploy | ⬜ | |
| 5 | Python API | `fastapi-app` | Render | Git integration + `render.yaml` | ★★☆☆☆ | Blueprint config, idle sleep | ⬜ | |
| 6 | Edge API | `hono-api` (cloudflare) | Cloudflare Workers | `wrangler deploy` | ★★☆☆☆ | Isolates, PoPs (`region` = colo), versions | ⬜ | |
| 7 | Container | `hono-api` (Dockerfile) | Fly.io | `fly deploy` | ★★☆☆☆ | Dockerfile, micro-VMs, multi-region (paid, from ~$4/mo) | ⬜ | |
| 8 | Python API from source | `fastapi-app` | Google Cloud Run | Buildpacks via `gcloud run deploy --source` | ★★☆☆☆ | Buildpacks, scale to zero, revisions / traffic split | ⬜ | |
| 9 | Git-remote deploy | `fastapi-app` (Dockerfile) | Hugging Face Spaces | Git push | ★☆☆☆☆ | Git-remote deploy, Docker Spaces | ⬜ | |
| 10 | Node function | `hono-api` (aws-lambda) | AWS Lambda + Function URL | Terraform + GitHub Actions OIDC | ★★★☆☆ | Terraform state, IAM, keyless CI auth | ⬜ | |
| 11 | Python function | `fastapi-app` (ASGI adapter) | Azure Functions | Bicep + `func` CLI | ★★★☆☆ | Azure resource model, Bicep | ⬜ | |
| 12 | Zero-downtime Docker | `hono-api` (Dockerfile) | Hetzner VPS | Kamal | ★★★☆☆ | SSH deploys, registry, proxy, TLS | ⬜ | |
| 13 | Self-hosted PaaS | `fastapi-app` (Dockerfile) | Coolify on Oracle Always Free VM | Git push via Coolify | ★★★★☆ | Running your own PaaS | ⬜ | |
| 14 | Containers on AWS | `hono-api` (Dockerfile) | ECS Fargate + ALB | AWS CDK | ★★★★☆ | VPC, ALB, task definitions, secrets | ⬜ | |
| 15 | Kubernetes GitOps | `hono-api` + `fastapi-app` | k3s on VPS or GKE Autopilot | Helm + Argo CD | ★★★★★ | Manifests, ingress routing to two services, GitOps sync | ⬜ | |

Framework-specific SSR (e.g. Next.js on Vercel / Amplify) and databases (D1, RDS, Neon) are intentionally left out
of the workloads. Add them as new workloads only when an experiment needs them.

---

## 2. Hosting catalog

Columns: **Rec** = recommendation for this workspace (★★★ try first · ★★ worth trying · ★ optional / niche).
Rows within each table are sorted by recommendation.

### 2.1 Static site hosting

Best for: SPA, SSG output, plain HTML (including this repo's `index.html`).

| Provider | Rec | Complexity | Free tier | Typical deploy | Notes | Tried |
| -------- | --- | ---------- | --------- | -------------- | ----- | ----- |
| GitHub Pages | ★★★ | ★☆☆☆☆ | ✅ | GitHub Actions / branch publish | Static only. Simplest option for the root entry page. | ✅ [github-pages](../github-pages) |
| Cloudflare Pages / Workers Static Assets | ★★★ | ★☆☆☆☆ | ✅ | Git integration, `wrangler` CLI | Cloudflare is steering new projects toward Workers with static assets. | ⬜ |
| Netlify | ★★ | ★☆☆☆☆ | ✅ | Git integration, `netlify` CLI | Preview deploys per PR, forms, redirects. | ⬜ |
| AWS S3 + CloudFront | ★★ | ★★★☆☆ | 🟡 | CLI / IaC | Good exercise for IaC (bucket, OAC, distribution, ACM cert). | ⬜ |
| Firebase Hosting | ★★ | ★☆☆☆☆ | ✅ | `firebase deploy` | Preview channels, CDN. | ⬜ |
| Azure Static Web Apps | ★★ | ★★☆☆☆ | ✅ | GitHub Actions (auto-generated) | Built-in Functions API backend. | ⬜ |
| Vercel | ★ | ★☆☆☆☆ | ✅ | Git integration, `vercel` CLI | Hobby plan is for non-commercial use. Better used for SSR (2.2). | ⬜ |
| GitLab Pages | ★ | ★☆☆☆☆ | ✅ | GitLab CI (`pages` job) | Requires a GitLab mirror of the repo. | ⬜ |
| Render Static Sites | ★ | ★☆☆☆☆ | ✅ | Git integration | | ⬜ |
| Google Cloud Storage + Cloud CDN / LB | ★ | ★★★☆☆ | 🟡 | `gcloud` / IaC | Load balancer has a baseline cost. | ⬜ |
| Surge | ★ | ★☆☆☆☆ | ✅ | `surge` CLI | One-command deploy, minimal features. | ⬜ |

### 2.2 Frontend / full-stack platforms (framework-aware PaaS)

Best for: Next.js, Nuxt, SvelteKit, Astro, Remix with SSR.

| Provider | Rec | Complexity | Free tier | Typical deploy | Notes | Tried |
| -------- | --- | ---------- | --------- | -------------- | ----- | ----- |
| Vercel | ★★★ | ★☆☆☆☆ | ✅ | Git integration, `vercel` CLI | First-class Next.js; Functions + Edge runtime. | ⬜ |
| Cloudflare Workers (OpenNext / framework adapters) | ★★ | ★★☆☆☆ | ✅ | `wrangler deploy` | SSR at the edge; Node.js compatibility flags. | ⬜ |
| Netlify | ★★ | ★☆☆☆☆ | ✅ | Git integration, `netlify` CLI | Framework adapters, Netlify Functions / Edge Functions. | ⬜ |
| AWS Amplify Hosting | ★★ | ★★☆☆☆ | 🟡 | Git integration | SSR support for Next.js on AWS. | ⬜ |
| SST (on your AWS account) | ★★ | ★★★☆☆ | 🟡 | `sst deploy` | IaC-driven framework deployments to AWS. | ⬜ |
| Firebase App Hosting | ★ | ★★☆☆☆ | 🟡 | Git integration | Next.js / Angular SSR on Cloud Run under the hood. Requires Blaze plan. | ⬜ |
| Azure Static Web Apps (hybrid) | ★ | ★★☆☆☆ | ✅ | GitHub Actions | Next.js hybrid rendering support. | ⬜ |

### 2.3 Serverless functions / edge runtimes

Best for: APIs, webhooks, lightweight backends.

| Provider | Rec | Complexity | Free tier | Runtimes | Typical deploy | Notes | Tried |
| -------- | --- | ---------- | --------- | -------- | -------------- | ----- | ----- |
| Cloudflare Workers | ★★★ | ★☆☆☆☆ | ✅ | JS/TS, Python (beta), Wasm | `wrangler deploy` | V8 isolates, KV / D1 / R2 / Durable Objects. | ⬜ |
| AWS Lambda (+ API Gateway / Function URL) | ★★★ | ★★★☆☆ | ✅ | Node, Python, container images, others | SAM, CDK, Serverless Framework, Terraform | Function URLs avoid API Gateway setup. | ⬜ |
| Azure Functions | ★★ | ★★★☆☆ | ✅ | Node, Python, .NET, others | `func` CLI, VS Code, Actions | Flex Consumption plan. | ⬜ |
| Google Cloud Run functions | ★★ | ★★☆☆☆ | ✅ | Node, Python, Go, others | `gcloud functions deploy` | Formerly Cloud Functions; runs on Cloud Run. | ⬜ |
| Deno Deploy | ★★ | ★☆☆☆☆ | ✅ | Deno / TS | Git integration, `deployctl` / `deno deploy` | | ⬜ |
| Vercel Functions | ★ | ★☆☆☆☆ | ✅ | Node, Python, Edge | Git / CLI | Usually covered by the Vercel SSR experiment. | ⬜ |
| Netlify Functions | ★ | ★☆☆☆☆ | ✅ | Node, Go | Git / CLI | | ⬜ |
| Supabase Edge Functions | ★ | ★★☆☆☆ | ✅ | Deno | `supabase functions deploy` | Pairs with Supabase Postgres. | ⬜ |
| Val Town | ★ | ★☆☆☆☆ | ✅ | TS | Browser editor / CLI | Tiny scripts and HTTP endpoints. | ⬜ |

### 2.4 Container / application PaaS

Best for: long-running web servers (FastAPI, Express, Django), Dockerfiles.

| Provider | Rec | Complexity | Free tier | Typical deploy | Notes | Tried |
| -------- | --- | ---------- | --------- | -------------- | ----- | ----- |
| Google Cloud Run | ★★★ | ★★☆☆☆ | ✅ | `gcloud run deploy --source`, image push | Scale to zero, buildpacks from source. | ⬜ |
| Fly.io | ★★★ | ★★☆☆☆ | ❌ | `fly deploy` | Firecracker micro-VMs, multi-region. Short trial only, then pay-as-you-go (from $3.89/mo). | ⬜ |
| Render | ★★★ | ★☆☆☆☆ | 🟡 | Git integration, Blueprint (`render.yaml`) | Free web services sleep when idle. | ⬜ |
| Azure Container Apps | ★★ | ★★★☆☆ | ✅ | `az containerapp up`, image push | KEDA-based scaling, scale to zero. | ⬜ |
| Railway | ★★ | ★☆☆☆☆ | 🟡 | Git integration, `railway up` | Trial credits; Railpack/Nixpacks auto-build. | ⬜ |
| AWS ECS on Fargate | ★★ | ★★★★☆ | ❌ | CDK / Terraform / Copilot | Full control; needs VPC, ALB, etc. | ⬜ |
| Hugging Face Spaces | ★★ | ★☆☆☆☆ | ✅ | Git push | Gradio / Streamlit / Docker; ML demos. | ⬜ |
| Koyeb | ★ | ★☆☆☆☆ | 🟡 | Git / image / CLI | Joining Mistral AI; free tier for new users unclear. | ⬜ |
| Northflank | ★ | ★★☆☆☆ | 🟡 | Git / image | Free sandbox project. | ⬜ |
| Zeabur | ★ | ★☆☆☆☆ | 🟡 | Git integration | | ⬜ |
| DigitalOcean App Platform | ★ | ★★☆☆☆ | 🟡 | Git / image, App Spec | Free for static sites. | ⬜ |
| Azure App Service | ★ | ★★☆☆☆ | 🟡 | `az webapp up`, zip deploy, container | F1 free tier exists. | ⬜ |
| Google App Engine | ★ | ★★☆☆☆ | 🟡 | `gcloud app deploy` | Standard environment has free quotas. Legacy; prefer Cloud Run. | ⬜ |
| AWS App Runner | ★ | ★★☆☆☆ | ⛔ | Image from ECR / source repo | Closed to new customers since 2026-04-30. Use ECS Express Mode instead. | ⏭ not available |
| AWS Elastic Beanstalk | ★ | ★★★☆☆ | 🟡 | `eb deploy` | Classic PaaS on EC2. | ⬜ |
| Heroku | ★ | ★☆☆☆☆ | ❌ | `git push heroku`, container registry | Buildpacks origin; no free dynos. | ⬜ |
| Streamlit Community Cloud | ★ | ★☆☆☆☆ | ✅ | Git integration | Streamlit apps only. | ⬜ |
| PythonAnywhere | ★ | ★☆☆☆☆ | ✅ | Web UI / Git pull | WSGI apps; limited outbound network on free tier. | ⬜ |

### 2.5 Kubernetes

Best for: learning orchestration, GitOps, service meshes.

| Provider | Rec | Complexity | Free tier | Notes | Tried |
| -------- | --- | ---------- | --------- | ----- | ----- |
| kind / minikube (local) | ★★★ | ★★★☆☆ | ✅ | Local only; rehearse manifests before paying for a cluster. | ⬜ |
| k3s on a VPS | ★★★ | ★★★★★ | ❌ | Self-managed, cheapest real cluster. | ⬜ |
| GKE Autopilot | ★★ | ★★★★☆ | 🟡 | Cluster management fee credit for one cluster; pay per pod. | ⬜ |
| Azure AKS | ★ | ★★★★☆ | 🟡 | Free control plane tier; pay for nodes. | ⬜ |
| Amazon EKS / EKS Auto Mode | ★ | ★★★★★ | ❌ | Control plane fee per cluster. | ⬜ |
| DigitalOcean Kubernetes | ★ | ★★★★☆ | ❌ | Free control plane; pay for nodes. | ⬜ |
| Civo | ★ | ★★★☆☆ | 🟡 | Fast k3s clusters; trial credits. | ⬜ |

### 2.6 Virtual machines / VPS (IaaS)

Best for: self-managed deploys, Docker Compose, self-hosted PaaS.

| Provider | Rec | Complexity | Free tier | Notes | Tried |
| -------- | --- | ---------- | --------- | ----- | ----- |
| Oracle Cloud Always Free | ★★★ | ★★★☆☆ | ✅ | Arm (Ampere) 2 OCPU / 12 GB; capacity can be scarce in some regions. | ⬜ |
| Hetzner Cloud | ★★★ | ★★★☆☆ | ❌ | Very cheap, EU/US regions. | ⬜ |
| Google Compute Engine | ★★ | ★★★☆☆ | ✅ | One e2-micro in selected US regions. | ⬜ |
| AWS EC2 / Lightsail | ★★ | ★★★☆☆ | 🟡 | Up to $200 credits over 6 months for new accounts; Lightsail is flat-priced. | ⬜ |
| Azure Virtual Machines | ★ | ★★★☆☆ | 🟡 | 12-month free B1s for new accounts. | ⬜ |
| DigitalOcean Droplets | ★ | ★★★☆☆ | ❌ | | ⬜ |
| Vultr / Akamai (Linode) | ★ | ★★★☆☆ | ❌ | | ⬜ |
| Sakura Cloud / ConoHa / Xserver VPS | ★ | ★★★☆☆ | ❌ | Japan-based providers. | ⬜ |

### 2.7 Self-hosted PaaS (runs on a VPS from 2.6)

| Tool | Rec | Complexity | Notes | Tried |
| ---- | --- | ---------- | ----- | ----- |
| Kamal | ★★★ | ★★★☆☆ | Zero-downtime Docker deploys over SSH from your laptop / CI. | ⬜ |
| Coolify | ★★★ | ★★★★☆ | Web UI, Git integration, Docker/Compose, automatic TLS. | ⬜ |
| Dokku | ★★ | ★★★☆☆ | "Mini Heroku": `git push dokku`, buildpacks. | ⬜ |
| Dokploy | ★ | ★★★★☆ | Similar to Coolify; Docker Swarm based. | ⬜ |
| CapRover | ★ | ★★★★☆ | One-click apps, Docker Swarm. | ⬜ |

### 2.8 Supporting services (data, storage) — optional pairings

| Kind | Candidates (recommended first) |
| ---- | ------------------------------ |
| Postgres | Neon, Supabase, Cloud SQL, RDS / Aurora Serverless, Aiven, Azure Database for PostgreSQL |
| SQLite at the edge | Cloudflare D1, Turso (libSQL) |
| Key-value / cache | Upstash Redis, Cloudflare KV, Valkey on VPS |
| Object storage | Cloudflare R2, S3, GCS, Azure Blob, Backblaze B2 |
| Document DB | Firestore, DynamoDB, MongoDB Atlas, Cosmos DB |

---

## 3. Usage domain, popularity, commercial use, and pricing

**Popularity**: ●●● mainstream, widely known · ●●○ well known in its niche / region · ●○○ niche or emerging

**Commercial use**: ✅ allowed, including on the free tier (within quotas) · 🟡 allowed only on a paid plan, or the
free tier is not suitable for production · 💰 paid-only service, commercial use is normal

**Price**: checked against official pricing pages on **2026-09-27**. USD unless stated; AWS/GCP/Azure rates are for
us-east-1 / us-central1 / East US. Hetzner prices exclude VAT; Japanese prices include tax.
† = could not be confirmed on the official page (taken from vendor blog, docs, or third-party sources).
Sources are listed in [3.8](#38-pricing-sources-and-recent-changes).

Constraints below are summaries of each provider's terms as understood at the last review. They are not legal
advice; read the current ToS / acceptable use policy before running anything commercial.

### 3.1 Static site hosting

| Provider | Primary use domain | Popularity | Commercial use | Commercial constraints / caveats | Price (2026-09-27) |
| -------- | ------------------ | ---------- | -------------- | -------------------------------- | ------------------ |
| GitHub Pages | OSS docs, personal sites, project pages | ●●● | 🟡 | ToS: not for running an online business, e-commerce, or SaaS. Business docs / landing pages are fine. Soft limits: 1 GB site, 100 GB/month bandwidth, 10 builds/hour. No SLA. | Free for public repos. Private repos need a paid plan: Team $4/user/mo (promo, first 12 months) |
| Cloudflare Pages / Workers Static Assets | Jamstack sites, SPAs, edge apps | ●●● | ✅ | Free tier allows commercial use. Limits: 500 builds/mo, 20k files, 25 MiB/file. Heavy video/large-file delivery should use R2 / Stream. | Free; static asset requests free and unlimited. Workers Paid $5/mo minimum |
| Netlify | Jamstack sites, marketing sites, agencies | ●●● | ✅ | Free plan allows commercial use within its credit allowance; hard cap, the site is paused when credits run out. SLA only on Enterprise. | Free 300 credits/mo · Personal $9/mo (1,000 credits) · Pro $20/mo (3,000 credits, unlimited seats). Bandwidth 20 credits/GB, deploy 15 credits |
| AWS S3 + CloudFront | Enterprise static assets, media, SPAs | ●●● | 💰 | Pay-as-you-go; production-grade SLA. Watch data transfer costs. | S3 $0.023/GB-mo. CloudFront always-free 1 TB + 10M req/mo, then $0.085/GB; or flat-rate Free $0 / Pro $15/mo |
| Firebase Hosting | Mobile/web app frontends in the Google ecosystem | ●●● | ✅ | Spark (free) plan allows commercial use with storage/transfer quotas; exceeding them requires Blaze. | Spark: 10 GB storage, 360 MB/day transfer. Blaze: $0.026/GB storage, $0.15/GB transfer |
| Azure Static Web Apps | Enterprise SPAs in Microsoft shops | ●●○ | 🟡 | Free plan is intended for hobby / personal projects and stops serving when over quota; Standard plan for production (SLA, custom auth, private endpoints). | Free: 100 GB bandwidth, 250 MB app. Standard ~$9/app/mo, 100 GB incl., then ~$0.20/GB † |
| Vercel | Next.js / React sites | ●●● | 🟡 | Hobby plan is **non-commercial personal use only**. Any commercial use requires Pro or Enterprise. | Hobby $0 (100 GB transfer, 1M edge req). Pro $20/mo incl. 1 deploying seat + $20 usage credit; extra seat $20/mo |
| GitLab Pages | Docs and sites for GitLab-hosted projects | ●●○ | ✅ | Commercial use allowed; free tier CI compute minutes are limited. | Free: 400 CI min/mo, 1 GB per site. Premium $29/user/mo (annual) |
| Render Static Sites | Small teams' sites alongside Render services | ●●○ | ✅ | Free static sites allowed commercially; bandwidth is shared with the workspace. | Free on Hobby (5 GB bandwidth, then $0.15/GB). Pro workspace $25/mo flat (25 GB incl.) |
| Google Cloud Storage + Cloud CDN / LB | GCP-based enterprise static delivery | ●●○ | 💰 | Pay-as-you-go; load balancer has a fixed hourly cost. | GCS 5 GiB always free, then $0.020/GB-mo †. LB forwarding rule $0.025/hr (~$18/mo). CDN ~$0.08/GiB † |
| Surge | Quick prototypes, front-end demos | ●○○ | ✅ | Custom SSL, force HTTPS, and redirects require the paid plan. | Free (custom domain, basic SSL). Professional $30/mo |

### 3.2 Frontend / full-stack platforms

| Provider | Primary use domain | Popularity | Commercial use | Commercial constraints / caveats | Price (2026-09-27) |
| -------- | ------------------ | ---------- | -------------- | -------------------------------- | ------------------ |
| Vercel | Next.js SSR, e-commerce frontends, startups | ●●● | 🟡 | Hobby is non-commercial only; Hobby cannot buy extra usage and pauses when over limits. | Hobby $0: 1M invocations, 4 CPU-hr, 360 GB-hr. Pro $20/mo + usage (Active CPU $0.128/hr, $0.15/GB transfer) |
| Netlify | Framework SSR, agencies, content sites | ●●● | ✅ | Free tier commercial OK within credits; functions have execution time limits. | Same plans as 3.1. Compute 10 credits/GB-hr |
| Cloudflare Workers (framework adapters) | Edge SSR, global low-latency apps | ●●○ | ✅ | Free tier: 10 ms CPU per request; Paid plan needed for heavier SSR. Some Node.js APIs unsupported. | Free 100k req/day. Paid $5/mo incl. 10M req + 30M CPU-ms, then $0.30/1M req, $0.02/1M CPU-ms |
| AWS Amplify Hosting | AWS-centric teams, mobile + web | ●●○ | 💰 | Pay-as-you-go after the monthly free allowance; production use normal. | Free/mo: 1,000 build min, 15 GB served, 500k SSR req. Then $0.01/build-min, $0.15/GB, SSR $0.30/1M req |
| SST | Startups building on their own AWS account | ●●○ | 💰 | Open source tool (free); you pay AWS for resources. | Framework free. Console free up to 350 resources, then $0.086/resource |
| Firebase App Hosting | Next.js / Angular on Google Cloud | ●○○ | 💰 | Requires Blaze (pay-as-you-go) plan. | Free/mo on Blaze: 2M req, 10 GiB egress, 180k vCPU-s. Then $0.40/1M req, $0.15–0.20/GiB |
| Azure Static Web Apps (hybrid) | Enterprise Next.js on Azure | ●○○ | 🟡 | Same plan rules as 3.1; hybrid Next.js support has feature gaps. | Same as 3.1 |

### 3.3 Serverless functions / edge runtimes

| Provider | Primary use domain | Popularity | Commercial use | Commercial constraints / caveats | Price (2026-09-27) |
| -------- | ------------------ | ---------- | -------------- | -------------------------------- | ------------------ |
| Cloudflare Workers | Edge APIs, proxies, auth, A/B testing | ●●● | ✅ | Free: daily request cap and 10 ms CPU. Paid plan for production traffic and Durable Objects scale. | Free 100k req/day. Paid $5/mo incl. 10M req + 30M CPU-ms, then $0.30/1M req |
| AWS Lambda | Enterprise event-driven backends, APIs, data pipelines | ●●● | ✅ | Always-free monthly quota; beyond that pay-per-use. Cold-start (INIT) time is billed since 2025-08. | Free 1M req + 400k GB-s/mo. Then $0.20/1M req, $0.0000166667/GB-s (x86) |
| Azure Functions | Enterprise integrations, Microsoft 365 / .NET shops | ●●● | ✅ | Monthly free grant on Flex Consumption (smaller than the old Consumption plan); production common. | Free 250k exec + 100k GB-s/mo. Then $0.40/1M exec, $0.000026/GB-s |
| Google Cloud Run functions | GCP event handlers, Firebase backends | ●●○ | ✅ | Billed as Cloud Run; free monthly quota per billing account. | Free 2M req, 180k vCPU-s, 360k GiB-s/mo. Then $0.40/1M req, $0.000024/vCPU-s |
| Deno Deploy | Deno / TS APIs, edge apps, Fresh sites | ●○○ | ✅ | Free tier has request and egress limits; paid plan for production scale. | Free 1M req, 20 GiB/mo. Pro $20/mo (5M req, 200 GiB) |
| Vercel Functions | API routes for Next.js apps | ●●○ | 🟡 | Follows Vercel plan rules (Hobby non-commercial). | Pro: $0.60/1M invocations, $0.128/CPU-hr, $0.0106/GB-hr (from the $20 credit first) |
| Netlify Functions | API routes for Netlify sites | ●●○ | ✅ | Counted against Netlify credits; execution time limits. | Credits: 10/GB-hr compute, 2 per 10k req (~$0.07/GB-hr on Pro) |
| Supabase Edge Functions | Backends for Supabase apps | ●●○ | 🟡 | Free projects **pause after 1 week of inactivity**; use Pro for production. | Free: 2 projects, 500k function calls. Pro $25/mo (2M calls, then $2/1M; no pausing) |
| Val Town | Scripts, webhooks, bots, prototypes | ●○○ | 🟡 | Free plan: new vals are public only, 10 crons per val. Not aimed at high-traffic production. | Free. Pro $25/mo or $250/yr † |

### 3.4 Container / application PaaS

| Provider | Primary use domain | Popularity | Commercial use | Commercial constraints / caveats | Price (2026-09-27) |
| -------- | ------------------ | ---------- | -------------- | -------------------------------- | ------------------ |
| Google Cloud Run | Containerized APIs and web apps, startups to enterprise | ●●● | ✅ | Monthly free quota; production-grade with SLA. Cold starts when scaled to zero. | Free 2M req, 180k vCPU-s, 360k GiB-s/mo. Then $0.000024/vCPU-s, $0.0000025/GiB-s, $0.40/1M req |
| Fly.io | Global low-latency apps, Elixir/Rails/Phoenix, side projects | ●●○ | 💰 | No free allowance; trial is 2 machine-hours or 7 days. Pay-as-you-go. | shared-cpu-1x 256 MB $3.89/mo, 1 GB $15.55/mo |
| Render | Startups, Heroku replacements | ●●○ | 🟡 | Free web services spin down after 15 min idle; free Postgres expires after 30 days. **Not suitable for production.** | Free instance (512 MB, 750 hr/mo). Starter $7/mo. Pro workspace $25/mo + compute |
| Azure Container Apps | Microservices on Azure, event-driven workers | ●●○ | ✅ | Monthly free grant; production-grade. | Free 180k vCPU-s, 360k GiB-s, 2M req/mo. Then $0.000024/vCPU-s, $0.40/1M req |
| Railway | Indie hackers, prototypes, small SaaS | ●●○ | 🟡 | $5 trial for 30 days, then a Free plan with $1/mo credit (1 vCPU / 0.5 GB per service). Hobby/Pro for real use. | Hobby $5/mo (incl. $5 usage). Pro $20/mo. ~$20/vCPU-mo, $10/GB RAM-mo |
| AWS ECS on Fargate | Enterprise containerized workloads | ●●● | 💰 | No free tier for Fargate compute; ALB and NAT gateway add fixed costs. | $0.04048/vCPU-hr, $0.004445/GB-hr (x86); Arm ~20% cheaper |
| Hugging Face Spaces | ML demos, model showcases, research | ●●● (ML) | 🟡 | Free CPU Spaces sleep when idle; GPUs are paid. Respect model/dataset licenses (many are non-commercial). | CPU Basic free (2 vCPU, 16 GB). CPU Upgrade $0.03/hr. PRO $9/mo |
| Koyeb | Global serverless containers, small apps | ●○○ | 🟡 | Joining Mistral AI; free tier for new signups is unclear †. Paid plans for production. | eco-nano $1.61/mo. Pro plan $29/mo (incl. $10 credit) |
| Northflank | Dev teams wanting K8s-like features as PaaS | ●○○ | 🟡 | Free sandbox is for trying the platform (payment method required); paid for production. | Sandbox free. nf-compute-10 $2.70/mo; $0.01667/vCPU-hr |
| Zeabur | Indie developers, popular in Asia | ●○○ | 🟡 | Free plan sleeps when idle, no SLA. Shared clusters are being phased out (2026). | Free. Dev $5/mo · Pro $19/mo · Team $79/mo |
| DigitalOcean App Platform | Small businesses, startups | ●●○ | 🟡 | Free only for static sites (3 apps); paid containers for dynamic apps. | Container from $5/mo (512 MiB) |
| Azure App Service | Enterprise web apps, .NET / Java | ●●● | 🟡 | F1 free tier: 60 CPU-min/day, no SLA — dev/test only. Basic+ for production. | F1 free. B1 Linux ~$12.41/mo ($0.017/hr) |
| Google App Engine | Legacy GCP web apps | ●●○ | ✅ | Free daily quotas in Standard environment; Google now points new projects to Cloud Run. | Free 28 F-instance-hr/day. Then $0.05/instance-hr (F1) |
| AWS App Runner | Simple container web services on AWS | ●○○ | ⛔ | **Closed to new customers since 2026-04-30**; maintenance mode. AWS recommends ECS Express Mode. | $0.064/vCPU-hr + $0.007/GB-hr (existing customers only) |
| AWS Elastic Beanstalk | Legacy AWS web apps, lift-and-shift | ●●○ | 💰 | Free itself; you pay for EC2 / ELB. | EC2 t4g.micro ~$6.13/mo |
| Heroku | Rails/Node startups, legacy apps, enterprise (Salesforce) | ●●● | 💰 | No free tier; Eco dynos sleep after 30 min; Basic+ for always-on. | Eco $5/mo · Basic $7/mo · Standard-1X $25/mo |
| Streamlit Community Cloud | Data apps, internal dashboards, demos | ●●○ | 🟡 | Free and intended for sharing public apps; sleeps after 12 h without traffic. Use Snowflake / self-hosting for business-critical apps. | Free only (no paid self-serve tier) |
| PythonAnywhere | Education, beginner Python web apps | ●●○ | 🟡 | Free: one app on `*.pythonanywhere.com`, 100 CPU-s/day, restricted outbound internet. Paid plans for custom domains and production. | Free. Developer $10/mo (custom domain, SSH) |

⛔ = not available to new customers.

### 3.5 Kubernetes

| Provider | Primary use domain | Popularity | Commercial use | Commercial constraints / caveats | Price (2026-09-27) |
| -------- | ------------------ | ---------- | -------------- | -------------------------------- | ------------------ |
| kind / minikube | Local development, CI testing | ●●● | — | Local tools, not for hosting. | Free (OSS) |
| k3s | Edge / IoT, homelabs, small clusters | ●●● | ✅ | Apache-2.0; you are responsible for operations and security. | Free (OSS); pay for hosts |
| GKE Autopilot | Production K8s without node management | ●●● | 💰 | Pay per pod resources plus cluster fee (monthly credit covers one cluster). | Cluster $0.10/hr ($74.40/mo credit covers 1). Pods ~$0.0445/vCPU-hr † |
| Azure AKS | Enterprise K8s on Azure | ●●● | 💰 | Free tier control plane has no SLA; Standard tier for production. | Free tier $0. Standard $0.10/hr/cluster † |
| Amazon EKS | Enterprise K8s on AWS | ●●● | 💰 | Hourly control plane fee plus nodes. | $0.10/hr/cluster (extended support $0.60/hr) + nodes |
| DigitalOcean Kubernetes | SMB and startup K8s | ●●○ | 💰 | HA control plane is a paid option. | Control plane free. HA $40/mo. Nodes from $12/mo |
| Civo | Developer-focused fast k3s clusters | ●○○ | 💰 | $250 credit for new users, then paid. | Control plane free. Nodes from $5.43/mo |

### 3.6 Virtual machines / VPS

| Provider | Primary use domain | Popularity | Commercial use | Commercial constraints / caveats | Price (2026-09-27) |
| -------- | ------------------ | ---------- | -------------- | -------------------------------- | ------------------ |
| Oracle Cloud Always Free | Hobby servers, homelab-in-the-cloud | ●●○ | 🟡 | Commercial use allowed, but **idle Always Free instances can be reclaimed**; no SLA on free resources. Arm allowance halved in 2026-06. | Free: Ampere A1 2 OCPU / 12 GB, 2× AMD micro, 200 GB block |
| Hetzner Cloud | Cost-sensitive production, EU hosting | ●●○ (●●● in EU) | 💰 | Strict acceptable use policy (e.g. no crypto mining); identity verification may be required. Prices raised 2026-06. | CX23 €5.49/mo · CAX11 €5.99/mo (2 vCPU / 4 GB); IPv4 +€0.50 |
| Google Compute Engine | General IaaS on GCP | ●●● | ✅ | Free e2-micro limited to us-west1 / us-central1 / us-east1; egress beyond 1 GB/mo is billed. | Free 1× e2-micro + 30 GB disk. $300 trial credit |
| AWS EC2 / Lightsail | General IaaS; Lightsail for simple servers | ●●● | ✅ | New accounts (since 2025-07): up to $200 credits over 6 months instead of 12-month free tier. | Credits up to $200. Lightsail $5/mo (IPv4) or $3.50/mo (IPv6-only) |
| Azure Virtual Machines | Enterprise IaaS, Windows workloads | ●●● | ✅ | 12-month free VMs for new accounts; then pay-as-you-go. | Free 750 hr/mo B1s / B2pts v2 / B2ats v2 for 12 months † |
| DigitalOcean Droplets | Developers, SMBs | ●●● | 💰 | Standard commercial use. | From $4/mo (512 MiB) |
| Vultr / Akamai (Linode) | Developers, SMBs, global regions | ●●○ | 💰 | Standard commercial use. | Vultr from $2.50/mo (IPv6-only) †. Linode Nanode $5/mo † |
| Sakura Cloud / ConoHa / Xserver VPS | Japanese businesses and developers | ●●○ (JP) | 💰 | Standard commercial use; Japan-local support, invoices in JPY. Xserver VPS new orders may be paused. | Sakura ¥1,540/mo (1 GB). ConoHa ¥751/mo (512 MB) †. Xserver ¥1,980/mo (2 GB, monthly) |

### 3.7 Self-hosted PaaS tools

| Tool | Primary use domain | Popularity | Commercial use | Commercial constraints / caveats | Price (2026-09-27) |
| ---- | ------------------ | ---------- | -------------- | -------------------------------- | ------------------ |
| Kamal | Rails / Docker apps on own servers (by 37signals) | ●●○ | ✅ | MIT license. | Free |
| Coolify | Self-hosted Vercel/Heroku alternative for indie devs | ●●○ | ✅ | Apache-2.0 when self-hosted; managed Coolify Cloud is paid. | Self-hosted free. Cloud $5/mo (2 servers), +$3/server |
| Dokku | Heroku-style PaaS on a single server | ●●○ | ✅ | MIT license. | Free. Optional Dokku Pro $849 one-time |
| Dokploy | Self-hosted PaaS, Docker Swarm | ●○○ | 🟡 | Apache-2.0 except a `/proprietary` folder under a separate license. | Self-hosted free. Cloud from $4.50/server/mo |
| CapRover | Self-hosted PaaS with one-click apps | ●○○ | ✅ | Apache-2.0 license. | Free |

### 3.8 Pricing sources and recent changes

Notable changes found during the 2026-09-27 review:

- **AWS App Runner** stopped accepting new customers on 2026-04-30 (use ECS Express Mode instead).
- **AWS Free Tier** (2025-07-15): 12-month free tier replaced by up to $200 credits over 6 months for new accounts.
- **AWS Lambda** (2025-08-01): INIT phase billed for all functions.
- **Oracle Always Free** (2026-06): Ampere A1 allowance halved to 2 OCPU / 12 GB.
- **Hetzner** (2026-06-15): new-order prices raised (CX23 €3.99 → €5.49).
- **Netlify** (2025-09-04): new accounts are credit-based only; Pro became $20/mo with unlimited seats (2026-04).
- **Vercel**: Pro is a $20 platform fee with $20 usage credit; functions billed by Active CPU.
- **Render** (2026-04-23): workspace plans became Hobby $0 / Pro $25 / Scale $499 flat.
- **Fly.io**: no free allowance, only a short trial.
- **Koyeb**: joining Mistral AI; free plan no longer shown on the pricing page.
- **Zeabur** (2026-04): shared clusters being phased out; new server-based plans.
- **PythonAnywhere** (2026-01): plans consolidated into Developer $10/mo.
- **Val Town**: Pro $10 → $25/mo (2026-05); free plan limited to public vals (2026-09).
- **Xserver VPS** (2026-09-01): all plans raised; new orders possibly paused.
- **Azure Static Web Apps**: Dedicated plan retired (2025-10-31).

Official pricing pages:

- Static: [GitHub](https://github.com/pricing) · [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) · [Cloudflare Workers](https://developers.cloudflare.com/workers/platform/pricing/) · [Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/) · [Netlify](https://www.netlify.com/pricing/) · [S3](https://aws.amazon.com/s3/pricing/) · [CloudFront](https://aws.amazon.com/cloudfront/pricing/) · [Firebase](https://firebase.google.com/pricing) · [Azure SWA](https://azure.microsoft.com/en-us/pricing/details/app-service/static/) · [Vercel](https://vercel.com/pricing) · [GitLab](https://about.gitlab.com/pricing/) · [Render](https://render.com/pricing) · [Cloud CDN](https://cloud.google.com/cdn/pricing) · [GCP Load Balancing](https://cloud.google.com/load-balancing/pricing) · [Surge](https://surge.sh/pricing)
- Frontend / serverless: [Amplify](https://aws.amazon.com/amplify/pricing/) · [SST Console](https://sst.dev/docs/console/) · [Firebase App Hosting](https://firebase.google.com/docs/app-hosting/costs) · [Lambda](https://aws.amazon.com/lambda/pricing/) · [Azure Functions](https://azure.microsoft.com/en-us/pricing/details/functions/) · [Cloud Run](https://cloud.google.com/run/pricing) · [Deno Deploy](https://deno.com/deploy/pricing) · [Vercel Functions](https://vercel.com/docs/functions/usage-and-pricing) · [Supabase](https://supabase.com/pricing) · [Val Town](https://www.val.town/pricing)
- Containers: [Fly.io](https://fly.io/docs/about/pricing/) · [Azure Container Apps](https://azure.microsoft.com/pricing/details/container-apps/) · [Railway](https://railway.com/pricing) · [Fargate](https://aws.amazon.com/fargate/pricing/) · [Hugging Face](https://huggingface.co/pricing) · [Koyeb](https://www.koyeb.com/pricing) · [Northflank](https://northflank.com/pricing) · [Zeabur](https://zeabur.com/pricing) · [DO App Platform](https://www.digitalocean.com/pricing/app-platform) · [Azure App Service](https://azure.microsoft.com/en-us/pricing/details/app-service/linux/) · [App Engine](https://cloud.google.com/appengine/pricing) · [App Runner](https://aws.amazon.com/apprunner/pricing/) · [App Runner availability](https://docs.aws.amazon.com/apprunner/latest/dg/apprunner-availability-change.html) · [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/pricing/) · [Heroku](https://www.heroku.com/pricing) · [Streamlit](https://streamlit.io/cloud) · [PythonAnywhere](https://www.pythonanywhere.com/pricing/)
- Kubernetes / VMs: [GKE](https://cloud.google.com/kubernetes-engine/pricing) · [AKS](https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/) · [EKS](https://aws.amazon.com/eks/pricing/) · [DOKS](https://www.digitalocean.com/pricing/kubernetes) · [Civo](https://www.civo.com/pricing) · [Oracle Always Free](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) · [GCP Free](https://docs.cloud.google.com/free/docs/free-cloud-features) · [AWS Free](https://aws.amazon.com/free/) · [Lightsail](https://aws.amazon.com/lightsail/pricing/) · [Azure Free](https://azure.microsoft.com/en-us/pricing/free-services) · [Hetzner](https://www.hetzner.com/cloud) · [DO Droplets](https://www.digitalocean.com/pricing/droplets) · [Vultr](https://www.vultr.com/pricing/) · [Akamai](https://www.akamai.com/cloud/pricing) · [Sakura Cloud](https://cloud.sakura.ad.jp/products/server/) · [ConoHa](https://vps.conoha.jp/pricing/) · [Xserver VPS](https://vps.xserver.ne.jp/price.php)
- Self-hosted: [Kamal](https://kamal-deploy.org) · [Coolify](https://coolify.io/pricing) · [Dokku Pro](https://pro.dokku.com) · [Dokploy](https://dokploy.com/pricing) · [CapRover](https://caprover.com)

---

## 4. Deployment methods

Sorted by recommendation within each table. "Tried" marks methods used in at least one project.

### 4.1 Trigger / delivery mechanism

| Method | Rec | Complexity | Description | Examples | Tried |
| ------ | --- | ---------- | ----------- | -------- | ----- |
| Platform Git integration | ★★★ | ★☆☆☆☆ | Platform watches the repo and builds on push; preview per PR. | Vercel, Netlify, Cloudflare, Render, Railway, Amplify | ⬜ |
| CLI deploy from local | ★★★ | ★☆☆☆☆ | Upload and build from the developer machine. | `vercel`, `wrangler deploy`, `fly deploy`, `gcloud run deploy`, `firebase deploy` | ⬜ |
| CI/CD pipeline | ★★★ | ★★☆☆☆ | Build/test in CI, then deploy with provider CLI or API. | GitHub Actions, GitLab CI, Cloud Build, CodePipeline, Azure Pipelines | ✅ github-pages |
| CI with OIDC federation | ★★★ | ★★★☆☆ | CI authenticates to the cloud without long-lived keys. | GitHub Actions → AWS IAM role / GCP Workload Identity / Azure Federated Credentials | ⬜ |
| SSH-based push | ★★ | ★★★☆☆ | Copy artifacts or images to a server over SSH. | Kamal, rsync/scp + systemd, Ansible | ⬜ |
| Git push to remote | ★★ | ★☆☆☆☆ | Push to a special Git remote that builds and releases. | Heroku, Dokku, Hugging Face Spaces | ⬜ |
| GitOps | ★★ | ★★★★☆ | A controller in the cluster syncs manifests from Git. | Argo CD, Flux | ⬜ |
| Manual / console | ★ | ★☆☆☆☆ | Upload via web console (baseline for comparison). | S3 console upload, Azure portal zip deploy | ⬜ |

### 4.2 Build / packaging format

| Format | Rec | Complexity | Description | Examples | Tried |
| ------ | --- | ---------- | ----------- | -------- | ----- |
| Static artifacts | ★★★ | ★☆☆☆☆ | Pre-built HTML/JS/CSS uploaded to a CDN. | `vite build`, `astro build` | ✅ github-pages |
| Dockerfile / OCI image | ★★★ | ★★☆☆☆ | Build image, push to registry, run it. | GHCR, ECR, Artifact Registry, ACR, Docker Hub | ⬜ |
| Source + buildpacks | ★★ | ★☆☆☆☆ | Platform detects language and builds. | Cloud Native Buildpacks, Heroku, Cloud Run `--source` | ⬜ |
| Zip / function package | ★★ | ★★☆☆☆ | Bundled code for FaaS. | Lambda zip, Azure Functions zip deploy | ⬜ |
| Source + auto-builder | ★ | ★☆☆☆☆ | Platform-specific detection. | Railpack / Nixpacks (Railway), Vercel builders | ⬜ |
| Wasm | ★ | ★★★☆☆ | Compile to WebAssembly and run in an isolate/runtime. | Cloudflare Workers, Fermyon Spin | ⬜ |
| Nix | ★ | ★★★★☆ | Reproducible builds and system configs. | Nix flakes, NixOS on VPS | ⬜ |

### 4.3 Infrastructure provisioning

| Tool | Rec | Complexity | Scope | Notes | Tried |
| ---- | --- | ---------- | ----- | ----- | ----- |
| Platform config files | ★★★ | ★☆☆☆☆ | Single platform | `vercel.json`, `netlify.toml`, `wrangler.toml`, `fly.toml`, `render.yaml`, `app.yaml` | ⬜ |
| Terraform / OpenTofu | ★★★ | ★★★☆☆ | Multi-cloud | Declarative HCL, state management. | ⬜ |
| AWS CDK | ★★ | ★★★☆☆ | AWS | Synthesizes CloudFormation. | ⬜ |
| Pulumi | ★★ | ★★★☆☆ | Multi-cloud | IaC in TypeScript / Python / Go. | ⬜ |
| Azure Bicep | ★★ | ★★★☆☆ | Azure | Native ARM templates in a friendlier DSL. | ⬜ |
| Helm / Kustomize | ★★ | ★★★☆☆ | Kubernetes | Package and patch manifests. | ⬜ |
| SST | ★★ | ★★☆☆☆ | AWS / Cloudflare | App-centric IaC for full-stack frameworks. | ⬜ |
| AWS SAM | ★ | ★★☆☆☆ | AWS serverless | Lambda + API Gateway focused. | ⬜ |
| AWS CloudFormation | ★ | ★★★☆☆ | AWS | Native YAML/JSON templates. | ⬜ |
| Serverless Framework | ★ | ★★☆☆☆ | Serverless | Multi-provider function deploys. | ⬜ |
| Google Cloud Infrastructure Manager | ★ | ★★★☆☆ | GCP | Managed Terraform runs. | ⬜ |
| Ansible | ★ | ★★★☆☆ | VMs | Configuration management over SSH. | ⬜ |
| cloud-init | ★ | ★★☆☆☆ | VMs | First-boot provisioning. | ⬜ |

### 4.4 Release strategies

| Strategy | Rec | Complexity | Description | Where to try it | Tried |
| -------- | --- | ---------- | ----------- | --------------- | ----- |
| Preview environments | ★★★ | ★☆☆☆☆ | Ephemeral deploy per branch/PR. | Vercel, Netlify, Cloudflare, Render, Firebase channels | ⬜ |
| Immutable deploys + instant rollback | ★★★ | ★☆☆☆☆ | Every deploy is a new immutable version. | Vercel, Netlify, Cloudflare Workers versions | ⬜ |
| Canary / traffic splitting | ★★★ | ★★★☆☆ | Send a percentage of traffic to the new version. | Cloud Run revisions, Container Apps revisions, Argo Rollouts, Lambda aliases | ⬜ |
| Rolling update | ★★ | ★★☆☆☆ | Replace instances gradually. | Kubernetes Deployment, ECS, Fly.io | ⬜ |
| Blue/green | ★★ | ★★★☆☆ | Switch traffic between two full environments. | ECS + CodeDeploy, App Service slots, Kamal | ⬜ |
| Recreate | ★ | ★☆☆☆☆ | Stop old, start new; downtime. | Plain VM + systemd | ⬜ |
