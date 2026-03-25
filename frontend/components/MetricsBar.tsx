"use client";

import React from "react";
import type { FullReport, AgentStatus } from "../lib/types";

export default function MetricsBar({ report, agentStatuses }: { report: FullReport | null; agentStatuses: Record<string, AgentStatus> }) {
  const synthesis = report?.synthesis;
  
  return (
    <div className="grid grid-cols-4 divide-x divide-[#c9a84c26]">
      <MetricCard 
        label="VIABILITY SCORE"
        val={synthesis?.viability_score ?? "74"}
        valExtra="/100"
        sub={synthesis ? (synthesis.viability_score >= 70 ? "Strong potential" : "Risk identified") : "Strong potential"}
        subColor={synthesis ? (synthesis.viability_score >= 70 ? "#4caf7d" : "#e09c3a") : "#4caf7d"}
      />
      <MetricCard 
        label="ADDRESSABLE MARKET"
        val={report?.market?.tam?.replace(/[^\d.]/g, '') || "18.4"}
        valExtra={report?.market?.tam?.replace(/[\d.]/g, '') || "B"}
        sub={report?.market?.growth_rate ? `+${report.market.growth_rate} YoY` : "+14% YoY"}
        subColor="#4caf7d"
      />
      <MetricCard 
        label="COMPETITORS FOUND"
        val={report?.competitors?.total_found ?? "12"}
        valExtra=" total"
        sub={report?.competitors ? `${report.competitors.direct_threats} direct threats` : "3 direct threats"}
        subColor="#e09c3a"
      />
      <MetricCard 
        label="RISK LEVEL"
        val={report?.synthesis ? (report.synthesis.key_risks.length > 4 ? "High" : "Med") : "Med"}
        sub={report?.synthesis ? (report.synthesis.key_risks.length > 4 ? "High entry barrier" : "Analyzing risks") : "High entry barrier"}
        subColor="#e05252"
        isText={true}
      />
    </div>
  );
}

function MetricCard({ label, val, valExtra, sub, subColor, isText = false }: any) {
  return (
    <div className="px-10 py-5 flex flex-col justify-center bg-[#0a0a0b]">
      <div className="text-[9px] tracking-[0.2em] text-[#5a5a6a] font-[family-name:var(--font-bebas)] mb-2 uppercase font-bold">
        {label}
      </div>
      <div className="flex items-baseline gap-1.5 mb-1">
        <span className={`font-[family-name:var(--font-cormorant)] text-[32px] leading-none font-light tracking-wide ${isText ? 'text-[#e09c3a]' : 'text-white'}`}>
          {val}
        </span>
        <span className="text-[11px] text-[#5a5a6a] font-light italic">{valExtra}</span>
      </div>
      <div className="text-[9px] font-bold tracking-[0.1em] uppercase opacity-90" style={{ color: subColor }}>
        {sub}
      </div>
    </div>
  );
}
