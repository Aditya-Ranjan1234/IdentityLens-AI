
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_endpoint(endpoint, method="GET", data=None):
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}/{endpoint}", timeout=30)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}/{endpoint}", json=data, timeout=30)
        response.raise_for_status()
        print(f"[SUCCESS] /{endpoint}: {response.status_code}")
        if len(response.text) < 500:
            print(f"  Response: {response.text[:500]}")
        else:
            print(f"  Response length: {len(response.text)} chars")
        return response.json()
    except Exception as e:
        print(f"[ERROR] /{endpoint}: {str(e)}")
        return None

print("Testing all API endpoints...")
print("=" * 50)

test_endpoint("users")
test_endpoint("risks")
test_endpoint("incidents")
test_endpoint("graph")
test_endpoint("master")
test_endpoint("privileges")
test_endpoint("anomalies")
test_endpoint("metrics")

# Test explanations with sample data
sample_incident = {
    "incident_id": "INC-001",
    "user_id": "U001",
    "user_name": "John Smith",
    "department": "Engineering",
    "severity": "CRITICAL",
    "risk_score": 100,
    "alerts": ["Cross-platform admin", "Offboarding gap"]
}
test_endpoint("explanations", method="POST", data=sample_incident)

print("=" * 50)
print("All tests completed!")
