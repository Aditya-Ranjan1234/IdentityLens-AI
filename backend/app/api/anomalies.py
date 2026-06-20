from fastapi import APIRouter, Query
from app.ml.anomaly_detector import get_anomalies, train_all_models

router = APIRouter()

@router.get("/")
def get_all_anomalies(model_type: str = Query("isolation_forest", description="Model type: isolation_forest, one_class_svm, local_outlier_factor")):
    return get_anomalies(model_type)

@router.post("/train")
def train_models():
    train_all_models()
    return {"status": "success", "message": "All models trained successfully"}
