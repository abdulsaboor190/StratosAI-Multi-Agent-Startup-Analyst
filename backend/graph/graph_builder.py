import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, END, START
from graph.state import VentureScopeState
from graph.nodes import (
    market_research_node,
    competitor_node,
    financial_node,
    synthesis_node,
    supervisor_node,
    assemble_report_node
)

def supervisor_router(state: VentureScopeState) -> str:
    statuses = state["agent_statuses"]
    
    if statuses["market_research"].status == "queued":
        return "market_research"
    if statuses["market_research"].status in ["done", "failed"] and statuses["competitor"].status == "queued":
        return "competitor"
    if statuses["competitor"].status in ["done", "failed"] and statuses["financial"].status == "queued":
        return "financial"
    
    return "synthesis"

def build_graph():
    builder = StateGraph(VentureScopeState)
    
    builder.add_node("market_research", market_research_node)
    builder.add_node("competitor", competitor_node)
    builder.add_node("financial", financial_node)
    builder.add_node("synthesis", synthesis_node)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("assemble_report", assemble_report_node)
    
    builder.add_edge(START, "market_research")
    builder.add_edge("market_research", "supervisor")
    builder.add_edge("competitor", "supervisor")
    builder.add_edge("financial", "supervisor")
    builder.add_edge("synthesis", "assemble_report")
    builder.add_edge("assemble_report", END)
    
    builder.add_conditional_edges(
        "supervisor",
        supervisor_router,
        {
            "market_research": "market_research",
            "competitor": "competitor",
            "financial": "financial",
            "synthesis": "synthesis"
        }
    )
    
    return builder.compile()

graph = build_graph()
