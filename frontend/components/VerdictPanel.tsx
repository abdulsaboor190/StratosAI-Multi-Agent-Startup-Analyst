"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import type { SynthesisOutput, MarketResearchOutput } from "../lib/types";

export function ViabilityBreakdown({ synthesis }: { synthesis: SynthesisOutput | null }) {
  const [offset, setOffset] = useState(201);
  useEffect(() => {
    if (synthesis) {
       setTimeout(() => setOffset(201 * (1 - (synthesis.viability_score || 74) / 100)), 500);
    } else {
       setTimeout(() => setOffset(201 * (1 - 74 / 100)), 500);
    }
  }, [synthesis]);

  return (
    <div className="flex flex-col h-full justify-center">
      <div className="text-[9px] tracking-[0.3em] text-[#e09c3a] font-[family-name:var(--font-bebas)] mb-6 uppercase font-bold">
        Viability Breakdown
      </div>
      
      <div className="flex items-center gap-6 mb-6">
        <div className="relative h-16 w-16 shrink-0 rotate-[-90deg]">
          <svg viewBox="0 0 80 80" className="h-full w-full">
            <circle cx="40" cy="40" r="32" fill="none" stroke="rgba(201,168,76,0.1)" strokeWidth="4" />
            <circle cx="40" cy="40" r="32" fill="none" stroke="#c9a84c" strokeWidth="4" strokeDasharray="201" strokeDashoffset={offset} strokeLinecap="square" className="transition-all duration-[1.5s]" />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center rotate-[90deg]">
            <span className="text-[18px] font-light text-[#c9a84c] tabular-nums leading-none font-[family-name:var(--font-cormorant)]">
                {synthesis?.viability_score ?? "74"}
            </span>
            <span className="text-[8px] text-[#5a5a6a] tracking-widest mt-0.5 italic">/100</span>
          </div>
        </div>
        <div className="flex-1">
          <div className="text-[18px] font-[family-name:var(--font-cormorant)] text-white leading-tight mb-1 italic">
            {synthesis?.verdict || "Viable with differentiation"}
          </div>
          <p className="text-[10px] text-[#5a5a6a] leading-relaxed line-clamp-2 italic opacity-85">
            {synthesis?.recommended_strategy || "Strong market pull. Competitive pressure requires clear strategic wedge."}
          </p>
        </div>
      </div>

      <div className="space-y-4 pt-4 border-t border-[#c9a84c26]">
        <MetricRow label="Market Demand" val={synthesis?.market_demand_score ?? 88} color="#4caf7d" />
        <MetricRow label="Competitive Gap" val={synthesis?.competitive_gap_score ?? 61} color="#e09c3a" />
        <MetricRow label="Execution Feasibility" val={synthesis?.execution_feasibility_score ?? 79} color="#c9a84c" />
        <MetricRow label="Financial Outlook" val={synthesis?.financial_outlook_score ?? 66} color="#e09c3a" />
      </div>
    </div>
  );
}

function MetricRow({ label, val, color }: any) {
  return (
    <div className="flex items-center justify-between gap-6">
      <div className="text-[8px] text-[#5a5a6a] uppercase tracking-[0.2em] shrink-0 font-bold">{label}</div>
      <div className="flex-1 h-px bg-[#111114] relative overflow-hidden">
        <motion.div initial={{ width: 0 }} animate={{ width: `${val}%` }} transition={{ duration: 2, ease: "easeOut" }} className="absolute h-full left-0" style={{ backgroundColor: color }} />
      </div>
      <div className="text-[10px] font-bold tabular-nums italic font-mono" style={{ color }}>{val}</div>
    </div>
  );
}

export function MarketSizePanel({ market }: { market: MarketResearchOutput | null }) {
  return (
    <div className="flex flex-col h-full justify-center">
      <div className="text-[9px] tracking-[0.3em] text-[#e09c3a] font-[family-name:var(--font-bebas)] mb-4 uppercase font-bold text-left">
        Market Sizing
      </div>
      <div className="flex-1 flex flex-col justify-around divide-y divide-[#c9a84c26]">
        <Block label="TAM — TOTAL MARKET" val={market?.tam || "$18.4B"} sub="Global addressable" />
        <Block label="SAM — SERVICEABLE" val={market?.sam || "$4.2B"} sub="Reachable segment" />
        <Block label="SOM — YEAR 3 TARGET" val={market?.som || "$84M"} sub="Realistic capture" />
      </div>
    </div>
  );
}

function Block({ label, val, sub }: any) {
  return (
    <div className="py-2.5 flex flex-col items-center">
      <div className="text-[8px] text-[#5a5a6a] tracking-[0.2em] uppercase mb-1 font-bold">{label}</div>
      <div className="text-2xl font-[family-name:var(--font-cormorant)] text-white tracking-wide italic leading-none">{val}</div>
      <div className="text-[8px] text-[#7a6230] tracking-[0.2em] uppercase mt-1 opacity-80 font-bold">{sub}</div>
    </div>
  );
}

export function AIVerdictPanel({ synthesis, onReset }: { synthesis: SynthesisOutput | null; onReset: () => void }) {
  return (
    <div className="flex flex-col h-full flex-1 justify-center">
       <div className="text-[9px] tracking-[0.3em] text-[#e09c3a] font-[family-name:var(--font-bebas)] mb-4 uppercase font-bold">
         AI Verdict
       </div>
       
       <div className="mb-3 h-8 w-8 border border-[#c9a84c] flex items-center justify-center bg-[rgba(201,168,76,0.04)]">
          <svg className="w-4 h-4 text-[#c9a84c]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M5 13l4 4L19 7" />
          </svg>
       </div>
       
       <h4 className="text-[18px] font-[family-name:var(--font-cormorant)] tracking-wide text-white leading-tight font-medium mb-2 italic">
          {synthesis?.verdict || "Viable with differentiation"}
       </h4>
       
       <p className="text-[10px] leading-[1.6] text-[#5a5a6a] mb-4 font-medium italic opacity-90 pr-2">
          {synthesis?.recommended_strategy || "Strong market demand exists but competitive pressure is high. Success depends on a clear wedge — target async-first remote teams."}
       </p>
       
       <div className="flex flex-wrap gap-2 mb-4">
          {(synthesis?.tags || ["B2B SAAS", "REMOTE WORK", "PLG STRATEGY", "ASYNC"]).map(t => (
             <span key={t} className="px-2 py-1 border border-[#c9a84c33] text-[8px] text-[#7a6230] uppercase font-bold tracking-widest bg-black/40">{t}</span>
          ))}
       </div>

       <button onClick={onReset} className="mt-auto border border-[#c9a84c] py-2.5 text-[9px] font-[family-name:var(--font-bebas)] tracking-[0.2em] text-[#c9a84c] font-bold uppercase transition-all hover:bg-[#c9a84c11] bg-black/60">
          INITIATE NEW VALIDATION &rarr;
       </button>
    </div>
  );
}

export default function VerdictPanel() { return null; }
