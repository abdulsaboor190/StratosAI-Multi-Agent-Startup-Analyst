import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from utils.helpers import build_groq_llm, parse_json_from_llm
import json

load_dotenv()

def filter_search_results(results: list[dict], idea: str, topic: str) -> list[dict]:
    if not results:
        return []

    snippets = []
    for i, r in enumerate(results):
        title = r.get("title", "")
        content = r.get("content", "")[:300]
        snippets.append(f"[{i}] {title}\n{content}")
    
    snippets_text = "\n\n".join(snippets)

    prompt = f"""
You are an expert relevance judge. We are researching a startup idea: "{idea}".
The specific topic we need information on is: "{topic}".

Below is a numbered list of search result snippets. Read each snippet and determine if it is genuinely relevant and helpful for researching this specific topic for this startup idea.

Return ONLY a JSON array of the integer indices (0-based) for the snippets that are relevant. For example: [0, 2, 3].
If none are relevant, return an empty array: [].
Do not include any other text, explanation, or preamble. Just the JSON array.

Snippets:
{snippets_text}
"""
    
    llm = build_groq_llm()
    try:
        response = llm.invoke(prompt)
        parsed = parse_json_from_llm(response.content)
        if isinstance(parsed, list) and all(isinstance(x, int) for x in parsed):
            filtered = [results[i] for i in parsed if 0 <= i < len(results)]
            if not filtered and parsed: # Edge case out of bounds
                 return results
            return filtered
        else:
            print(f"Warning: Relevance filter returned invalid format. Falling back to original results. Raw response: {response.content}")
            return results
    except Exception as e:
        print(f"Warning: Relevance filter failed ({e}). Falling back to original results.")
        return results

def truncate_results_to_context(results: list[dict], max_chars: int = 4000) -> str:
    combined = []
    for r in results:
        title = r.get("title", "")
        content = r.get("content", "")
        combined.append(f"Title: {title}\nContent: {content}")
    
    full_text = "\n\n".join(combined)
    
    if len(full_text) <= max_chars:
        return full_text
        
    truncated = full_text[:max_chars]
    last_period = truncated.rfind(". ")
    if last_period != -1:
        truncated = truncated[:last_period + 1]
    
    return truncated + "\n[truncated]"
