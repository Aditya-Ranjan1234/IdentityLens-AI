import requests

def test_endpoint(endpoint):
    try:
        response = requests.get(f"http://localhost:8000{endpoint}", timeout=30)
        print(f"\n=== {endpoint} ===")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"Data count: {len(data)}")
                if data:
                    print(f"First item: {data[0]}")
            else:
                print(f"Data: {data}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"\n=== {endpoint} ===")
        print(f"Exception: {e}")
        return False

endpoints = [
    "/api/users",
    "/api/risks",
    "/api/incidents",
    "/api/anomalies",
    "/api/metrics",
    "/api/graph"
]

all_passed = True
for endpoint in endpoints:
    passed = test_endpoint(endpoint)
    if not passed:
        all_passed = False

print(f"\nAll passed: {all_passed}")
