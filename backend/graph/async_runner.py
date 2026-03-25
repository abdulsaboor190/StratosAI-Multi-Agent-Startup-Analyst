import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

from store.job_store import job_store, JobStatus
from store.event_bus import event_bus
from models.schemas import FullReport, MarketResearchOutput, CompetitorAnalysisOutput, FinancialModellingOutput, SynthesisOutput
from utils.timeout_wrapper import with_loading_state

load_dotenv()

_executor = ThreadPoolExecutor(max_workers=4)

def _build_and_stream_pipeline(idea: str, job_id: str):
    from langgraph.graph import StateGraph, END, START
    from graph.state import VentureScopeState, create_initial_state
    import graph.nodes as nodes
    from graph.graph_builder import supervisor_router

    def wrap_node(func, name):
        def wrapper(state):
            with with_loading_state(name, job_id):
                return func(state)
        return wrapper

    builder = StateGraph(VentureScopeState)
    builder.add_node("market_research", wrap_node(nodes.market_research_node, "market_research"))
    builder.add_node("competitor", wrap_node(nodes.competitor_node, "competitor"))
    builder.add_node("financial", wrap_node(nodes.financial_node, "financial"))
    builder.add_node("synthesis", wrap_node(nodes.synthesis_node, "synthesis"))
    builder.add_node("supervisor", nodes.supervisor_node)
    builder.add_node("assemble_report", wrap_node(nodes.assemble_report_node, "assemble_report"))

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

    custom_graph = builder.compile()
    initial_state = create_initial_state(idea)
    
    chunks = []
    for chunk in custom_graph.stream(initial_state):
        chunks.append(chunk)
    return chunks

async def run_pipeline_for_job(job_id: str, idea: str) -> None:
    loop = asyncio.get_event_loop()

    try:
        job_store.update_job(job_id, status=JobStatus.running)
        await event_bus.publish(job_id, {
            "type": "job_started",
            "job_id": job_id,
            "idea": idea,
        })

        # Run with global timeout 180s
        task = loop.run_in_executor(_executor, _build_and_stream_pipeline, idea, job_id)
        
        start_time = time.time()
        chunks = None
        
        while not task.done():
            # Wait with heartbeat interval
            done, pending = await asyncio.wait([task], timeout=10.0)
            if task in done:
                chunks = task.result()
                break
            
            elapsed = time.time() - start_time
            if elapsed >= 180:
                raise asyncio.TimeoutError("Pipeline timed out after 180 seconds")
                
            await event_bus.publish(job_id, {
                "type": "heartbeat",
                "job_id": job_id,
                "timestamp": datetime.utcnow().isoformat()
            })

        final_report = None

        for chunk in chunks:
            node_name = list(chunk.keys())[0] if isinstance(chunk, dict) else "unknown"
            node_data = chunk.get(node_name, {})
            
            agent_statuses = node_data.get("agent_statuses", {})
            chunk_report = node_data.get("final_report")

            if agent_statuses:
                for name, status_obj in agent_statuses.items():
                    job_store.update_agent_status(job_id, name, status_obj.status, status_obj.message)

            if chunk_report is not None:
                final_report = chunk_report

            serialised_statuses = {}
            if agent_statuses:
                serialised_statuses = {k: v.model_dump() for k, v in agent_statuses.items()}

            await event_bus.publish(job_id, {
                "type": "agent_update",
                "node": node_name,
                "agent_statuses": serialised_statuses,
            })

        if final_report is None:
            # Construct partial report
            empty_market = MarketResearchOutput(tam="N/A", sam="N/A", som="N/A", growth_rate="N/A", market_summary="N/A", key_trends=["Partial Data"])
            empty_comp = CompetitorAnalysisOutput(competitors=[], total_found=0, direct_threats=0, analysis_summary="N/A")
            empty_fin = FinancialModellingOutput(
                conservative={"year_1": "N/A", "year_2": "N/A", "year_3": "N/A"},
                base={"year_1": "N/A", "year_2": "N/A", "year_3": "N/A"},
                optimistic={"year_1": "N/A", "year_2": "N/A", "year_3": "N/A"},
                key_assumptions=[], financial_summary="N/A"
            )
            empty_syn = SynthesisOutput(viability_score=0, market_demand_score=0, competitive_gap_score=0, execution_feasibility_score=0, financial_outlook_score=0, verdict="N/A", recommended_strategy="N/A", key_risks=[], tags=[])

            job = job_store.get_job(job_id)
            final_report = FullReport(
                idea=idea,
                market=job.partial_results.get("market", empty_market) if isinstance(job.partial_results.get("market"), MarketResearchOutput) else empty_market,
                competitors=job.partial_results.get("competitors", empty_comp) if isinstance(job.partial_results.get("competitors"), CompetitorAnalysisOutput) else empty_comp,
                financials=job.partial_results.get("financials", empty_fin) if isinstance(job.partial_results.get("financials"), FinancialModellingOutput) else empty_fin,
                synthesis=job.partial_results.get("synthesis", empty_syn) if isinstance(job.partial_results.get("synthesis"), SynthesisOutput) else empty_syn
            )

        job_store.update_job(job_id, status=JobStatus.complete, final_report=final_report)
        await event_bus.publish(job_id, {
            "type": "complete",
            "final_report": final_report.model_dump(),
        })

    except asyncio.TimeoutError as exc:
        job_store.update_job(job_id, status=JobStatus.failed, errors={"pipeline": str(exc)})
        await event_bus.publish(job_id, {
            "type": "error",
            "message": str(exc),
        })
    except Exception as exc:
        job_store.update_job(job_id, status=JobStatus.failed, errors={"pipeline": str(exc)})
        await event_bus.publish(job_id, {
            "type": "error",
            "message": str(exc),
        })

    finally:
        await event_bus.publish_done(job_id)
