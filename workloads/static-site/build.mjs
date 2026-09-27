// Copies public/ to dist/ and writes dist/info.json with build metadata.
// Zero dependencies so it runs on any static host's build image.
import { cpSync, mkdirSync, rmSync, writeFileSync, readFileSync } from "node:fs";

const env = process.env;
const pkg = JSON.parse(readFileSync(new URL("./package.json", import.meta.url), "utf8"));

// Build-time markers set by static hosts' CI environments (first match wins).
const TARGET_MARKERS = [
  ["VERCEL", "vercel"],
  ["NETLIFY", "netlify"],
  ["CF_PAGES", "cloudflare-pages"],
  ["WORKERS_CI", "cloudflare-workers"],
  ["RENDER", "render"],
  ["AWS_APP_ID", "aws-amplify"],
  ["GITLAB_CI", "gitlab-ci"],
  ["GITHUB_ACTIONS", "github-actions"],
];

const COMMIT_VARS = [
  "GIT_COMMIT",
  "VERCEL_GIT_COMMIT_SHA",
  "COMMIT_REF",
  "CF_PAGES_COMMIT_SHA",
  "WORKERS_CI_COMMIT_SHA",
  "RENDER_GIT_COMMIT",
  "AWS_COMMIT_ID",
  "CI_COMMIT_SHA",
  "GITHUB_SHA",
];

const firstSet = (names) => names.map((n) => env[n]).find((v) => v) ?? null;

const info = {
  workload: "static-site",
  version: env.APP_VERSION || pkg.version,
  target: env.DEPLOY_TARGET || TARGET_MARKERS.find(([name]) => env[name])?.[1] || "unknown",
  commit: firstSet(COMMIT_VARS),
  builtAt: new Date().toISOString(),
};

rmSync("dist", { recursive: true, force: true });
mkdirSync("dist", { recursive: true });
cpSync("public", "dist", { recursive: true });
writeFileSync("dist/info.json", JSON.stringify(info, null, 2) + "\n");

console.log("Built dist/ with", info);
