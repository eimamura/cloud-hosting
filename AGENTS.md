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
- **The root is the entry point.** `index.html` at the root lists every project and links to its deployed URL.
  When a project is added, removed, renamed, or its deployment URL changes, update `index.html` and the
  project table in `README.md` in the same change.

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
├── docs/          # Workspace-level docs (e.g. hosting-candidates.md)
├── workloads/     # Reusable test apps: static-site, hono-api, fastapi-app
├── tools/         # Shared scripts, e.g. smoke-test.sh
└── <project>/     # Independent deployment projects
```

## Adding a new project

1. Create a top-level directory with a short kebab-case name that hints at the platform, e.g. `vercel-nextjs`,
   `cloudflare-workers-hono`, `aws-lambda-python`.
2. Choose a workload from `workloads/` (see the roadmap in `docs/hosting-candidates.md`).
   Add only platform-specific files that reference it.
3. Add a `README.md` inside it describing: the hosting target, the workload used, how to deploy,
   how to verify (`tools/smoke-test.sh <url>`), and how to tear down.
4. Add project-specific ignore rules to a `.gitignore` inside the project if the root one is not enough.
5. Register the project in the root `index.html` (`projects` array) and in the root `README.md` table.

## Secrets

- Never commit credentials. Use `.env.example` to document required variables.
- Do not read `.env`, `*.pem`, `*.key`, `terraform.tfvars`, or credential files unless the user explicitly asks.
