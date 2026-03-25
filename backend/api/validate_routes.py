import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator

from graph.runner import run_pipeline
from agents.market_research_agent import run_market_research_agent
from agents.competitor_agent import run_competitor_agent

load_dotenv()

router = APIRouter(prefix="/api/validate")

_executor = ThreadPoolExecutor(max_workers=4)


class ValidateRequest(BaseModel):
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


@router.post("")
async def validate_idea(request: ValidateRequest):
    """
    One-shot synchronous validation. Runs the full LangGraph pipeline in a
    thread executor so FastAPI's event loop is never blocked.
    """
    loop = asyncio.get_event_loop()
    try:
        report = await loop.run_in_executor(_executor, run_pipeline, request.idea)
        return report.model_dump()
    except Exception as exc:
        raise HTTPException(status_code=500, detail={"error": str(exc)})


def _run_quick(idea: str) -> dict:
    """Runs only market + competitor agents synchronously for fast previews."""
    market = run_market_research_agent(idea)
    competitors = run_competitor_agent(idea)
    return {
        "market": market.model_dump(),
        "competitors": competitors.model_dump(),
    }


@router.post("/quick")
async def quick_validate(request: ValidateRequest):
    """
    Lightweight preview endpoint — runs only market research and competitor analysis.
    Skips financial modelling and synthesis so it returns faster.
    """
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(_executor, _run_quick, request.idea)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail={"error": str(exc)})
