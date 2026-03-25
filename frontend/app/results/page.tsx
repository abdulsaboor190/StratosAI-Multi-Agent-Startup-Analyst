"use client";

import React from "react";
import Link from "next/link";

export default function ResultsDashboard() {
  return (
    <div className="relative min-h-screen bg-[var(--bg)] font-[family-name:var(--font-dm-mono)] text-[var(--white)] overflow-y-auto">
      
      {/* Ambient BG */}
      <div className="pointer-events-none fixed left-1/2 top-[-200px] h-[800px] w-[800px] -translate-x-1/2 bg-[radial-gradient(ellipse,rgba(201,168,76,0.04)_0%,transparent_70%)] z-0 blend-screen" />
      
      <div className="relative z-10 mx-auto max-w-[1200px] px-8 py-7">
        
        {/* TOPBAR */}
        <div className="flex items-center justify-between border-b-[0.5px] border-[var(--border)] pb-5 mb-[36px]">
           <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
             <div className="flex h-8 w-8 items-center justify-center border border-[var(--gold)] rotate-45 shrink-0">
               <div className="h-3 w-3 bg-[var(--gold)] rotate-0" />
             </div>
             <div>
               <div className="font-[family-name:var(--font-bebas)] text-[22px] tracking-[0.12em] text-[var(--white)] leading-none">STRATOSAI</div>
               <div className="text-[10px] tracking-[0.2em] text-[var(--gold)] mt-0.5">Startup Intelligence Platform</div>
             </div>
           </Link>
           
           <div className="hidden md:block border-[0.5px] border-[var(--border)] px-4 py-[6px] text-[11px] text-[var(--gold-dim)] tracking-[0.08em] shadow-sm">
             AI-powered SaaS for remote team collaboration
           </div>
           
           <div className="flex items-center gap-1.5 text-[11px] text-[var(--muted)] shrink-0">
             <div className="h-1.5 w-1.5 animate-pulse rounded-full bg-[var(--green)]" />
             Agents complete
           </div>
        </div>

        {/* METRICS ROW */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-[1px] bg-[var(--border)] mb-[28px]">
          <MetricCard title="Viability Score" val="74" valSub="/100" note="Strong potential" noteColor="var(--green)" valColor="var(--gold)" />
          <MetricCard title="Total Addressable Market" val="$18.4" valSub="B" note="+14% YoY" noteColor="var(--green)" />
          <MetricCard title="Competitors Found" val="12" valSub=" total" note="3 direct threats" noteColor="var(--amber)" />
          <MetricCard title="Risk Level" val="Med" note="High entry barrier" noteColor="var(--red)" valColor="var(--amber)" />
        </div>

        {/* MAIN 2-COLUMN GRID */}
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_380px] gap-[1px] bg-[var(--border)] mb-[1px]">
          
          {/* Agent Pipeline */}
          <div className="bg-[var(--surface)] p-[24px]">
            <div className="mb-5 font-[family-name:var(--font-bebas)] text-[9px] tracking-[0.25em] text-[var(--gold)] uppercase">Agent Pipeline</div>
            <div className="flex flex-col">
               <AgentRow num="01" name="Market Research Agent" desc="Analyzed 34 sources across market size, trends & growth data" status="Done" color="var(--green)" bg="rgba(76,175,125,0.3)" />
               <AgentRow num="02" name="Competitor Analysis Agent" desc="Mapped 12 competitors across direct & indirect categories" status="Done" color="var(--green)" bg="rgba(76,175,125,0.3)" />
               <AgentRow num="03" name="Financial Modelling Agent" desc="Estimating revenue scenarios across 3-year horizon..." status="Running" color="var(--gold)" bg="rgba(201,168,76,0.3)" />
               <AgentRow num="04" name="Report Synthesis Agent" desc="Waiting for upstream agents to complete" status="Queued" color="var(--muted)" bg="rgba(90,90,106,0.3)" />
            </div>
          </div>
          
          {/* Viability Breakdown */}
          <div className="bg-[var(--surface)] p-[24px]">
            <div className="mb-[20px] font-[family-name:var(--font-bebas)] text-[9px] tracking-[0.25em] text-[var(--gold)] uppercase">Viability Breakdown</div>
            
            <div className="mb-[24px] flex items-center gap-[20px] border-b-[0.5px] border-[var(--border)] pb-[20px]">
               <div className="relative h-[80px] w-[80px] shrink-0 rotate-[-90deg]">
                 <svg viewBox="0 0 80 80" className="absolute inset-0 h-full w-full">
                   <circle cx="40" cy="40" r="32" fill="none" stroke="rgba(201,168,76,0.1)" strokeWidth="4" />
                   <circle cx="40" cy="40" r="32" fill="none" stroke="var(--gold)" strokeWidth="4" strokeDasharray="201" strokeDashoffset="52" strokeLinecap="square" />
                 </svg>
                 <div className="absolute inset-0 flex flex-col items-center justify-center rotate-[90deg]">
                   <span className="font-[family-name:var(--font-cormorant)] text-[26px] font-light leading-none text-[var(--gold)]">74</span>
                   <span className="text-[9px] text-[var(--muted)]">/100</span>
                 </div>
               </div>
               <div className="flex-1">
                 <div className="font-[family-name:var(--font-cormorant)] text-[18px] text-[var(--white)] leading-tight mb-1.5">Viable with differentiation</div>
                 <div className="text-[10px] text-[var(--muted)] leading-[1.6]">Strong market pull. Competitive pressure requires a clear strategic wedge.</div>
               </div>
            </div>
            
            <div className="flex flex-col gap-[12px]">
              <DimensionBar name="Market Demand" val={88} color="var(--green)" />
              <DimensionBar name="Competitive Gap" val={61} color="var(--amber)" />
              <DimensionBar name="Execution Feasibility" val={79} color="var(--gold)" />
              <DimensionBar name="Financial Outlook" val={66} color="var(--amber)" />
            </div>
          </div>
        </div>

        {/* BOTTOM 3-COLUMN GRID */}
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_1fr_380px] gap-[1px] bg-[var(--border)]">
           
           {/* Top Competitors */}
           <div className="bg-[var(--surface)] p-[24px]">
             <div className="mb-[20px] font-[family-name:var(--font-bebas)] text-[9px] tracking-[0.25em] text-[var(--gold)] uppercase">Top Competitors</div>
             <div className="flex flex-col">
               <CompetitorRow init="N" name="Notion" cat="All-in-one workspace" threat="High" color="var(--red)" bg="rgba(224,82,82,0.3)" />
               <CompetitorRow init="S" name="Slack" cat="Team communication" threat="Med" color="var(--amber)" bg="rgba(224,156,58,0.3)" />
               <CompetitorRow init="L" name="Linear" cat="Project management" threat="Med" color="var(--amber)" bg="rgba(224,156,58,0.3)" />
               <CompetitorRow init="A" name="Asana" cat="Work management" threat="Low" color="var(--green)" bg="rgba(76,175,125,0.3)" />
             </div>
           </div>

           {/* Market Sizing */}
           <div className="bg-[var(--surface)] p-[24px]">
             <div className="mb-[20px] font-[family-name:var(--font-bebas)] text-[9px] tracking-[0.25em] text-[var(--gold)] uppercase">Market Sizing</div>
             <TamBlock label="TAM — Total Market" val="$18.4B" sub="Global addressable" />
             <TamBlock label="SAM — Serviceable" val="$4.2B" sub="Reachable segment" />
             <TamBlock label="SOM — Year 3 Target" val="$84M" sub="Realistic capture" />
           </div>

           {/* AI Verdict */}
           <div className="bg-[var(--surface2)] p-[24px]">
             <div className="mb-[20px] font-[family-name:var(--font-bebas)] text-[9px] tracking-[0.25em] text-[var(--gold)] uppercase">AI Verdict</div>
             
             <div className="mb-[14px] flex h-[36px] w-[36px] items-center justify-center border border-[var(--gold)]">
                <svg viewBox="0 0 16 16" className="h-4 w-4 fill-none stroke-[var(--gold)] stroke-[1.5px]"><polyline points="2,8 6,12 14,4"/></svg>
             </div>
             
             <div className="mb-[10px] font-[family-name:var(--font-cormorant)] text-[20px] text-[var(--white)]">Viable with differentiation</div>
             <p className="mb-[16px] text-[11px] leading-[1.8] text-[var(--muted)]">
                Strong market demand exists but competitive pressure is high. Success depends on a clear wedge — target async-first remote teams in the 10–50 employee range where enterprise tools are too heavy.
             </p>
             <div className="flex flex-wrap gap-1.5">
               <Tag text="B2B SAAS" />
               <Tag text="REMOTE WORK" />
               <Tag text="PLG STRATEGY" />
               <Tag text="ASYNC-FIRST" />
             </div>
           </div>
        </div>
        
      </div>
    </div>
  );
}

