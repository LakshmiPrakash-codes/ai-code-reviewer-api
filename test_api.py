"""
Quick smoke tests — run against local server.
Start server first: uvicorn app.main:app --reload
Then: python test_api.py
"""
import sys
import requests

BASE = "http://localhost:8000"
ok = "\033[92m✓\033[0m"
fail = "\033[91m✗\033[0m"
errors = 0


def check(label, condition, detail=""):
    global errors
    sym = ok if condition else fail
    print(f"  {sym} {label}" + (f"  ({detail})" if detail else ""))
    if not condition:
        errors += 1


# health
print("\n/ health")
r = requests.get(f"{BASE}/health")
check("200", r.status_code == 200)

# swagger
print("\n/ docs")
r = requests.get(f"{BASE}/docs")
check("swagger up", r.status_code == 200)

# validation
print("\n/ validation")
r = requests.post(f"{BASE}/review", json={"code": "x=1", "language": "ruby"})
check("ruby → 400", r.status_code == 400)

r = requests.post(f"{BASE}/review", json={"code": "  ", "language": "python"})
check("blank code → 400", r.status_code == 400)

r = requests.post(f"{BASE}/review", json={})
check("missing fields → 422", r.status_code == 422)

# history (empty)
print("\n/ history")
r = requests.get(f"{BASE}/history")
check("returns list", isinstance(r.json(), list))

# 404
r = requests.get(f"{BASE}/history/99999")
check("missing id → 404", r.status_code == 404)

# live review (needs ANTHROPIC_API_KEY in .env)
print("\n/ review (skipped — add ANTHROPIC_API_KEY to .env to test)")

print(f"\n{'─'*40}")
if errors:
    print(f"  {errors} test(s) failed")
    sys.exit(1)
else:
    print("  all tests passed")
print(f"{'─'*40}\n")
