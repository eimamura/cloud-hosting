import { Hono } from "hono";
import type { Context } from "hono";
import { env, getRuntimeKey } from "hono/adapter";
import { html } from "hono/html";
import { detectInfo, type Info, type InstanceState } from "./info.ts";

// Set lazily: some runtimes (e.g. Cloudflare Workers) freeze the clock at global scope.
const state: InstanceState = { startedAt: "", requestCount: 0 };

// Runtime keys that imply a platform even without environment markers.
const RUNTIME_TARGETS: Record<string, string> = { workerd: "cloudflare-workers" };

function runtimeLabel(): string {
  const key = getRuntimeKey();
  const versions = (globalThis as { process?: { versions?: Record<string, string> } }).process
    ?.versions;
  if (key === "node" && versions?.node) return `node ${versions.node}`;
  if (key === "bun" && versions?.bun) return `bun ${versions.bun}`;
  if (key === "deno") {
    const deno = (globalThis as { Deno?: { version?: { deno?: string } } }).Deno;
    if (deno?.version?.deno) return `deno ${deno.version.deno}`;
  }
  return key;
}

function buildInfo(c: Context): Info {
  const cf = (c.req.raw as Request & { cf?: { colo?: string } }).cf;
  return detectInfo(env(c) as Record<string, string | undefined>, runtimeLabel(), state, {
    target: RUNTIME_TARGETS[getRuntimeKey()],
    region: cf?.colo,
  });
}

export const app = new Hono();

app.use(async (_c, next) => {
  if (!state.startedAt) state.startedAt = new Date().toISOString();
  state.requestCount++;
  await next();
});

app.get("/healthz", (c) => c.text("ok"));

app.get("/api/info", (c) => c.json(buildInfo(c)));

app.get("/api/echo", (c) => {
  const headers = Object.fromEntries(c.req.raw.headers.entries());
  const forwarded = headers["x-forwarded-for"]?.split(",")[0]?.trim();
  return c.json({
    method: c.req.method,
    path: c.req.path,
    query: c.req.queries(),
    ip: headers["cf-connecting-ip"] ?? forwarded ?? null,
    headers,
  });
});

app.get("/", (c) => {
  const info = buildInfo(c);
  return c.html(html`<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${info.workload}</title>
  <style>
    body { margin: 0; padding: 48px 16px; font: 16px/1.5 system-ui, sans-serif; }
    main { max-width: 720px; margin: 0 auto; }
    table { border-collapse: collapse; width: 100%; }
    td { padding: 6px 10px; border-bottom: 1px solid #8884; overflow-wrap: anywhere; }
    td:first-child { opacity: 0.7; width: 30%; }
  </style>
</head>
<body>
  <main>
    <h1>${info.workload}</h1>
    <table>
      ${Object.entries(info).map(([k, v]) => html`<tr><td>${k}</td><td>${v ?? "—"}</td></tr>`)}
    </table>
    <p><a href="api/info">/api/info</a> · <a href="api/echo">/api/echo</a> · <a href="healthz">/healthz</a></p>
  </main>
</body>
</html>`);
});
