from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import os
import logging
from app.api import users, risks, incidents, graph, master, privileges, anomalies, explanations, metrics, offboarding, reports

logger = logging.getLogger("identitylens")

app = FastAPI(title="IdentityLens AI", version="1.0.0", redirect_slashes=False)

@app.on_event("startup")
async def startup_event():
    """Pre-train ML models on startup so the first API request never blocks."""
    try:
        from app.ml.anomaly_detector import _ensure_models
        logger.info("Pre-training / verifying ML models...")
        _ensure_models()
        logger.info("ML models ready.")
    except Exception as exc:
        logger.error(f"Startup model training failed (will retry on first request): {exc}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(risks.router, prefix="/api/risks", tags=["risks"])
app.include_router(incidents.router, prefix="/api/incidents", tags=["incidents"])
app.include_router(graph.router, prefix="/api/graph", tags=["graph"])
app.include_router(master.router, prefix="/api/master", tags=["master identities"])
app.include_router(privileges.router, prefix="/api/privileges", tags=["effective privileges"])
app.include_router(anomalies.router, prefix="/api/anomalies", tags=["ml anomalies"])
app.include_router(explanations.router, prefix="/api/explanations", tags=["llm explanations"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(offboarding.router, prefix="/api/offboarding", tags=["offboarding gaps"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

# Frontend static files — safely resolve paths (handle None when path not found)
def get_frontend_path(suffix):
    paths = [
        os.path.join(os.path.dirname(__file__), "../../frontend", suffix),
        os.path.join(os.path.dirname(__file__), "../../../frontend", suffix),
        os.path.join("/app/frontend", suffix),
    ]
    for path in paths:
        norm = os.path.normpath(path)
        if os.path.exists(norm):
            return norm
    return None

frontend_standalone = get_frontend_path(".next/standalone")
frontend_public = get_frontend_path("public")
frontend_static = get_frontend_path(".next/static")

_frontend_available = frontend_standalone is not None

if _frontend_available:
    # Mount Next.js static assets
    if frontend_static and os.path.exists(frontend_static):
        app.mount("/_next/static", StaticFiles(directory=frontend_static), name="next-static")
    if frontend_public and os.path.exists(frontend_public):
        app.mount("/public", StaticFiles(directory=frontend_public), name="public")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str):
        # Don't intercept /api routes (they are registered before this catch-all)
        # Try to serve the Next.js standalone index
        html_path = os.path.join(frontend_standalone, "server", "app", "index.html")
        # Fallback paths for different Next.js versions
        fallback_paths = [
            os.path.join(frontend_standalone, "server", "app", "index.html"),
            os.path.join(frontend_standalone, "server", "pages", "index.html"),
            os.path.join(frontend_standalone, "index.html"),
        ]
        for p in fallback_paths:
            if os.path.exists(p):
                return FileResponse(p)
        # Last resort: return a minimal redirect page
        return HTMLResponse(
            content="<html><head><meta http-equiv='refresh' content='0;url=/'></head><body>Loading...</body></html>",
            status_code=200
        )

else:
    # No frontend built — serve a status page so HF Spaces health check passes
    @app.get("/", include_in_schema=False)
    async def root():
        return HTMLResponse(
            content="""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IdentityLens AI</title>
  <style>
    body { font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0;
           display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
    .card { background: #1e293b; border-radius: 12px; padding: 48px; text-align: center; max-width: 480px; }
    h1 { color: #38bdf8; margin: 0 0 12px; font-size: 2rem; }
    p  { color: #94a3b8; margin: 0 0 24px; }
    a  { display: inline-block; background: #0ea5e9; color: #fff; text-decoration: none;
         border-radius: 8px; padding: 12px 28px; font-weight: 600; }
    a:hover { background: #38bdf8; }
  </style>
</head>
<body>
  <div class="card">
    <h1>🔐 IdentityLens AI</h1>
    <p>Identity Sprawl Detection &amp; Risk Intelligence Platform</p>
    <a href="/docs">View API Docs →</a>
  </div>
</body>
</html>""",
            status_code=200
        )

@app.get("/health", include_in_schema=False)
@app.get("/healthz", include_in_schema=False)
def health():
    return {"status": "ok", "service": "IdentityLens AI"}

@app.get("/test")
def test():
    return {
        "file": __file__,
        "cwd": os.getcwd(),
        "frontend_standalone": frontend_standalone,
        "frontend_available": _frontend_available
    }
