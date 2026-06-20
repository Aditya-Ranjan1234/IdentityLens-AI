from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.api import users, risks, incidents, graph, master, privileges, anomalies, explanations, metrics, offboarding, reports

app = FastAPI(title="IdentityLens AI", version="1.0.0")

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

# Frontend static files (check both possible relative paths for single-space and local dev)
def get_frontend_path(suffix):
    paths = [
        os.path.join(os.path.dirname(__file__), "../../frontend", suffix),
        os.path.join(os.path.dirname(__file__), "../../../frontend", suffix),
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return None

frontend_dist = get_frontend_path(".next/standalone")
frontend_public = get_frontend_path("public")
frontend_static = get_frontend_path(".next/static")

if os.path.exists(frontend_dist):
    if os.path.exists(frontend_static):
        app.mount("/_next/static", StaticFiles(directory=frontend_static), name="next-static")
    if os.path.exists(frontend_public):
        app.mount("/public", StaticFiles(directory=frontend_public), name="public")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        html_path = os.path.join(frontend_dist, "server", "index.html")
        if os.path.exists(html_path):
            return FileResponse(html_path)
        return {"message": "IdentityLens AI API"}

@app.get("/test")
def test():
    import os
    return {"file": __file__, "cwd": os.getcwd()}
