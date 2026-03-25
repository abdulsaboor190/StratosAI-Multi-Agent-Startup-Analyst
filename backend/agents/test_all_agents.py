import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from agents.market_research_agent import run_market_research_agent
from agents.competitor_agent import run_competitor_agent
from agents.financial_agent import run_financial_agent
from agents.synthesis_agent import run_synthesis_agent

load_dotenv()

def run_all_agents():
    idea = "AI-powered SaaS for remote team collaboration"
    print("====================================")
    print(f"STARTING VALIDATION FOR IDEA:")
    print(f"{idea}")
    print("====================================\n")

    # 1. MARKET RESEARCH AGENT
    print("=== MARKET RESEARCH AGENT ===")
    try:
        market_output = run_market_research_agent(idea)
        print("Status: SUCCESS")
        print(f"TAM: {market_output.tam}")
        print(f"Growth Rate: {market_output.growth_rate}")
    except Exception as e:
        print(f"Status: FAILED ({e})")
        market_output = None
    print()

    # 2. COMPETITOR AGENT
    print("=== COMPETITOR AGENT ===")
    try:
        competitor_output = run_competitor_agent(idea)
        print("Status: SUCCESS")
        print(f"Direct Threats: {competitor_output.direct_threats}")
        print(f"Top Competitors: {[c.name for c in competitor_output.competitors]}")
    except Exception as e:
        print(f"Status: FAILED ({e})")
        competitor_output = None
    print()

    # 3. FINANCIAL AGENT
    print("=== FINANCIAL AGENT ===")
    if market_output:
        try:
            financial_output = run_financial_agent(idea, market_output)
            print("Status: SUCCESS")
            print(f"Base Year 3 Revenue: {financial_output.base.year_3}")
        except Exception as e:
            print(f"Status: FAILED ({e})")
            financial_output = None
    else:
        print("Status: SKIPPED (Missing market data)")
        financial_output = None
    print()

    # 4. SYNTHESIS AGENT
    print("=== SYNTHESIS AGENT ===")
    if market_output and competitor_output and financial_output:
        try:
            synthesis_output = run_synthesis_agent(
                idea, market_output, competitor_output, financial_output
            )
            print("Status: SUCCESS\n")
            print("====================================")
            print("         FINAL SYNTHESIS          ")
            print("====================================")
            print(f"VIABILITY SCORE : {synthesis_output.viability_score}/100")
            print(f"VERDICT         : {synthesis_output.verdict}")
            print(f"RECOMMENDATION  : {synthesis_output.recommended_strategy}")
            print("====================================")
        except Exception as e:
            print(f"Status: FAILED ({e})")
    else:
        print("Status: SKIPPED (Missing prerequisite agent data)")

if __name__ == "__main__":
    run_all_agents()
