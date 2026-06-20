from fastapi import APIRouter
from app.services.incident_correlator import correlate_incidents

router = APIRouter()

@router.get("/")
def get_all_incidents():
    return correlate_incidents()
