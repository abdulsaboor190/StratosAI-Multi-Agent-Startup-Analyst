import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

import time
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api import job_routes, validate_routes
from store.job_store import job_store, JobStatus

app = FastAPI(
    title="StratosAI",
    version="3.0",
    description="Multi-Agent Startup Validator API",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request logging middleware ─────────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 1)
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {request.method} {request.url.path} → {response.status_code} ({duration}ms)")
    return response

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(job_routes.router)
app.include_router(validate_routes.router)

# ── Core endpoints ────────────────────────────────────────────────────────────
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "project": "StratosAI",
        "phase": 6,
        "timestamp": datetime.utcnow().isoformat(),
    }

@app.get("/")
def read_root():
    return {"message": "StratosAI API is running", "docs": "/docs"}

@app.get("/api/jobs-summary")
def jobs_summary():
    all_jobs = job_store.list_jobs()
    counts = {s.value: 0 for s in JobStatus}
    for job in all_jobs:
        counts[job.status.value] += 1
    return {
        "total_jobs": len(all_jobs),
        **counts,
    }

# ── Startup event ─────────────────────────────────────────────────────────────
@app.on_event("startup")
async def on_startup():
    print("=" * 50)
    print("  StratosAI API started — Phase 6")
    print("=" * 50)
    routes = [f"  {r.methods} {r.path}" for r in app.routes if hasattr(r, "methods")]
    for r in routes:
        print(r)
    print("=" * 50)
