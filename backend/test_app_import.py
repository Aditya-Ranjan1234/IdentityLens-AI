import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")
try:
    from app.main import app
    print("Successfully imported app!")
except Exception as e:
    print(f"Failed to import app: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting users endpoint...")
try:
    from app.api.users import get_all_users
    users = get_all_users()
    print(f"Got users! Count: {len(users)}")
except Exception as e:
    print(f"Failed to get users: {e}")
    import traceback
    traceback.print_exc()
