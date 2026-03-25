import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
import json
import time

BASE = "http://localhost:8000"
IDEA = "AI-powered SaaS for remote team collaboration"

passed = 0
total = 7


def _result(name: str, ok: bool, detail: str = ""):
    global passed
    status = "✓ PASS" if ok else "✗ FAIL"
    print(f"  [{status}] {name}{': ' + detail if detail else ''}")
    if ok:
        passed += 1


# ── Test 1 ────────────────────────────────────────────────────────────────────
def test_health():
    try:
        r = httpx.get(f"{BASE}/health", timeout=10)
        ok = r.status_code == 200 and r.json().get("status") == "ok"
        _result("test_health", ok, f"status={r.status_code}")
    except Exception as e:
        _result("test_health", False, str(e))


# ── Test 2 ────────────────────────────────────────────────────────────────────
def test_create_job() -> str | None:
    try:
        r = httpx.post(f"{BASE}/api/jobs", json={"idea": IDEA}, timeout=10)
        ok = r.status_code == 201 and "job_id" in r.json()
        job_id = r.json().get("job_id") if ok else None
        _result("test_create_job", ok, f"job_id={job_id}")
        return job_id
    except Exception as e:
        _result("test_create_job", False, str(e))
        return None


# ── Test 3 ────────────────────────────────────────────────────────────────────
def test_get_job(job_id: str):
    try:
        r = httpx.get(f"{BASE}/api/jobs/{job_id}", timeout=10)
        ok = r.status_code == 200
        status = r.json().get("status", "?") if ok else "?"
        _result("test_get_job", ok, f"status={status}")
    except Exception as e:
        _result("test_get_job", False, str(e))


# ── Test 4 ────────────────────────────────────────────────────────────────────
def test_stream_job(job_id: str):
    try:
        deadline = time.time() + 120
        received_done = False
        with httpx.stream("GET", f"{BASE}/api/jobs/{job_id}/stream", timeout=130) as r:
            for line in r.iter_lines():
                if time.time() > deadline:
                    print("    [stream] timeout reached")
                    break
                if line.startswith("data:"):
                    raw = line[5:].strip()
                    if not raw:
                        continue
                    try:
                        evt = json.loads(raw)
                    except Exception:
                        evt = {}
                    evt_type = evt.get("type", "")
                    print(f"    [stream] event type={evt_type}")
                    if evt_type == "done":
                        received_done = True
                        break
        _result("test_stream_job", received_done, "received done sentinel" if received_done else "no done received")
    except Exception as e:
        _result("test_stream_job", False, str(e))


# ── Test 5 ────────────────────────────────────────────────────────────────────
def test_get_report(job_id: str):
    try:
        r = httpx.get(f"{BASE}/api/jobs/{job_id}/report", timeout=10)
        if r.status_code == 200:
            data = r.json()
            score = data.get("synthesis", {}).get("viability_score", "?")
            verdict = data.get("synthesis", {}).get("verdict", "?")
            _result("test_get_report", True, f"score={score} verdict={verdict}")
        elif r.status_code == 202:
            _result("test_get_report", True, "not ready (202 accepted)")
        else:
            _result("test_get_report", False, f"status={r.status_code}")
    except Exception as e:
        _result("test_get_report", False, str(e))


# ── Test 6 ────────────────────────────────────────────────────────────────────
def test_delete_job(job_id: str):
    try:
        r = httpx.delete(f"{BASE}/api/jobs/{job_id}", timeout=10)
        _result("test_delete_job", r.status_code == 204, f"status={r.status_code}")
    except Exception as e:
        _result("test_delete_job", False, str(e))


# ── Test 7 ────────────────────────────────────────────────────────────────────
def test_invalid_idea():
    try:
        r = httpx.post(f"{BASE}/api/jobs", json={"idea": "hi"}, timeout=10)
        _result("test_invalid_idea", r.status_code == 422, f"status={r.status_code}")
    except Exception as e:
        _result("test_invalid_idea", False, str(e))


# ── Runner ────────────────────────────────────────────────────────────────────
def main():
    print("\n" + "=" * 50)
    print("  VentureScope AI — API Test Suite")
    print("=" * 50 + "\n")

    test_health()
    job_id = test_create_job()

    if job_id:
        test_get_job(job_id)
        test_stream_job(job_id)   # blocks until pipeline finishes (~60–90 s)
        test_get_report(job_id)
        test_delete_job(job_id)
    else:
        for name in ["test_get_job", "test_stream_job", "test_get_report", "test_delete_job"]:
            _result(name, False, "skipped — no job_id")

    test_invalid_idea()

    print(f"\n{'=' * 50}")
    print(f"  Result: {passed}/{total} tests passed")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
