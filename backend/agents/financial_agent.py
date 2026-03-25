import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from utils.helpers import build_groq_llm, parse_json_from_llm
from utils.timeout_wrapper import run_with_retry
from models.schemas import FinancialModellingOutput, MarketResearchOutput

load_dotenv()

def _run_financial_agent_impl(idea: str, market: MarketResearchOutput) -> FinancialModellingOutput:
    llm = build_groq_llm()
    
    context = f"""
Idea: {idea}
Market Context:
TAM: {market.tam} | SAM: {market.sam} | SOM: {market.som}
Growth Rate: {market.growth_rate}
Market Summary: {market.market_summary}
Trends: {", ".join(market.key_trends)}
"""
    
    prompt = f"""
You are an expert startup financial modeler. Analyze the following context about the startup idea "{idea}".
Context:
{context}

Based on the market data, provide a 3-year revenue financial projection in 3 scenarios (conservative, base, optimistic).
You MUST return ONLY a JSON object exactly matching the following fields and types.
IMPORTANT RULES:
- All revenue values must be strings in format "$X.XM" or "$X.XK" or "$X.XB" — always with dollar sign and unit suffix.
- key_assumptions must be an array of exactly 3 to 5 strings.
- All fields are required. No nulls.
- Do not include any extra text, preamble, or explanation.

Fields:
- conservative: object with string fields year_1, year_2, year_3
- base: object with string fields year_1, year_2, year_3
- optimistic: object with string fields year_1, year_2, year_3
- key_assumptions: list of strings (exactly 3 to 5)
- financial_summary: string

Respond with the JSON object exactly formulated:
"""
    
    def _call_llm():
        response = llm.invoke(prompt)
        return parse_json_from_llm(response.content)

    parsed_json = run_with_retry(_call_llm, timeout_seconds=45, max_retries=2)
    return FinancialModellingOutput(**parsed_json)

def run_financial_agent(idea: str, market: MarketResearchOutput) -> FinancialModellingOutput:
    try:
        return _run_financial_agent_impl(idea, market)
    except Exception as e:
        print(f"FinancialAgent ultimate failure: {e}")
        zero_scen = {"year_1": "$0 — data unavailable", "year_2": "$0 — data unavailable", "year_3": "$0 — data unavailable"}
        return FinancialModellingOutput(
            conservative=zero_scen,
            base=zero_scen,
            optimistic=zero_scen,
            key_assumptions=["Financial projection unavailable due to LLM timeout"],
            financial_summary="Data unavailable due to timeout"
        )

if __name__ == "__main__":
    idea = "AI-powered SaaS for remote team collaboration"
    dummy_market = MarketResearchOutput(tam="$10B", sam="$2B", som="$100M", growth_rate="15%", market_summary="growing", key_trends=["AI"])
    result = run_financial_agent(idea, dummy_market)
    print(result.model_dump_json(indent=2))
