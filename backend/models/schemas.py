from pydantic import BaseModel, Field
from typing import List, Literal

class StartupInput(BaseModel):
    idea: str

class MarketResearchOutput(BaseModel):
    tam: str
    sam: str
    som: str
    growth_rate: str
    market_summary: str
    key_trends: List[str]

class Competitor(BaseModel):
    name: str
    category: str
    threat_level: Literal["low", "medium", "high"]
    reason: str

class CompetitorAnalysisOutput(BaseModel):
    competitors: List[Competitor]
    total_found: int
    direct_threats: int
    analysis_summary: str

class RevenueScenario(BaseModel):
    year_1: str
    year_2: str
    year_3: str

class FinancialModellingOutput(BaseModel):
    conservative: RevenueScenario
    base: RevenueScenario
    optimistic: RevenueScenario
    key_assumptions: List[str]
    financial_summary: str

class SynthesisOutput(BaseModel):
    viability_score: int = Field(ge=0, le=100)
    market_demand_score: int
    competitive_gap_score: int
    execution_feasibility_score: int
    financial_outlook_score: int
    verdict: str
    recommended_strategy: str
    key_risks: List[str]
    tags: List[str]

class AgentStatus(BaseModel):
    name: str
    status: Literal["queued", "running", "done", "failed"]
    message: str

class FullReport(BaseModel):
    idea: str
    market: MarketResearchOutput
    competitors: CompetitorAnalysisOutput
    financials: FinancialModellingOutput
    synthesis: SynthesisOutput
