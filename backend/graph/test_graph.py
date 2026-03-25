import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from graph.runner import run_pipeline, stream_pipeline

load_dotenv()

def test_full_pipeline():
    idea = "AI-powered SaaS for remote team collaboration"
    print("====================================")
    print(f"TESTING FULL PIPELINE")
    print("====================================\n")
    
    try:
        report = run_pipeline(idea)
        
        print("=== MARKET RESEARCH RESULT ===")
        print(f"TAM: {report.market.tam}")
        print(f"Growth Rate: {report.market.growth_rate}")
        print()
        
        print("=== COMPETITOR ANALYSIS RESULT ===")
        print(f"Total Found: {report.competitors.total_found}")
        print(f"Direct Threats: {report.competitors.direct_threats}")
        print()
        
        print("=== FINANCIAL MODELLING RESULT ===")
        print(f"Base Year 3 Revenue: {report.financials.base.year_3}")
        print()
        
        print("=== SYNTHESIS RESULT ===")
        print(f"Viability Score : {report.synthesis.viability_score}/100")
        print(f"Verdict         : {report.synthesis.verdict}")
        print("Top 3 Risks     :")
        for r in report.synthesis.key_risks[:3]:
            print(f"- {r}")
        print(f"Strategy        : {report.synthesis.recommended_strategy}")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")

def test_stream_pipeline():
    idea = "AI-powered SaaS for remote team collaboration"
    print("\n====================================")
    print(f"TESTING STREAM PIPELINE")
    print("====================================\n")
    
    try:
        for chunk in stream_pipeline(idea):
            node = chunk.get("node")
            print(f"--- Node Executed: {node} ---")
            
            statuses = chunk.get("agent_statuses")
            if statuses:
                for k, v in statuses.items():
                    print(f"Agent '{k}' -> {v.status} ({v.message})")
            
            p_data = chunk.get("partial_data")
            if p_data:
                print(f"Partial data available: {p_data}")
                
            if chunk.get("final_report"):
                print("Final report generated successfully!")
            print()
    except Exception as e:
        print(f"Stream pipeline failed: {e}")

if __name__ == "__main__":
    test_full_pipeline()
    test_stream_pipeline()
