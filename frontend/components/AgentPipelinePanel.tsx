"use client";

import React from "react";
import type { AgentStatus } from "../lib/types";

const ORDER = ["market_research", "competitor", "financial", "synthesis"];
const NAMES: Record<string, string> = {
  market_research: "Market Research Agent",
  competitor: "Competitor Analysis Agent",
  financial: "Financial Modelling Agent",
  synthesis: "Report Synthesis Agent",
};

export default function AgentPipelinePanel({ agentStatuses, currentNode }: { agentStatuses: Record<string, AgentStatus>; currentNode: string | null }) {
  return (
    <div className="flex flex-col h-full justify-center">
      <div className="text-[9px] tracking-[0.3em] text-[#e09c3a] font-[family-name:var(--font-bebas)] mb-6 uppercase font-bold">
        Agent Pipeline
      </div>
      
      <div className="space-y-6">
        {ORDER.map((id, index) => {
          const status = agentStatuses[id]?.status ?? (index < 2 ? "done" : index === 2 ? "running" : "queued");
          const isRunning = status === "running" || currentNode === id;
          const isDone = status === "done";
          
          let color = "#5a5a6a";
          let label = "QUEUED"; 
          if (isRunning) { color = "#e09c3a"; label = "RUNNING"; }
          if (isDone) { color = "#4caf7d"; label = "DONE"; }

          return (
            <div key={id} className="flex items-center gap-6 group relative">
              <div className={`font-[family-name:var(--font-bebas)] text-3xl leading-none tabular-nums transition-colors duration-500 shrink-0 ${isDone || isRunning ? 'text-[#c9a84c33]' : 'text-[#18181d]'}`}>
                0{index + 1}
              </div>
              
              <div className="flex-1 min-w-0 pr-4">
                <div className="flex items-center justify-between gap-4 mb-1">
                  <div className="text-[12px] text-white font-[family-name:var(--font-dm-mono)] tracking-wider uppercase font-bold">
                    {NAMES[id]}
                  </div>
                  <div className={`text-[8px] px-2 py-0.5 border grow-0 font-bold tracking-[0.2em] transition-colors duration-300 uppercase`} style={{ borderColor: color + '44', color: color }}>
                    {label}
                  </div>
                </div>
                <div className="text-[10px] text-[#5a5a6a] mb-2 italic truncate opacity-90 font-medium">
                  {agentStatuses[id]?.message || (isDone ? "Analytical sequence complete." : isRunning ? "Processing data streams..." : "Waiting for sequence...")}
                </div>
                <div className="h-px w-full bg-[#111114] relative overflow-hidden">
                   <div 
                    className={`absolute h-full left-0 transition-all duration-1000 ${isRunning ? 'animate-progress-slide bg-[#e09c3a]' : isDone ? 'bg-[#c9a84c]' : 'bg-transparent'}`}
                    style={{ width: isDone ? '100%' : isRunning ? '45%' : '0%' }}
                   />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
