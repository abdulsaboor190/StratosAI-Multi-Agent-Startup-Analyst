import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from utils.helpers import build_tavily_tool, build_groq_llm, parse_json_from_llm
from utils.relevance_filter import filter_search_results, truncate_results_to_context
from utils.timeout_wrapper import run_with_retry
from models.schemas import MarketResearchOutput

load_dotenv()

def _run_market_research_agent_impl(idea: str) -> MarketResearchOutput:
    tavily = build_tavily_tool()
    llm = build_groq_llm()
    
    # Run with retry
    search1_raw = run_with_retry(tavily.invoke, {"query": f"{idea} market size TAM 2024"}, timeout_seconds=30, max_retries=2)
    search2_raw = run_with_retry(tavily.invoke, {"query": f"{idea} industry growth trends"}, timeout_seconds=30, max_retries=2)
        
    filtered_s1 = filter_search_results(search1_raw, idea, "market size and TAM")
    filtered_s2 = filter_search_results(search2_raw, idea, "industry growth trends")
    
    context = truncate_results_to_context(filtered_s1 + filtered_s2)
    
    prompt = f"""
You are an expert market research analyst. Analyze the following context about the startup idea "{idea}".
Context:
{context}

Based on the context, provide a detailed market research analysis.
You MUST return ONLY a JSON object exactly matching the following fields and types. 
IMPORTANT RULES:
- All fields are required. No nulls.
- All monetary values must include a unit (e.g. "$4.2B", "$500M", not "4.2").
- Percentages must include % (e.g. "15% CAGR").
- Do not include any extra text, preamble, or explanation.

Fields:
- tam: string (Total Addressable Market size, eg "$10B")
- sam: string (Serviceable Addressable Market size, eg "$2B")
- som: string (Serviceable Obtainable Market size, eg "$100M")
- growth_rate: string (eg "15% CAGR")
- market_summary: string (brief summary)
- key_trends: list of strings (eg ["AI integration", "Remote work"])

Respond with the JSON object exactly formulated:
"""
    
    def _call_llm():
        response = llm.invoke(prompt)
        return parse_json_from_llm(response.content)

    parsed_json = run_with_retry(_call_llm, timeout_seconds=45, max_retries=2)
    return MarketResearchOutput(**parsed_json)

def run_market_research_agent(idea: str) -> MarketResearchOutput:
    try:
        return _run_market_research_agent_impl(idea)
    except Exception as e:
        print(f"MarketResearchAgent ultimate failure: {e}")
        return MarketResearchOutput(
            tam="Data unavailable — LLM timeout",
            sam="Data unavailable — LLM timeout",
            som="Data unavailable — LLM timeout",
            growth_rate="Data unavailable — LLM timeout",
            market_summary="Data unavailable — LLM timeout",
            key_trends=["Unable to retrieve trends"]
        )

if __name__ == "__main__":
    idea = "AI-powered SaaS for remote team collaboration"
    result = run_market_research_agent(idea)
    print(result.model_dump_json(indent=2))
