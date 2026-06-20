from fastapi import APIRouter
from app.risk.engine import calculate_risk_scores
import pandas as pd
import os

router = APIRouter()
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')

@router.get("/")
def get_all_risks():
    scores = calculate_risk_scores()
    return scores
