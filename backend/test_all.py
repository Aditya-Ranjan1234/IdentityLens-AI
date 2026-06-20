
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing endpoints...")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("/api/users")
response = client.get("/api/users")
print("Status:", response.status_code)

print("\n/api/risks")
response = client.get("/api/risks")
print("Status:", response.status_code)

print("\n/api/incidents")
response = client.get("/api/incidents")
print("Status:", response.status_code)

print("\n/api/anomalies")
response = client.get("/api/anomalies")
print("Status:", response.status_code)

print("\n/api/metrics")
response = client.get("/api/metrics")
print("Status:", response.status_code)

print("\n/api/graph")
response = client.get("/api/graph")
print("Status:", response.status_code)

print("\nAll tests done!")
