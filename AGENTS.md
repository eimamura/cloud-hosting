# AGENTS.md

Guidance for coding agents working in this repository.

## Purpose

This workspace is a playground for experimenting with different deployment methods and cloud hosting providers.
It holds multiple **independent projects**. Each project picks whatever stack fits its target platform best.

## Principles

- **Deployment projects are independent.** Do not standardize tooling, IaC, CI, or structure across deployment
  projects, and do not import from one deployment project into another.
- **Test applications are shared.** Reusable test apps live in `workloads/` and the smoke test in `tools/`.
  A deployment project picks a workload and adds only platform-specific files (config, IaC, CI, manifests).
  Do not copy a workload's app code into a deployment project, and do not change a workload to suit a single
  platform — add a new entry/adapter file instead. See `workloads/README.md`.
- **One project = one top-level directory.** Work only inside the target project unless the task is about the root.
- **Git is managed at the root only.** Never run `git init` inside a project directory and never add nested
  repositories or submodules.
- **The catalog is the single source of truth.** Provider facts and progress live only in `docs/catalog.yaml`
  (`roadmap`, `vendors`, `services`, `enums`). Do not restate them in Markdown docs; link to the catalog instead.
  When you re-verify an entry, update its `checked` date. Run `tools/catalog.py check` after every edit.
- **The root is the entry point.** `index.html` at the root lists every project and links to its deployed URL.
  It reads the roadmap in `docs/catalog.yaml`, and the project table in `README.md` is generated from it
  (`tools/catalog.py sync`), so a project is registered by editing its roadmap item only.

## Language

- Conversation with the user (chat with the coding agent): **Japanese**.
- Everything else — source code, comments, commit messages, documentation, file names: **English**.

## Root layout

```
.
├── AGENTS.md      # This file
├── README.md      # Overview and project table
├── .gitignore     # Root-level ignore rules covering all projects
├── index.html     # Entry point page linking to each deployment
├── catalog.html   # Viewer for docs/catalog.yaml and docs/hosting-candidates.md
├── docs/          # catalog.yaml (all provider facts + progress) and hosting-candidates.md (guide)
├── workloads/     # Reusable test apps: static-site, hono-api, fastapi-app
├── tools/         # Shared scripts: smoke-test.sh, catalog.py (validate / sync the catalog)
└── <project>/     # Independent deployment projects
```

## Adding a new project

1. Create a top-level directory with a short kebab-case name that hints at the platform, e.g. `vercel-nextjs`,
   `cloudflare-workers-hono`, `aws-lambda-python`.
2. Choose a workload from `workloads/` (see the roadmap in `docs/catalog.yaml` / `catalog.html#roadmap`).
   Add only platform-specific files that reference it.
3. Add a `README.md` inside it describing: the hosting target, the workload used, how to deploy,
   how to verify (`tools/smoke-test.sh <url>`), and how to tear down.
4. Add project-specific ignore rules to a `.gitignore` inside the project if the root one is not enough.
5. Register it on its roadmap item in `docs/catalog.yaml`: `status` (`in-progress` / `done`), `project: <dir>`,
   and once deployed `url` and `date`. If the experiment is not on the roadmap yet, append a new item.
6. Run `tools/catalog.py sync` (updates the README table) and `tools/catalog.py check`. `index.html` and
   `catalog.html` pick the change up automatically.

## Secrets

- Never commit credentials. Use `.env.example` to document required variables.
- Do not read `.env`, `*.pem`, `*.key`, `terraform.tfvars`, or credential files unless the user explicitly asks.
