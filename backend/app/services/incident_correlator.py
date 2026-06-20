from typing import List, Dict
from app.risk.engine import calculate_risk_scores
from app.ml.anomaly_detector import get_anomalies

_cached_incidents = None

def correlate_incidents():
    global _cached_incidents
    if _cached_incidents is not None:
        return _cached_incidents
    
    risk_scores = calculate_risk_scores()
    anomalies = get_anomalies()

    incident_id_counter = 1
    incidents = []

    # Create a map for fast lookup
    anomaly_map = {a['user_id']: a for a in anomalies}

    for risk in risk_scores:
        user_id = risk['user_id']
        anomaly = anomaly_map.get(user_id)
        
        correlated = False

        incident_alerts = []

        if risk['severity'] in ['CRITICAL', 'HIGH']:
            correlated = True
            incident_alerts.append(f"Risk Score: {risk['risk_score']}")
            for reason in risk['reasons']:
                incident_alerts.append(f"- {reason}")

        if anomaly and anomaly['is_anomaly']:
            correlated = True
            incident_alerts.append(f"ML Anomaly Detected (score: {anomaly['anomaly_score']:.4f})")

        if correlated:
            incidents.append({
                "incident_id": f"INC-{str(incident_id_counter).zfill(4)}",
                "user_id": user_id,
                "user_name": risk['name'],
                "department": risk['department'],
                "severity": risk['severity'],
                "alerts": incident_alerts,
                "status": "OPEN",
                "risk_score": risk['risk_score']
            })
            incident_id_counter +=1

    _cached_incidents = incidents
    return incidents
