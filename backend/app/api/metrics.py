from fastapi import APIRouter
import pandas as pd
import os
from app.risk.engine import calculate_risk_scores
from app.ml.anomaly_detector import get_anomalies

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
_cached_metrics = None
_cached_users_df = None

def _get_users_df():
    global _cached_users_df
    if _cached_users_df is None:
        _cached_users_df = pd.read_csv(os.path.join(DATA_DIR, "users.csv"))
    return _cached_users_df

@router.get("/")
def get_metrics():
    global _cached_metrics
    if _cached_metrics is not None:
        return _cached_metrics
    try:
        users_df = _get_users_df()
        risks = calculate_risk_scores()
        anomalies = get_anomalies()

        critical_count = sum(1 for r in risks if r["severity"] == "CRITICAL")
        high_count = sum(1 for r in risks if r["severity"] == "HIGH")
        medium_count = sum(1 for r in risks if r["severity"] == "MEDIUM")
        low_count = sum(1 for r in risks if r["severity"] == "LOW")
        anomaly_count = sum(1 for a in anomalies if a["is_anomaly"])
        offboarding_count = sum(1 for r in risks if any("Offboarding" in reason for reason in r["reasons"]))

        _cached_metrics = {
            "total_users": len(users_df),
            "risk_distribution": {
                "CRITICAL": critical_count,
                "HIGH": high_count,
                "MEDIUM": medium_count,
                "LOW": low_count
            },
            "ml_anomalies": anomaly_count,
            "offboarding_gaps": offboarding_count,
            "avg_risk_score": sum(r["risk_score"] for r in risks) / len(risks) if risks else 0
        }
        return _cached_metrics
    except Exception as e:
        return {"error": str(e)}
