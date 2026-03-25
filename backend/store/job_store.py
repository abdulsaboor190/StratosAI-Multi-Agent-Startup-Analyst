import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Any, Dict
from pydantic import BaseModel
from models.schemas import AgentStatus, FullReport


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    complete = "complete"
    failed = "failed"


class JobRecord(BaseModel):
    job_id: str
    idea: str
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    agent_statuses: Dict[str, AgentStatus]
    errors: Dict[str, str]
    partial_results: Dict[str, Any]
    final_report: Optional[FullReport] = None


class JobStore:
    def __init__(self):
        self._jobs: Dict[str, JobRecord] = {}

    def create_job(self, idea: str) -> JobRecord:
        job_id = str(uuid.uuid4())
        now = datetime.utcnow()
        agent_names = ["market_research", "competitor", "financial", "synthesis"]
        record = JobRecord(
            job_id=job_id,
            idea=idea,
            status=JobStatus.pending,
            created_at=now,
            updated_at=now,
            agent_statuses={
                name: AgentStatus(name=name, status="queued", message="Waiting to start")
                for name in agent_names
            },
            errors={},
            partial_results={},
            final_report=None,
        )
        self._jobs[job_id] = record
        return record

    def get_job(self, job_id: str) -> Optional[JobRecord]:
        return self._jobs.get(job_id)

    def update_job(self, job_id: str, **kwargs) -> Optional[JobRecord]:
        job = self._jobs.get(job_id)
        if not job:
            return None
        data = job.model_dump()
        data.update(kwargs)
        data["updated_at"] = datetime.utcnow()
        updated = JobRecord(**data)
        self._jobs[job_id] = updated
        return updated

    def update_agent_status(self, job_id: str, agent_name: str, status: str, message: str) -> None:
        job = self._jobs.get(job_id)
        if not job:
            return
        statuses = dict(job.agent_statuses)
        statuses[agent_name] = AgentStatus(name=agent_name, status=status, message=message)
        data = job.model_dump()
        data["agent_statuses"] = statuses
        data["updated_at"] = datetime.utcnow()
        self._jobs[job_id] = JobRecord(**data)

    def set_partial_result(self, job_id: str, agent_name: str, data: dict) -> None:
        job = self._jobs.get(job_id)
        if not job:
            return
        partial = dict(job.partial_results)
        partial[agent_name] = data
        job_data = job.model_dump()
        job_data["partial_results"] = partial
        job_data["updated_at"] = datetime.utcnow()
        self._jobs[job_id] = JobRecord(**job_data)

    def list_jobs(self) -> list:
        return sorted(self._jobs.values(), key=lambda j: j.created_at, reverse=True)

    def delete_job(self, job_id: str) -> bool:
        if job_id in self._jobs:
            del self._jobs[job_id]
            return True
        return False


job_store = JobStore()
