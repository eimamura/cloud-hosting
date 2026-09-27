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

- [Hosting candidates and deployment methods](./docs/hosting-candidates.md)

## Projects

| Project | Hosting | Workload | URL |
| ------- | ------- | -------- | --- |
| [github-pages](./github-pages) | GitHub Pages (GitHub Actions) | root `index.html` | https://eimamura.github.io/cloud-hosting/ |

## Adding a project

See [AGENTS.md](./AGENTS.md#adding-a-new-project).
