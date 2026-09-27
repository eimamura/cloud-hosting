// Detects deployment metadata from environment variables.
// Keep the variable lists in sync with workloads/README.md and fastapi-app/app/info.py.

export const WORKLOAD = "hono-api";
export const DEFAULT_VERSION = "0.1.0";

type Vars = Record<string, string | undefined>;

const TARGET_MARKERS: ReadonlyArray<readonly [string, string]> = [
  ["AWS_LAMBDA_FUNCTION_NAME", "aws-lambda"],
  ["ECS_CONTAINER_METADATA_URI_V4", "aws-ecs"],
  ["VERCEL", "vercel"],
  ["NETLIFY", "netlify"],
  ["RENDER", "render"],
  ["FLY_APP_NAME", "fly"],
  ["RAILWAY_ENVIRONMENT", "railway"],
  ["K_SERVICE", "cloud-run"],
  ["GAE_SERVICE", "app-engine"],
  ["CONTAINER_APP_NAME", "azure-container-apps"],
  ["FUNCTIONS_WORKER_RUNTIME", "azure-functions"],
  ["WEBSITE_SITE_NAME", "azure-app-service"],
  ["SPACE_ID", "huggingface-spaces"],
  ["DENO_DEPLOYMENT_ID", "deno-deploy"],
  ["DYNO", "heroku"],
  ["KUBERNETES_SERVICE_HOST", "kubernetes"],
];

const REGION_VARS = [
  "REGION",
  "FLY_REGION",
  "VERCEL_REGION",
  "AWS_REGION",
  "RAILWAY_REPLICA_REGION",
  "REGION_NAME",
  "DENO_REGION",
];

const COMMIT_VARS = [
  "GIT_COMMIT",
  "VERCEL_GIT_COMMIT_SHA",
  "RENDER_GIT_COMMIT",
  "RAILWAY_GIT_COMMIT_SHA",
  "COMMIT_REF",
  "SOURCE_VERSION",
  "GITHUB_SHA",
];

const INSTANCE_VARS = [
  "FLY_MACHINE_ID",
  "K_REVISION",
  "AWS_LAMBDA_LOG_STREAM_NAME",
  "RENDER_INSTANCE_ID",
  "DYNO",
  "HOSTNAME",
];

const firstSet = (vars: Vars, names: readonly string[]): string | null =>
  names.map((n) => vars[n]).find((v) => v) ?? null;

export interface Info {
  workload: string;
  version: string;
  runtime: string;
  target: string;
  region: string | null;
  commit: string | null;
  instance: string | null;
  startedAt: string;
  requestCount: number;
  now: string;
}

export interface InstanceState {
  startedAt: string;
  requestCount: number;
}

export function detectInfo(
  vars: Vars,
  runtime: string,
  state: InstanceState,
  hints: { target?: string; region?: string } = {},
): Info {
  return {
    workload: WORKLOAD,
    version: vars.APP_VERSION || DEFAULT_VERSION,
    runtime,
    target:
      vars.DEPLOY_TARGET ||
      TARGET_MARKERS.find(([name]) => vars[name])?.[1] ||
      hints.target ||
      "unknown",
    region: firstSet(vars, REGION_VARS) ?? hints.region ?? null,
    commit: firstSet(vars, COMMIT_VARS),
    instance: firstSet(vars, INSTANCE_VARS),
    startedAt: state.startedAt,
    requestCount: state.requestCount,
    now: new Date().toISOString(),
  };
}
