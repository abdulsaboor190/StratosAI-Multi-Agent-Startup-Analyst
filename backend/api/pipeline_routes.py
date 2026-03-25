import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException, Query
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import json
import asyncio

from graph.runner import run_pipeline, stream_pipeline

load_dotenv()

router = APIRouter()

class ValidateRequest(BaseModel):
    idea: str

@router.post("/validate")
def validate_idea(request: ValidateRequest):
    try:
        report = run_pipeline(request.idea)
        return report.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def async_stream_generator(idea: str):
    try:
        loop = asyncio.get_running_loop()
        stream_iter = iter(stream_pipeline(idea))
        
        while True:
            try:
                chunk = await loop.run_in_executor(None, next, stream_iter)
            except StopIteration:
                break
                
            payload = {}
            if chunk["node"]: payload["node"] = chunk["node"]
            payload["partial_data"] = chunk["partial_data"]
            
            if chunk["agent_statuses"]:
                payload["agent_statuses"] = {k: v.model_dump() for k, v in chunk["agent_statuses"].items()}
            
            if chunk["final_report"]:
                payload["final_report"] = chunk["final_report"].model_dump()
                yield {
                    "event": "complete",
                    "data": json.dumps(payload)
                }
            else:
                yield {
                    "event": "agent_update",
                    "data": json.dumps(payload)
                }
                
        yield {
            "event": "done",
            "data": "{}"
        }
            
    except Exception as e:
        yield {
            "event": "error",
            "data": json.dumps({"error": str(e)})
        }

@router.get("/validate/stream")
async def stream_validate_idea(idea: str = Query(..., description="The startup idea to validate")):
    return EventSourceResponse(async_stream_generator(idea))
