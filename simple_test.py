
import requests
import time

BASE_URL = "http://127.0.0.1:8000/api"

def test_single_endpoint(endpoint):
    print(f"\nTesting /{endpoint}...")
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", timeout=60)
        elapsed = time.time() - start
        print(f"  Status: {response.status_code} (took {elapsed:.2f}s)")
        print(f"  Response length: {len(response.text)} chars")
        return True
    except Exception as e:
        elapsed = time.time() - start
        print(f"  Failed after {elapsed:.2f}s: {e}")
        return False

# Test each endpoint
test_single_endpoint("users")
test_single_endpoint("risks")
test_single_endpoint("incidents")
test_single_endpoint("graph")
test_single_endpoint("master")
test_single_endpoint("privileges")
test_single_endpoint("anomalies")
test_single_endpoint("metrics")
