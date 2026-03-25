import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from utils.helpers import build_groq_llm, parse_json_from_llm
from utils.timeout_wrapper import run_with_retry
from models.schemas import SynthesisOutput, MarketResearchOutput, CompetitorAnalysisOutput, FinancialModellingOutput

load_dotenv()

def _run_synthesis_agent_impl(idea: str, market: MarketResearchOutput, competitors: CompetitorAnalysisOutput, financials: FinancialModellingOutput) -> SynthesisOutput:
    llm = build_groq_llm()
    
    context = f"""
Idea: {idea}

--- MARKET ANALYSIS ---
TAM: {market.tam} | SAM: {market.sam} | SOM: {market.som} | Growth: {market.growth_rate}
Summary: {market.market_summary}
Trends: {", ".join(market.key_trends)}

--- COMPETITOR ANALYSIS ---
Total Found: {competitors.total_found} | Direct Threats: {competitors.direct_threats}
Summary: {competitors.analysis_summary}

--- FINANCIAL SCENARIOS ---
Conservative Y3: {financials.conservative.year_3}
Base Y3: {financials.base.year_3}
Optimistic Y3: {financials.optimistic.year_3}
Summary: {financials.financial_summary}
Assumptions: {", ".join(financials.key_assumptions)}
"""
    
    prompt = f"""
You are an expert startup analyst. Synthesize the following outputs from market research, competitive analysis, and financial modeling for the idea "{idea}".
Context:
{context}

Based on this synthesis, score the idea across 4 dimensions (0-100), compute an overall viability_score, and write a verdict and recommended strategy.
You MUST return ONLY a JSON object matching exactly the fields below.
IMPORTANT RULES:
- All score fields must be integers between 0 and 100 inclusive.
- viability_score must equal round((market_demand_score + competitive_gap_score + execution_feasibility_score + financial_outlook_score) / 4).
- key_risks must be an array of 3 to 5 strings.
- tags must be an array of 3 to 6 single-word or hyphenated strings.
- All fields are required. No nulls.
- Do not include any extra text, preamble, or explanation.

Fields:
- viability_score: int
- market_demand_score: int
- competitive_gap_score: int
- execution_feasibility_score: int
- financial_outlook_score: int
- verdict: string
- recommended_strategy: string
- key_risks: list of strings
- tags: list of strings

Respond with the JSON object exactly formulated:
"""
    
    def _call_llm():
        response = llm.invoke(prompt)
        return parse_json_from_llm(response.content)

    parsed_json = run_with_retry(_call_llm, timeout_seconds=60, max_retries=2)
    return SynthesisOutput(**parsed_json)

def run_synthesis_agent(idea: str, market: MarketResearchOutput, competitors: CompetitorAnalysisOutput, financials: FinancialModellingOutput) -> SynthesisOutput:
    try:
        return _run_synthesis_agent_impl(idea, market, competitors, financials)
    except Exception as e:
        print(f"SynthesisAgent ultimate failure: {e}")
        return SynthesisOutput(
            viability_score=0,
            market_demand_score=0,
            competitive_gap_score=0,
            execution_feasibility_score=0,
            financial_outlook_score=0,
            verdict="Analysis unavailable due to timeout",
            recommended_strategy="Please retry the analysis",
            key_risks=["Synthesis agent timed out"],
            tags=["error"]
        )

if __name__ == "__main__":
    pass
