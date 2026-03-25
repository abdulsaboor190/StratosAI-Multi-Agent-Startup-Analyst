from typing import TypedDict, Optional, Dict
from models.schemas import (
    MarketResearchOutput, 
    CompetitorAnalysisOutput, 
    FinancialModellingOutput, 
    SynthesisOutput, 
    AgentStatus, 
    FullReport
)

class VentureScopeState(TypedDict):
    idea: str
    market: Optional[MarketResearchOutput]
    competitors: Optional[CompetitorAnalysisOutput]
    financials: Optional[FinancialModellingOutput]
    synthesis: Optional[SynthesisOutput]
    agent_statuses: Dict[str, AgentStatus]
    errors: Dict[str, str]
    retry_counts: Dict[str, int]
    final_report: Optional[FullReport]

def create_initial_state(idea: str) -> VentureScopeState:
    return {
        "idea": idea,
        "market": None,
        "competitors": None,
        "financials": None,
        "synthesis": None,
        "agent_statuses": {
            "market_research": AgentStatus(name="market_research", status="queued", message="Waiting to start"),
            "competitor": AgentStatus(name="competitor", status="queued", message="Waiting to start"),
            "financial": AgentStatus(name="financial", status="queued", message="Waiting to start"),
            "synthesis": AgentStatus(name="synthesis", status="queued", message="Waiting to start"),
            "assemble_report": AgentStatus(name="assemble_report", status="queued", message="Waiting to start")
        },
        "errors": {},
        "retry_counts": {
            "market_research": 0,
            "competitor": 0,
            "financial": 0,
            "synthesis": 0,
            "assemble_report": 0
        },
        "final_report": None
    }