// ---------------- Helper Components ----------------

function MetricCard({ title, val, valSub, note, noteColor, valColor = "var(--white)" }: any) {
  return (
    <div className="group relative bg-[var(--surface)] px-[22px] py-[20px] overflow-hidden">
      <div className="mb-[10px] font-[family-name:var(--font-bebas)] text-[9px] tracking-[0.2em] text-[var(--muted)] uppercase">{title}</div>
      <div className="font-[family-name:var(--font-cormorant)] text-[32px] font-light leading-none" style={{ color: valColor }}>
         {val}<span className="text-[14px] text-[var(--muted)] ml-0.5">{valSub}</span>
      </div>
      <div className="mt-1.5 text-[10px]" style={{ color: noteColor }}>{note}</div>
      
      {/* Animated Bottom Border */}
      <div className="absolute inset-x-0 bottom-0 h-[2px] scale-x-0 bg-[var(--gold)] origin-left transition-transform duration-500 ease-out group-hover:scale-x-100" />
    </div>
  );
}

function AgentRow({ num, name, desc, status, color, bg }: any) {
  const isDone = status === "Done";
  const bgWidth = isDone ? "100%" : status === "Running" ? "65%" : "0%";
  
  return (
    <div className="group flex items-start gap-[14px] border-b-[0.5px] border-[rgba(255,255,255,0.04)] py-[14px] last:border-0 border-t-transparent">
       <div className="font-[family-name:var(--font-bebas)] text-[28px] leading-none text-[var(--border)] transition-colors duration-300 group-hover:text-[var(--gold-dim)] min-w-[30px]">
         {num}
       </div>
       <div className="flex-1 min-w-0">
         <div className="text-[12px] text-[var(--white)] tracking-[0.05em] mb-1">{name}</div>
         <div className="text-[10px] text-[var(--muted)] mb-2 leading-[1.6] pr-4">{desc}</div>
         <div className="relative h-[1px] w-full bg-[rgba(255,255,255,0.06)] overflow-hidden">
            <div className={`absolute inset-y-0 left-0 ${status==='Running'?'bg-[var(--gold)] animate-progress-slide':'transition-all duration-300 bg-[var(--gold)]'}`} style={{ width: bgWidth }} />
         </div>
       </div>
       <div className="text-[9px] uppercase tracking-[0.15em] border-[0.5px] px-[10px] py-[3px] self-center" style={{ color: color, borderColor: bg }}>
          {status}
       </div>
    </div>
  );
}

