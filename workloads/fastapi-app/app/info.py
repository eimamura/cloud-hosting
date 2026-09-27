"""Detects deployment metadata from environment variables.

Keep the variable lists in sync with workloads/README.md and hono-api/src/info.ts.
"""

import os
import platform
from datetime import datetime, timezone

WORKLOAD = "fastapi-app"
DEFAULT_VERSION = "0.1.0"

TARGET_MARKERS = [
    ("AWS_LAMBDA_FUNCTION_NAME", "aws-lambda"),
    ("ECS_CONTAINER_METADATA_URI_V4", "aws-ecs"),
    ("VERCEL", "vercel"),
    ("NETLIFY", "netlify"),
    ("RENDER", "render"),
    ("FLY_APP_NAME", "fly"),
    ("RAILWAY_ENVIRONMENT", "railway"),
    ("K_SERVICE", "cloud-run"),
    ("GAE_SERVICE", "app-engine"),
    ("CONTAINER_APP_NAME", "azure-container-apps"),
    ("FUNCTIONS_WORKER_RUNTIME", "azure-functions"),
    ("WEBSITE_SITE_NAME", "azure-app-service"),
    ("SPACE_ID", "huggingface-spaces"),
    ("DENO_DEPLOYMENT_ID", "deno-deploy"),
    ("DYNO", "heroku"),
    ("KUBERNETES_SERVICE_HOST", "kubernetes"),
]

REGION_VARS = [
    "REGION",
    "FLY_REGION",
    "VERCEL_REGION",
    "AWS_REGION",
    "RAILWAY_REPLICA_REGION",
    "REGION_NAME",
    "DENO_REGION",
]

COMMIT_VARS = [
    "GIT_COMMIT",
    "VERCEL_GIT_COMMIT_SHA",
    "RENDER_GIT_COMMIT",
    "RAILWAY_GIT_COMMIT_SHA",
    "COMMIT_REF",
    "SOURCE_VERSION",
    "GITHUB_SHA",
]

INSTANCE_VARS = [
    "FLY_MACHINE_ID",
    "K_REVISION",
    "AWS_LAMBDA_LOG_STREAM_NAME",
    "RENDER_INSTANCE_ID",
    "DYNO",
    "HOSTNAME",
]


def _first_set(names: list[str]) -> str | None:
    return next((os.environ[n] for n in names if os.environ.get(n)), None)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class InstanceState:
    def __init__(self) -> None:
        self.started_at = ""
        self.request_count = 0

    def record_request(self) -> None:
        if not self.started_at:
            self.started_at = _now()
        self.request_count += 1


def detect_info(state: InstanceState) -> dict:
    target = os.environ.get("DEPLOY_TARGET") or next(
        (t for name, t in TARGET_MARKERS if os.environ.get(name)), "unknown"
    )
    return {
        "workload": WORKLOAD,
        "version": os.environ.get("APP_VERSION") or DEFAULT_VERSION,
        "runtime": f"python {platform.python_version()}",
        "target": target,
        "region": _first_set(REGION_VARS),
        "commit": _first_set(COMMIT_VARS),
        "instance": _first_set(INSTANCE_VARS),
        "startedAt": state.started_at,
        "requestCount": state.request_count,
        "now": _now(),
    }
