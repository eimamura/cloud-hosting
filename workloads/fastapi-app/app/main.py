"""ASGI app implementing the probe contract in workloads/README.md."""

from html import escape

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse

from app.info import InstanceState, detect_info

state = InstanceState()

app = FastAPI(title="fastapi-app", docs_url="/docs", redoc_url=None)


@app.middleware("http")
async def count_requests(request: Request, call_next):
    state.record_request()
    return await call_next(request)


@app.get("/healthz", response_class=PlainTextResponse)
def healthz() -> str:
    return "ok"


@app.get("/api/info")
def info() -> dict:
    return detect_info(state)


@app.get("/api/echo")
def echo(request: Request) -> dict:
    headers = dict(request.headers)
    forwarded = headers.get("x-forwarded-for", "").split(",")[0].strip()
    client = request.client.host if request.client else None
    return {
        "method": request.method,
        "path": request.url.path,
        "query": {k: request.query_params.getlist(k) for k in request.query_params.keys()},
        "ip": headers.get("cf-connecting-ip") or forwarded or client,
        "headers": headers,
    }


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    data = detect_info(state)
    rows = "".join(
        f"<tr><td>{escape(k)}</td><td>{escape(str(v) if v is not None else '—')}</td></tr>"
        for k, v in data.items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{data["workload"]}</title>
  <style>
    body {{ margin: 0; padding: 48px 16px; font: 16px/1.5 system-ui, sans-serif; }}
    main {{ max-width: 720px; margin: 0 auto; }}
    table {{ border-collapse: collapse; width: 100%; }}
    td {{ padding: 6px 10px; border-bottom: 1px solid #8884; overflow-wrap: anywhere; }}
    td:first-child {{ opacity: 0.7; width: 30%; }}
  </style>
</head>
<body>
  <main>
    <h1>{data["workload"]}</h1>
    <table>{rows}</table>
    <p><a href="api/info">/api/info</a> · <a href="api/echo">/api/echo</a> · <a href="healthz">/healthz</a> · <a href="docs">/docs</a></p>
  </main>
</body>
</html>"""