function DimensionBar({ name, val, color }: any) {
  return (
    <div>
      <div className="mb-1 flex justify-between">
        <span className="text-[10px] text-[var(--muted)] tracking-[0.05em]">{name}</span>
        <span className="text-[10px] text-[var(--white)]">{val}</span>
      </div>
      <div className="h-[1px] w-full bg-[rgba(255,255,255,0.06)]">
        <div className="h-full transition-all duration-1000" style={{ width: `${val}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function CompetitorRow({ init, name, cat, threat, color, bg }: any) {
  return (
    <div className="flex items-center gap-[10px] border-b-[0.5px] border-[rgba(255,255,255,0.04)] py-[10px] last:border-0">
      <div className="flex h-[28px] w-[28px] shrink-0 items-center justify-center border-[0.5px] border-[var(--border)] text-[11px] text-[var(--gold-dim)]">
        {init}
      </div>
      <div className="flex-1 min-w-0">
        <div className="text-[12px] text-[var(--white)] truncate">{name}</div>
        <div className="mt-[2px] text-[9px] text-[var(--muted)] truncate">{cat}</div>
      </div>
      <div className="text-[9px] uppercase tracking-[0.1em] border-[0.5px] px-[8px] py-[2px]" style={{ color: color, borderColor: bg }}>
        {threat}
      </div>
    </div>
  );
}

function TamBlock({ label, val, sub }: any) {
  return (
    <div className="border-b-[0.5px] border-[var(--border)] py-[16px] px-[10px] text-center last:border-0">
      <div className="mb-[6px] font-[family-name:var(--font-dm-mono)] text-[9px] uppercase tracking-[0.2em] text-[var(--muted)]">{label}</div>
      <div className="font-[family-name:var(--font-cormorant)] text-[24px] font-[300] text-[var(--white)] leading-none mt-1">{val}</div>
      <div className="mt-[3px] text-[9px] text-[var(--gold-dim)]">{sub}</div>
    </div>
  );
}

function Tag({ text }: { text: string }) {
  return (
    <div className="border-[0.5px] border-[var(--border)] px-[10px] py-[4px] text-[9px] text-[var(--gold-dim)] tracking-[0.12em]">
      {text}
    </div>
  );
}
