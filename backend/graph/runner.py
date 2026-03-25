import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import json
from graph.state import create_initial_state
from graph.graph_builder import graph
from models.schemas import FullReport

load_dotenv()

def run_pipeline(idea: str) -> FullReport:
    initial_state = create_initial_state(idea)
    result = graph.invoke(initial_state)
    
    final_report = result.get("final_report")
    if not final_report:
        raise RuntimeError("Pipeline failed to generate final report.")
        
    return final_report

def stream_pipeline(idea: str):
    initial_state = create_initial_state(idea)
    
    for state_update in graph.stream(initial_state, stream_mode="updates"):
        for node_name, chunk in state_update.items():
            agent_statuses = chunk.get("agent_statuses")
            
            partial_data = {}
            if "market" in chunk: partial_data["market"] = chunk["market"] is not None
            if "competitors" in chunk: partial_data["competitors"] = chunk["competitors"] is not None
            if "financials" in chunk: partial_data["financials"] = chunk["financials"] is not None
            if "synthesis" in chunk: partial_data["synthesis"] = chunk["synthesis"] is not None
            
            final_report = chunk.get("final_report")
            
            yield {
                "node": node_name,
                "agent_statuses": agent_statuses,
                "partial_data": partial_data,
                "final_report": final_report
            }

if __name__ == "__main__":
    idea = "AI-powered SaaS for remote team collaboration"
    print(f"Running pipeline for idea: {idea}")
    try:
        report = run_pipeline(idea)
        print("\n=== PIPELINE SUCCESS ===")
        print(f"Viability Score : {report.synthesis.viability_score}/100")
        print(f"Verdict         : {report.synthesis.verdict}")
    except RuntimeError as e:
        print(f"=== PIPELINE FAILED ===\n{e}")
