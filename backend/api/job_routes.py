import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Response
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv

from store.job_store import job_store, JobStatus
from store.event_bus import event_bus
from graph.async_runner import run_pipeline_for_job

load_dotenv()

router = APIRouter(prefix="/api/jobs")


class CreateJobRequest(BaseModel):
    idea: str

    @field_validator("idea")
    @classmethod
    def validate_idea(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Idea must be at least 10 characters long.")
        if len(v) > 500:
            raise ValueError("Idea must be at most 500 characters long.")
        return v


@router.post("", status_code=201)
async def create_job(request: CreateJobRequest, background_tasks: BackgroundTasks):
    job = job_store.create_job(request.idea)
    background_tasks.add_task(run_pipeline_for_job, job.job_id, request.idea)
    return {
        "job_id": job.job_id,
        "status": "pending",
        "message": "Pipeline started",
    }


@router.get("/{job_id}")
async def get_job(job_id: str):
    job = job_store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail={"error": "Job not found"})
    return job.model_dump()


@router.get("/{job_id}/status")
async def get_job_status(job_id: str):
    job = job_store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail={"error": "Job not found"})
    return {
        "job_id": job.job_id,
        "status": job.status,
        "agent_statuses": {k: v.model_dump() for k, v in job.agent_statuses.items()},
        "updated_at": job.updated_at.isoformat(),
    }


@router.get("/{job_id}/report")
async def get_job_report(job_id: str):
    job = job_store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail={"error": "Job not found"})
    if job.final_report is None:
        return JSONResponse(
            status_code=202,
            content={"message": "Report not ready yet", "status": job.status},
        )
    return job.final_report.model_dump()


@router.get("/{job_id}/stream")
async def stream_job(job_id: str):
    job = job_store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail={"error": "Job not found"})

    async def event_generator():
        queue = event_bus.subscribe(job_id)
        try:
            # If job is already done or failed, immediately emit final state then close
            if job.status in (JobStatus.complete, JobStatus.failed):
                if job.final_report:
                    yield {
                        "event": "complete",
                        "data": json.dumps({"type": "complete", "final_report": job.final_report.model_dump()}),
                    }
                else:
                    yield {
                        "event": "error",
                        "data": json.dumps({"type": "error", "message": "Job failed without a report."}),
                    }
                yield {"event": "done", "data": json.dumps({"type": "done"})}
                return

            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=120.0)
                except asyncio.TimeoutError:
                    yield {"event": "timeout", "data": json.dumps({"message": "Stream timed out"})}
                    break

                event_type = event.get("type", "agent_update")

                if event_type == "done":
                    yield {"event": "done", "data": json.dumps({"type": "done"})}
                    break
                elif event_type == "complete":
                    yield {"event": "complete", "data": json.dumps(event)}
                elif event_type == "error":
                    yield {"event": "error", "data": json.dumps(event)}
                else:
                    yield {"event": "agent_update", "data": json.dumps(event)}

        finally:
            # Always clean up so queues don't leak if the client disconnects
            event_bus.unsubscribe(job_id, queue)

    return EventSourceResponse(event_generator())


@router.get("")
async def list_jobs(limit: int = Query(default=20, ge=1, le=100)):
    jobs = job_store.list_jobs()[:limit]
    return [j.model_dump() for j in jobs]


@router.delete("/{job_id}", status_code=204)
async def delete_job(job_id: str):
    deleted = job_store.delete_job(job_id)
    if not deleted:
        raise HTTPException(status_code=404, detail={"error": "Job not found"})
    return Response(status_code=204)
