# Hosting Candidates and Deployment Methods

The narrative guide for this workspace: why the roadmap is ordered the way it is, how to let a coding agent
operate hosting providers safely, supporting services, and deployment methods.

**All facts about providers, and all progress, live in one file: [catalog.yaml](./catalog.yaml).** It holds the
roadmap (the only place progress is recorded), every hosting target (hosting, use, commercial terms, price), every
vendor's agent tooling (API, CLI, MCP, IaC, human-only steps, rating), the legends, per-entry `checked` dates, and
source links. Browse it in [catalog.html](../catalog.html)
(published at https://eimamura.github.io/cloud-hosting/catalog.html).

This guide deliberately contains no per-provider facts, so it cannot drift from the catalog. When you need to name a
provider here, link to its catalog entry (`catalog.html#providers/<service-id>`) instead of restating its details.

`tools/catalog.py check` validates the catalog, the README project table, project directories, and links in the docs.
It runs before every GitHub Pages deploy.

---

## 1. Roadmap

The roadmap table lives in [catalog.yaml](./catalog.yaml) (`roadmap`) and is shown on the Roadmap tab of
[catalog.html](../catalog.html#roadmap).

Ordered so that each step introduces roughly one new concept on top of the previous ones:
static → framework PaaS → containers → serverless + IaC → self-managed → orchestration.

Every row reuses one of the shared [workloads](../workloads/README.md), so each experiment only adds
platform-specific files. Verify each deployment with `tools/smoke-test.sh`.

Framework-specific SSR (e.g. Next.js on Vercel / Amplify) and databases (D1, RDS, Neon) are intentionally left out
of the workloads. Add them as new workloads only when an experiment needs them.

Progress is recorded only on roadmap items (`status`, `project`, `url`, `date`). A service's tried status, the
project table in the root README (`tools/catalog.py sync`), and the cards on the root `index.html` are derived
from it.

---

## 2. Supporting services (data, storage) — optional pairings

| Kind | Candidates (recommended first) |
| ---- | ------------------------------ |
| Postgres | Neon, Supabase, Cloud SQL, RDS / Aurora Serverless, Aiven, Azure Database for PostgreSQL |
| SQLite at the edge | Cloudflare D1, Turso (libSQL) |
| Key-value / cache | Upstash Redis, Cloudflare KV, Valkey on VPS |
| Object storage | Cloudflare R2, S3, GCS, Azure Blob, Backblaze B2 |
| Document DB | Firestore, DynamoDB, MongoDB Atlas, Cosmos DB |

---

## 3. Agent operability

How far an autonomous coding agent (e.g. Claude Code with a shell and MCP support) can operate a provider is
recorded per vendor in the catalog (`vendors`: API, CLI and token env var, MCP, IaC, human-only steps, rating).
The principles below hold across all of them.

### 3.1 Key takeaways

1. **The CLI + a token env var is the most reliable path.** Prefer it over MCP for deploys, even where an MCP
   server exists.
2. **"Has an MCP server" does not mean "can deploy".** Many official servers are read-only, docs-only, or lack
   deploy / delete tools (🟡 in the MCP column). Use the CLI for the rest.
3. **Hosted MCP servers often need browser OAuth once.** Servers that also accept a static API token are fully
   headless; the MCP detail of each vendor says which.
4. **The same bootstrap steps are human-only everywhere** (next section). Everything after them can be delegated.
5. **Hyperscalers are fully operable but have the largest blast radius.** Use the guardrails in 3.4.

### 3.2 Human-only steps (common to all providers)

Provider-specific extras are in each vendor's `human` field.

| Step | Notes |
| ---- | ----- |
| Account signup, email / phone verification | A few CLIs can create the account themselves. |
| Payment method / identity verification (KYC) | Some providers require a real credit card, manual review, or ID documents. |
| Creating the first API token / key | After that, some CLIs can mint more tokens. |
| Installing a GitHub / GitLab app for Git-triggered deploys | Avoid by deploying from the CLI or pushing an image. |
| OAuth consent for hosted MCP servers | One browser click per client. |
| Root / admin MFA, quota increase approvals, org policies | Hyperscalers mostly. |
| DNS changes at an external registrar, domain verification | Unless the registrar also has an API the agent can use. |
| Bootstrapping keyless CI (GitHub Actions OIDC trust) | A human does it once with admin credentials; after that the agent manages it as IaC. |

### 3.3 Kubernetes tooling

Tools that work across every cluster in the catalog (they are not hosting targets, so they are listed here).

| Item | Tooling | MCP | Rating |
| ---- | ------- | --- | ------ |
| kind / minikube / k3s | CLI + `kubectl`; k3s installs over SSH. No cloud account; needs local Docker / VM (sudo for k3s) | 🔵 `containers/kubernetes-mcp-server` (core, helm, ... toolsets; read-only mode) or `Flux159/mcp-server-kubernetes` | **Full** |
| Helm | `helm` CLI | 🔵 `zekker6/mcp-helm` (chart repos); helm toolset in the k8s MCP | **Full** (via CLI) |
| Argo CD | `argocd` CLI | 🟡 `argoproj-labs/mcp-for-argocd` (`ARGOCD_BASE_URL` / `ARGOCD_API_TOKEN`, read-only mode) | **Full** |

### 3.4 Guardrails

- **Sandbox accounts:** give the agent a dedicated account / project / subscription, never org-admin credentials.
- **Short-lived, least-privilege credentials:** assume-role / impersonation with narrow roles on hyperscalers,
  project- or scope-limited tokens on PaaS.
- **Budgets and alerts** on every paid account; deny expensive instance types with org policies where available.
- **Read-only MCP by default:** use a vendor's read-only mode or high-risk switch where it exists (see the MCP
  detail), and enable writes per task.
- **Teardown is part of every project:** each project README documents how the agent removes what it created.

---

## 4. Review log

Dated notes from catalog reviews. These are history, not current state: the current state is always the catalog
entry, whose `checked` date says when it was last verified.

### 2026-09-27 pricing review

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

---

## 5. Deployment methods

Sorted by recommendation within each table. Which method each experiment uses is recorded on its roadmap item
(`method` in [catalog.yaml](./catalog.yaml)).

### 5.1 Trigger / delivery mechanism

| Method | Rec | Complexity | Description | Examples |
| ------ | --- | ---------- | ----------- | -------- |
| Platform Git integration | ★★★ | ★☆☆☆☆ | Platform watches the repo and builds on push; preview per PR. | Vercel, Netlify, Cloudflare, Render, Railway, Amplify |
| CLI deploy from local | ★★★ | ★☆☆☆☆ | Upload and build from the developer machine. | `vercel`, `wrangler deploy`, `fly deploy`, `gcloud run deploy`, `firebase deploy` |
| CI/CD pipeline | ★★★ | ★★☆☆☆ | Build/test in CI, then deploy with provider CLI or API. | GitHub Actions, GitLab CI, Cloud Build, CodePipeline, Azure Pipelines |
| CI with OIDC federation | ★★★ | ★★★☆☆ | CI authenticates to the cloud without long-lived keys. | GitHub Actions → AWS IAM role / GCP Workload Identity / Azure Federated Credentials |
| SSH-based push | ★★ | ★★★☆☆ | Copy artifacts or images to a server over SSH. | Kamal, rsync/scp + systemd, Ansible |
| Git push to remote | ★★ | ★☆☆☆☆ | Push to a special Git remote that builds and releases. | Heroku, Dokku, Hugging Face Spaces |
| GitOps | ★★ | ★★★★☆ | A controller in the cluster syncs manifests from Git. | Argo CD, Flux |
| Manual / console | ★ | ★☆☆☆☆ | Upload via web console (baseline for comparison). | S3 console upload, Azure portal zip deploy |

### 5.2 Build / packaging format

| Format | Rec | Complexity | Description | Examples |
| ------ | --- | ---------- | ----------- | -------- |
| Static artifacts | ★★★ | ★☆☆☆☆ | Pre-built HTML/JS/CSS uploaded to a CDN. | `vite build`, `astro build` |
| Dockerfile / OCI image | ★★★ | ★★☆☆☆ | Build image, push to registry, run it. | GHCR, ECR, Artifact Registry, ACR, Docker Hub |
| Source + buildpacks | ★★ | ★☆☆☆☆ | Platform detects language and builds. | Cloud Native Buildpacks, Heroku, Cloud Run `--source` |
| Zip / function package | ★★ | ★★☆☆☆ | Bundled code for FaaS. | Lambda zip, Azure Functions zip deploy |
| Source + auto-builder | ★ | ★☆☆☆☆ | Platform-specific detection. | Railpack / Nixpacks (Railway), Vercel builders |
| Wasm | ★ | ★★★☆☆ | Compile to WebAssembly and run in an isolate/runtime. | Cloudflare Workers, Fermyon Spin |
| Nix | ★ | ★★★★☆ | Reproducible builds and system configs. | Nix flakes, NixOS on VPS |

### 5.3 Infrastructure provisioning

| Tool | Rec | Complexity | Scope | Notes |
| ---- | --- | ---------- | ----- | ----- |
| Platform config files | ★★★ | ★☆☆☆☆ | Single platform | `vercel.json`, `netlify.toml`, `wrangler.toml`, `fly.toml`, `render.yaml`, `app.yaml` |
| Terraform / OpenTofu | ★★★ | ★★★☆☆ | Multi-cloud | Declarative HCL, state management. |
| AWS CDK | ★★ | ★★★☆☆ | AWS | Synthesizes CloudFormation. |
| Pulumi | ★★ | ★★★☆☆ | Multi-cloud | IaC in TypeScript / Python / Go. |
| Azure Bicep | ★★ | ★★★☆☆ | Azure | Native ARM templates in a friendlier DSL. |
| Helm / Kustomize | ★★ | ★★★☆☆ | Kubernetes | Package and patch manifests. |
| SST | ★★ | ★★☆☆☆ | AWS / Cloudflare | App-centric IaC for full-stack frameworks. |
| AWS SAM | ★ | ★★☆☆☆ | AWS serverless | Lambda + API Gateway focused. |
| AWS CloudFormation | ★ | ★★★☆☆ | AWS | Native YAML/JSON templates. |
| Serverless Framework | ★ | ★★☆☆☆ | Serverless | Multi-provider function deploys. |
| Google Cloud Infrastructure Manager | ★ | ★★★☆☆ | GCP | Managed Terraform runs. |
| Ansible | ★ | ★★★☆☆ | VMs | Configuration management over SSH. |
| cloud-init | ★ | ★★☆☆☆ | VMs | First-boot provisioning. |

### 5.4 Release strategies

| Strategy | Rec | Complexity | Description | Where to try it |
| -------- | --- | ---------- | ----------- | --------------- |
| Preview environments | ★★★ | ★☆☆☆☆ | Ephemeral deploy per branch/PR. | Vercel, Netlify, Cloudflare, Render, Firebase channels |
| Immutable deploys + instant rollback | ★★★ | ★☆☆☆☆ | Every deploy is a new immutable version. | Vercel, Netlify, Cloudflare Workers versions |
| Canary / traffic splitting | ★★★ | ★★★☆☆ | Send a percentage of traffic to the new version. | Cloud Run revisions, Container Apps revisions, Argo Rollouts, Lambda aliases |
| Rolling update | ★★ | ★★☆☆☆ | Replace instances gradually. | Kubernetes Deployment, ECS, Fly.io |
| Blue/green | ★★ | ★★★☆☆ | Switch traffic between two full environments. | ECS + CodeDeploy, App Service slots, Kamal |
| Recreate | ★ | ★☆☆☆☆ | Stop old, start new; downtime. | Plain VM + systemd |
