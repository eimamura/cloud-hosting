# fastapi-app

Python ASGI web API built with [FastAPI](https://fastapi.tiangolo.com). Implements the same probe contract as
`hono-api`, so Python-oriented platforms can be tested with the same smoke test.

## Layout

```
app/
  main.py            # Routes (probe contract) + /docs (OpenAPI UI)
  info.py            # Environment detection
lambda_handler.py    # AWS Lambda entry via Mangum
requirements.txt     # Runtime dependencies (detected by buildpacks, Render, Railway, Heroku, …)
Procfile             # Start command for Procfile-based platforms
.python-version      # Python version hint for buildpacks and uv
Dockerfile           # ASGI server image
```

## Local development

```bash
uv run --with-requirements requirements.txt uvicorn app.main:app --reload --port 8080
```

## Entry points by platform

| Platform | How to wire it up in a deployment project |
| -------- | ----------------------------------------- |
| Docker / Cloud Run / Fly.io / Azure Container Apps / Kubernetes / VPS / Kamal / Coolify | Build `Dockerfile` with this directory as context. Listens on `PORT` (default 8080). |
| Buildpacks (`gcloud run deploy --source`), Heroku, Dokku, Render, Railway | Root directory `workloads/fastapi-app`; `requirements.txt` and `Procfile` are detected. |
| Hugging Face Spaces (Docker SDK) | Use the `Dockerfile` and set `app_port: 8080` in the Space README metadata. |
| AWS Lambda | Package `app/`, `lambda_handler.py`, and dependencies; handler `lambda_handler.handler`. |
| Azure Functions | Add a `function_app.py` in the deployment project: `func.AsgiFunctionApp(app=app, http_auth_level=func.AuthLevel.ANONYMOUS)`. |

Verified locally: uvicorn server, Docker image, and the Lambda handler (invoked with a Function URL event).

See [../README.md](../README.md) for the probe contract and environment variables.
