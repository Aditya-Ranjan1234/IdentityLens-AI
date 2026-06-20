
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import csv
import json
from io import StringIO
import os
import pandas as pd
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')

router = APIRouter()

@router.get("/export/csv")
def export_csv_report(report_type: str = Query("risks", description="Report type: risks, users, anomalies, incidents")):
    output = StringIO()
    writer = csv.writer(output)
    
    if report_type == "users":
        users_df = pd.read_csv(os.path.join(DATA_DIR, "users.csv"))
        writer.writerow(users_df.columns.tolist())
        for _, row in users_df.iterrows():
            writer.writerow(row.tolist())
    elif report_type == "risks":
        from app.api.privileges import get_all_privileges
        all_risks = get_all_privileges()
        if all_risks:
            writer.writerow(["user_id", "privilege_score", "is_admin", "effective_permissions", "roles", "groups"])
            for risk in all_risks:
                writer.writerow([
                    risk["user_id"],
                    risk["privilege_score"],
                    str(risk["is_admin"]),
                    ", ".join(risk["effective_permissions"]),
                    ", ".join(risk["roles"]),
                    ", ".join(risk["groups"])
                ])
    elif report_type == "anomalies":
        from app.ml.anomaly_detector import get_anomalies
        anomalies = get_anomalies()
        writer.writerow(["user_id", "is_anomaly", "anomaly_score", "login_count", "platform_count", "resource_count", "country_count", "hour_variance"])
        for a in anomalies:
            writer.writerow([
                a["user_id"],
                str(a["is_anomaly"]),
                a["anomaly_score"],
                a["features"]["login_count"],
                a["features"]["platform_count"],
                a["features"]["resource_count"],
                a["features"]["country_count"],
                a["features"]["hour_variance"]
            ])
    elif report_type == "incidents":
        from app.api.incidents import get_incidents
        incidents = get_incidents()
        writer.writerow(["incident_id", "user_id", "title", "severity", "status", "alerts_count", "created_at"])
        for inc in incidents:
            writer.writerow([
                inc["incident_id"],
                inc["user_id"],
                inc["title"],
                inc["severity"],
                inc["status"],
                len(inc["alerts"]),
                inc["created_at"]
            ])
    
    output.seek(0)
    filename = f"{report_type}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@router.get("/export/json")
def export_json_report(report_type: str = Query("risks", description="Report type: risks, users, anomalies, incidents")):
    report_data = {}
    if report_type == "users":
        users_df = pd.read_csv(os.path.join(DATA_DIR, "users.csv"))
        report_data = users_df.to_dict(orient="records")
    elif report_type == "risks":
        from app.api.privileges import get_all_privileges
        report_data = get_all_privileges()
    elif report_type == "anomalies":
        from app.ml.anomaly_detector import get_anomalies
        report_data = get_anomalies()
    elif report_type == "incidents":
        from app.api.incidents import get_incidents
        report_data = get_incidents()
    
    output = StringIO()
    json.dump(report_data, output, indent=2)
    output.seek(0)
    filename = f"{report_type}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    return StreamingResponse(output, media_type="application/json", headers={"Content-Disposition": f'attachment; filename="{filename}"'})

