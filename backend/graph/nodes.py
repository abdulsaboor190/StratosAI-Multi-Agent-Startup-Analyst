import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.state import VentureScopeState
from agents.market_research_agent import run_market_research_agent
from agents.competitor_agent import run_competitor_agent
from agents.financial_agent import run_financial_agent
from agents.synthesis_agent import run_synthesis_agent
from models.schemas import AgentStatus, FullReport, MarketResearchOutput, CompetitorAnalysisOutput, FinancialModellingOutput, SynthesisOutput

def market_research_node(state: VentureScopeState) -> dict:
    statuses = state.get("agent_statuses", {}).copy()
    errors = state.get("errors", {}).copy()
    
    statuses["market_research"] = AgentStatus(name="market_research", status="running", message="Running market research")
    
    try:
        output = run_market_research_agent(state["idea"])
        statuses["market_research"] = AgentStatus(name="market_research", status="done", message="Completed successfully")
        return {"market": output, "agent_statuses": statuses, "errors": errors}
    except Exception as e:
        statuses["market_research"] = AgentStatus(name="market_research", status="failed", message=str(e))
        errors["market_research"] = str(e)
        return {"agent_statuses": statuses, "errors": errors}

def competitor_node(state: VentureScopeState) -> dict:
    statuses = state.get("agent_statuses", {}).copy()
    errors = state.get("errors", {}).copy()
    
    statuses["competitor"] = AgentStatus(name="competitor", status="running", message="Running competitor analysis")
    
    try:
        output = run_competitor_agent(state["idea"])
        statuses["competitor"] = AgentStatus(name="competitor", status="done", message="Completed successfully")
        return {"competitors": output, "agent_statuses": statuses, "errors": errors}
    except Exception as e:
        statuses["competitor"] = AgentStatus(name="competitor", status="failed", message=str(e))
        errors["competitor"] = str(e)
        return {"agent_statuses": statuses, "errors": errors}

def financial_node(state: VentureScopeState) -> dict:
    statuses = state.get("agent_statuses", {}).copy()
    errors = state.get("errors", {}).copy()
    
    statuses["financial"] = AgentStatus(name="financial", status="running", message="Running financial modelling")
    
    market_data = state.get("market")
    if not market_data:
        statuses["financial"] = AgentStatus(name="financial", status="failed", message="Market data unavailable")
        errors["financial"] = "Market data unavailable"
        return {"agent_statuses": statuses, "errors": errors}
        
    try:
        output = run_financial_agent(state["idea"], market_data)
        statuses["financial"] = AgentStatus(name="financial", status="done", message="Completed successfully")
        return {"financials": output, "agent_statuses": statuses, "errors": errors}
    except Exception as e:
        statuses["financial"] = AgentStatus(name="financial", status="failed", message=str(e))
        errors["financial"] = str(e)
        return {"agent_statuses": statuses, "errors": errors}

def synthesis_node(state: VentureScopeState) -> dict:
    statuses = state.get("agent_statuses", {}).copy()
    errors = state.get("errors", {}).copy()
    
    statuses["synthesis"] = AgentStatus(name="synthesis", status="running", message="Running synthesis")
    
    market_data = state.get("market") or MarketResearchOutput(
        tam="Unknown", sam="Unknown", som="Unknown", growth_rate="Unknown", 
        market_summary="Market data unavailable due to earlier failure.", key_trends=[]
    )
    
    comp_data = state.get("competitors") or CompetitorAnalysisOutput(
        competitors=[], total_found=0, direct_threats=0, 
        analysis_summary="Competitor data unavailable due to earlier failure."
    )
    
    fin_data = state.get("financials") or FinancialModellingOutput(
        conservative={"year_1": "Unknown", "year_2": "Unknown", "year_3": "Unknown"},
        base={"year_1": "Unknown", "year_2": "Unknown", "year_3": "Unknown"},
        optimistic={"year_1": "Unknown", "year_2": "Unknown", "year_3": "Unknown"},
        key_assumptions=[],
        financial_summary="Financial data unavailable."
    )
    
    try:
        output = run_synthesis_agent(state["idea"], market_data, comp_data, fin_data)
        statuses["synthesis"] = AgentStatus(name="synthesis", status="done", message="Completed successfully")
        return {"synthesis": output, "agent_statuses": statuses, "errors": errors}
    except Exception as e:
        statuses["synthesis"] = AgentStatus(name="synthesis", status="failed", message=str(e))
        errors["synthesis"] = str(e)
        return {"agent_statuses": statuses, "errors": errors}

def supervisor_node(state: VentureScopeState) -> dict:
    statuses = state.get("agent_statuses", {}).copy()
    retries = state.get("retry_counts", {}).copy()
    
    for agent_name in ["market_research", "competitor", "financial", "synthesis"]:
        if statuses[agent_name].status == "failed" and retries[agent_name] < 1:
            retries[agent_name] += 1
            statuses[agent_name] = AgentStatus(name=agent_name, status="queued", message="Retrying after failure")
            
    return {"agent_statuses": statuses, "retry_counts": retries}

def assemble_report_node(state: VentureScopeState) -> dict:
    statuses = state.get("agent_statuses", {}).copy()
    statuses["assemble_report"] = AgentStatus(name="assemble_report", status="done", message="Completed")
    
    empty_market = MarketResearchOutput(tam="N/A", sam="N/A", som="N/A", growth_rate="N/A", market_summary="N/A", key_trends=[])
    empty_comp = CompetitorAnalysisOutput(competitors=[], total_found=0, direct_threats=0, analysis_summary="N/A")
    empty_fin = FinancialModellingOutput(
        conservative={"year_1": "N/A", "year_2": "N/A", "year_3": "N/A"},
        base={"year_1": "N/A", "year_2": "N/A", "year_3": "N/A"},
        optimistic={"year_1": "N/A", "year_2": "N/A", "year_3": "N/A"},
        key_assumptions=[], financial_summary="N/A"
    )
    empty_syn = SynthesisOutput(viability_score=0, market_demand_score=0, competitive_gap_score=0, execution_feasibility_score=0, financial_outlook_score=0, verdict="N/A", recommended_strategy="N/A", key_risks=[], tags=[])

    report = FullReport(
        idea=state["idea"],
        market=state.get("market") if state.get("market") is not None else empty_market,
        competitors=state.get("competitors") if state.get("competitors") is not None else empty_comp,
        financials=state.get("financials") if state.get("financials") is not None else empty_fin,
        synthesis=state.get("synthesis") if state.get("synthesis") is not None else empty_syn
    )
    return {"final_report": report, "agent_statuses": statuses}
