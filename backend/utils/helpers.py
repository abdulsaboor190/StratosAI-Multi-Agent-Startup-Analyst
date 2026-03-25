import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

def parse_json_from_llm(text: str) -> dict:
    text = text.strip()
    # Strip markdown code fences if present
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    
    # Strip any preamble before the first {
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx == -1 or end_idx == -1:
        raise ValueError(f"No JSON object found in response:\n{text}")
        
    json_str = text[start_idx : end_idx + 1]
    
    try:
        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON. Error: {e}\nRaw extracted text:\n{json_str}")

def build_groq_llm() -> ChatGroq:
    """Returns a ChatGroq instance using llama-3.1-8b-instant."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment.")
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=api_key
    )

def build_tavily_tool() -> TavilySearchResults:
    """Returns a TavilySearchResults instance."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment.")
    return TavilySearchResults(max_results=5, tavily_api_key=api_key)
