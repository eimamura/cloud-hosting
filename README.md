# cloud-hosting

A collection of independent experiments with deployment methods and cloud hosting providers.

Each deployment project is a self-contained top-level directory that uses whatever tooling best fits its
target platform. The applications being deployed are shared: a small set of reusable test workloads lives in
[`workloads/`](./workloads), and every deployment is verified with the same [`tools/smoke-test.sh`](./tools/smoke-test.sh).

## Entry point

[`index.html`](./index.html) is the landing page. It links to the live deployment of every project.
Open it locally in a browser, or host it anywhere static (e.g. GitHub Pages).

## Workloads

| Workload | Use for |
| -------- | ------- |
| [`static-site`](./workloads/static-site) | Static hosts |
| [`hono-api`](./workloads/hono-api) | Node / Docker, Cloudflare Workers, Deno, Bun, AWS Lambda, Vercel, Netlify |
| [`fastapi-app`](./workloads/fastapi-app) | Python: Docker, buildpacks, Procfile platforms, AWS Lambda |

Verify any deployment:

```bash
tools/smoke-test.sh https://<deployment-url> [--static] [--expect-target <name>]
```

## Docs

All provider facts and all progress live in one file, [`docs/catalog.yaml`](./docs/catalog.yaml): the roadmap,
every hosting target (hosting, use, commercial terms, price), and every vendor's agent tooling (API / CLI / MCP /
IaC, human-only steps). Browse it with filters in [`catalog.html`](./catalog.html)
(published at https://eimamura.github.io/cloud-hosting/catalog.html; locally: `python3 -m http.server`).

- [Catalog data](./docs/catalog.yaml) — single source of truth: roadmap, services, vendors, legends
- [Hosting guide](./docs/hosting-candidates.md) — roadmap rationale, agent operability principles, deployment methods

Validate after editing, and regenerate the project table below:

```bash
pip install pyyaml
tools/catalog.py check   # also runs before every GitHub Pages deploy
tools/catalog.py sync    # rewrites the Projects table from the roadmap
```

## Projects

Generated from the roadmap in `docs/catalog.yaml` by `tools/catalog.py sync`. Do not edit by hand.

<!-- projects:start -->
| Project | Hosting | Workload | Status | URL |
| ------- | ------- | -------- | ------ | --- |
| [github-pages](./github-pages) | GitHub Pages | root `index.html` | ✅ Done | https://eimamura.github.io/cloud-hosting/ |
<!-- projects:end -->

## Adding a project

See [AGENTS.md](./AGENTS.md#adding-a-new-project).
