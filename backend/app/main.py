from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/test")
def test():
    import os
    return {"file": __file__, "cwd": os.getcwd()}

@app.get("/")
def root():
    return {"message": "IdentityLens AI API"}
