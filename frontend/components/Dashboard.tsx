"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { AgentStatus, FullReport, StreamPhase } from "../lib/types";
import AgentPipelinePanel from "./AgentPipelinePanel";
import MetricsBar from "./MetricsBar";
import CompetitorTable from "./CompetitorTable";
import { ViabilityBreakdown, MarketSizePanel, AIVerdictPanel } from "./VerdictPanel";

interface Props {
  idea: string;
  jobStatus: string | null;
  agentStatuses: Record<string, AgentStatus>;
  report: FullReport | null;
  streamPhase: StreamPhase;
  error?: string | null;
  currentNode: string | null;
  elapsedSeconds: number;
  reset: () => void;
}

export default function Dashboard({ idea, agentStatuses, report, streamPhase, error, currentNode, elapsedSeconds, reset }: Props) {
  
  return (
    <div className="h-screen w-screen bg-[#0a0a0b] text-[#f0ede6] flex flex-col font-sans selection:bg-[#c9a84c] selection:text-[#0a0a0b] overflow-hidden">
      
      {/* HEADER: Ultra-compact */}
      <header className="px-10 py-5 flex items-center justify-between border-b border-[#c9a84c26] bg-[#0a0a0b] shrink-0">
        <div className="flex items-center gap-6">
          <div className="h-8 w-8 flex items-center justify-center border border-[#c9a84c] rotate-45 shadow-[0_0_15px_rgba(201,168,76,0.15)] shrink-0">
            <div className="h-2 w-2 bg-[#c9a84c] rotate-0" />
          </div>
          <div className="flex flex-col">
            <h1 className="font-[family-name:var(--font-bebas)] text-2xl tracking-[0.2em] leading-none mb-1 text-white uppercase">StratosAI</h1>
            <p className="text-[9px] tracking-[0.3em] text-[#7a6230] uppercase font-bold">Startup Intelligence</p>
          </div>
        </div>

        <div className="border border-[#c9a84c33] px-6 py-2 text-[11px] text-[#7a6230] max-w-[400px] truncate uppercase font-mono tracking-wider bg-[rgba(201,168,76,0.02)]">
          {idea}
        </div>

        <div className="flex items-center gap-3">
          <div className={`h-1.5 w-1.5 rounded-full ${streamPhase === 'complete' ? 'bg-[#4caf7d]' : 'bg-[#e09c3a]'} animate-pulse shadow-[0_0_8px_currentColor]`} />
          <span className="uppercase tracking-[0.2em] font-bold text-[9px] text-[#5a5a6a]">
             {streamPhase === 'streaming' ? 'Agents running' : streamPhase === 'complete' ? 'Agents complete' : 'Initializing'}
          </span>
        </div>
      </header>

      {/* METRICS */}
      <div className="border-b border-[#c9a84c26] shrink-0">
        <MetricsBar report={report} agentStatuses={agentStatuses} />
      </div>

      {/* MAIN GRID: Tightly packed */}
      <div className="flex-1 grid grid-cols-[1.8fr_1fr] divide-x divide-[#c9a84c26] min-h-0">
        
        {/* LEFT COLUMN */}
        <div className="flex flex-col flex-1 divide-y divide-[#c9a84c26] min-h-0">
          <div className="flex-[1.2] px-10 py-6 min-h-0 flex flex-col justify-center">
            <AgentPipelinePanel agentStatuses={agentStatuses} currentNode={currentNode} />
          </div>

          <div className="flex-1 grid grid-cols-2 divide-x divide-[#c9a84c26] min-h-0">
             <div className="px-10 py-6 min-h-0 flex flex-col justify-center">
                <CompetitorTable competitors={report?.competitors?.competitors ?? null} />
             </div>
             <div className="px-10 py-6 min-h-0 flex flex-col justify-center">
                <MarketSizePanel market={report?.market ?? null} />
             </div>
          </div>
        </div>

        {/* RIGHT COLUMN */}
        <div className="flex flex-col flex-1 divide-y divide-[#c9a84c26] bg-[rgba(255,255,255,0.01)] min-h-0">
          <div className="flex-[1.2] px-10 py-6 min-h-0 flex flex-col justify-center">
            <ViabilityBreakdown synthesis={report?.synthesis ?? null} />
          </div>

          <div className="flex-1 px-10 py-6 bg-[rgba(201,168,76,0.02)] min-h-0 flex flex-col justify-center">
            <AIVerdictPanel synthesis={report?.synthesis ?? null} onReset={reset} />
          </div>
        </div>

      </div>

      {/* ERROR MODAL */}
      <AnimatePresence>
        {streamPhase === "error" && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-[#0a0a0b]/80 backdrop-blur-sm flex items-center justify-center p-8"
          >
            <div className="p-8 bg-[#111114] border border-[#e05252aa] max-w-lg w-full shadow-[0_0_40px_rgba(224,82,82,0.15)] flex flex-col">
              <h3 className="text-[#e05252] font-[family-name:var(--font-bebas)] text-xl tracking-[0.2em] mb-3 uppercase">Orchestration Error</h3>
              <p className="text-xs text-[#f0ede6] opacity-70 mb-6 leading-relaxed font-mono uppercase">
                Critical failure in agent sequence.
              </p>
              <button 
                onClick={reset} 
                className="w-full bg-[#e05252] text-black font-bold py-2.5 tracking-[0.2em] uppercase hover:opacity-90 transition-all text-[10px]"
              >
                Reset System
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
