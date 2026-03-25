import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from utils.helpers import build_tavily_tool, build_groq_llm, parse_json_from_llm
from utils.relevance_filter import filter_search_results, truncate_results_to_context
from utils.timeout_wrapper import run_with_retry
from models.schemas import CompetitorAnalysisOutput

load_dotenv()

def _run_competitor_agent_impl(idea: str) -> CompetitorAnalysisOutput:
    tavily = build_tavily_tool()
    llm = build_groq_llm()
    
    search_raw = run_with_retry(tavily.invoke, {"query": f"{idea} competitors and alternative products"}, timeout_seconds=30, max_retries=2)
    filtered = filter_search_results(search_raw, idea, "competitors and alternative products")
    context = truncate_results_to_context(filtered)
    
    prompt = f"""
You are an expert startup competitor analyst. Analyze the following context about the startup idea "{idea}".
Context:
{context}

Based on the context, provide a detailed competitor analysis.
You MUST return ONLY a JSON object exactly matching the following fields and types.
IMPORTANT RULES:
- All fields are required. No nulls.
- threat_level must be EXACTLY the string "low", "medium", or "high" — no other values.
- competitors must be an array of at least 1 and at most 8 objects.
- total_found must equal competitors.length.
- direct_threats must be the count of competitors with threat_level equal to "high".
- Do not include any extra text, preamble, or explanation.

Fields:
- competitors: array of objects with fields:
    - name: string
    - category: string
    - threat_level: string ("low", "medium", or "high")
    - reason: string
- total_found: int
- direct_threats: int
- analysis_summary: string

Respond with the JSON object exactly formulated:
"""
    
    def _call_llm():
        response = llm.invoke(prompt)
        return parse_json_from_llm(response.content)

    parsed_json = run_with_retry(_call_llm, timeout_seconds=45, max_retries=2)
    return CompetitorAnalysisOutput(**parsed_json)

def run_competitor_agent(idea: str) -> CompetitorAnalysisOutput:
    try:
        return _run_competitor_agent_impl(idea)
    except Exception as e:
        print(f"CompetitorAgent ultimate failure: {e}")
        return CompetitorAnalysisOutput(
            competitors=[],
            total_found=0,
            direct_threats=0,
            analysis_summary="Competitor data unavailable due to timeout"
        )

if __name__ == "__main__":
    idea = "AI-powered SaaS for remote team collaboration"
    result = run_competitor_agent(idea)
    print(result.model_dump_json(indent=2))
