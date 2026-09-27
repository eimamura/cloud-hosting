# github-pages

Publishes the root entry page (`index.html`) to GitHub Pages. Roadmap item #1 in
[docs/hosting-candidates.md](../docs/hosting-candidates.md).

| Item | Value |
| ---- | ----- |
| Hosting | GitHub Pages |
| Workload | root `index.html` |
| Method | GitHub Actions (`actions/upload-pages-artifact` + `actions/deploy-pages`) |
| Workflow | [`.github/workflows/github-pages.yml`](../.github/workflows/github-pages.yml) |
| URL | https://eimamura.github.io/cloud-hosting/ |

GitHub only runs workflows from the repository root, so the workflow file lives in `.github/workflows/`
rather than in this directory.

## Setup (one time)

1. Push the repository to GitHub.
2. Enable Pages with GitHub Actions as the source:

   ```bash
   gh api -X POST repos/<owner>/cloud-hosting/pages -f build_type=workflow
   ```

   (or Settings → Pages → Source: GitHub Actions)

## Deploy

Automatic on push to `main` when `index.html`, this directory, or the workflow changes.
Manual run:

```bash
gh workflow run github-pages.yml
gh run watch
```

## Verify

The workflow's `Verify` step checks that the published URL returns HTTP 200. Manually:

```bash
curl -sI https://<owner>.github.io/cloud-hosting/ | head -1
```

## Constraints

- Free plan: Pages requires a **public** repository. Private repositories need a paid plan.
- Not for e-commerce or SaaS (GitHub terms). Soft limits: 1 GB site, 100 GB/month bandwidth, 10 builds/hour.

## Tear down

```bash
gh api -X DELETE repos/<owner>/cloud-hosting/pages
```
