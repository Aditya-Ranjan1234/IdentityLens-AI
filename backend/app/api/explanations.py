from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_explainer import explain_risk

router = APIRouter()

class IncidentRequest(BaseModel):
    incident_id: str
    user_id: str
    user_name: str
    department: str
    severity: str
    risk_score: int
    alerts: list

@router.post("/")
def get_explanation(incident: IncidentRequest):
    return explain_risk(incident.model_dump())
