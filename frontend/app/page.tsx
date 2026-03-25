"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useVentureScope } from "../lib/hooks/useVentureScope";
import Dashboard from "../components/Dashboard";

export default function Home() {
  const {
    idea,
    setIdea,
    submitIdea,
    reset,
    isLoading,
    error,
    streamPhase,
    agentStatuses,
    report,
    currentNode,
    elapsedSeconds,
  } = useVentureScope();

  // Show dashboard during execution or after completion/error
  const showDashboard = ["connecting", "streaming", "complete", "error"].includes(streamPhase);

  if (showDashboard) {
    return (
      <Dashboard
        idea={idea}
        jobStatus={null}
        agentStatuses={agentStatuses}
        report={report}
        streamPhase={streamPhase}
        error={error}
        currentNode={currentNode}
        elapsedSeconds={elapsedSeconds}
        reset={reset}
      />
    );
  }

  return (
    <main className="relative min-h-screen flex items-center justify-center px-4 overflow-hidden selection:bg-[var(--gold)] selection:text-[var(--bg)]">
      
      {/* Subtle ambient effect */}
      <div className="pointer-events-none fixed left-1/2 top-[-200px] h-[1000px] w-[1000px] -translate-x-1/2 rounded-full blur-[120px] bg-[radial-gradient(ellipse,_rgba(201,168,76,0.08)_0%,_transparent_70%)] z-0 mix-blend-screen" />
      
      <div className="relative z-10 w-full max-w-[640px] py-12 animate-in fade-in slide-in-from-bottom-5 duration-1000">
        
        {/* Brand Mark */}
        <div className="flex flex-col items-center gap-6 mb-16">
          <div className="flex h-12 w-12 items-center justify-center border-[0.5px] border-[var(--gold)] rotate-45 shrink-0 shadow-[0_0_20px_rgba(201,168,76,0.15)]">
            <div className="h-4 w-4 bg-[var(--gold)] rotate-0" />
          </div>
          <div className="flex flex-col items-center">
            <h1 className="font-[family-name:var(--font-bebas)] text-[42px] tracking-[0.25em] text-[var(--white)] leading-none">
              StratosAI
            </h1>
            <div className="text-[11px] tracking-[0.4em] text-[var(--gold)] mt-3 uppercase font-medium">
              Startup Intelligence Platform
            </div>
          </div>
        </div>

        <div className="text-center mb-12">
          <h2 className="font-[family-name:var(--font-cormorant)] text-[58px] font-light leading-[1.05] text-[var(--white)]">
            Validate your <br/>
            <span className="text-[var(--gold)] font-medium">strategic concept</span>
          </h2>
          <div className="mt-8 mx-auto h-[0.5px] w-24 bg-[var(--gold)] opacity-40 shadow-[0_0_10px_var(--gold)]" />
          <p className="mt-8 text-[13px] text-[var(--muted)] leading-relaxed tracking-wide font-medium">
            Autonomous agent swarm orchestrating market intelligence, <br/>
            competitor mapping, and financial longevity modelling.
          </p>
        </div>

        <div className="bg-[var(--surface)] border-[0.5px] border-[var(--border)] p-[32px] shadow-2xl relative group">
           {/* Decorative corner */}
           <div className="absolute top-0 right-0 h-4 w-4 border-t-[0.5px] border-r-[0.5px] border-[var(--gold-dim)] transition-all duration-500 group-hover:scale-125" />
           <div className="absolute bottom-0 left-0 h-4 w-4 border-b-[0.5px] border-l-[0.5px] border-[var(--gold-dim)] transition-all duration-500 group-hover:scale-125" />

           <div className="font-[family-name:var(--font-bebas)] text-[9px] tracking-[0.3em] text-[var(--gold-dim)] uppercase mb-3 font-bold">
             Concept Definition
           </div>
           
           <AnimatePresence>
             {error && (
               <motion.div
                 initial={{ opacity: 0, height: 0 }} 
                 animate={{ opacity: 1, height: "auto" }} 
                 exit={{ opacity: 0, height: 0 }}
                 className="text-[11px] mb-4 p-4 font-bold tracking-wide italic"
                 style={{ background: "rgba(224,82,82,0.05)", color: "var(--red)", borderLeft: "2px solid var(--red)" }}
               >
                 ⚠ {error}
               </motion.div>
             )}
           </AnimatePresence>

           <textarea
             rows={5}
             value={idea}
             onChange={(e) => setIdea(e.target.value)}
             placeholder="Describe your startup concept, revenue model, and competitive edge..."
             disabled={isLoading}
             className="w-full bg-[var(--bg)] border-[0.5px] border-[var(--border)] p-5 text-[14px] leading-relaxed text-[var(--white)] placeholder-[var(--muted)] focus:border-[var(--gold)] focus:outline-none transition-all duration-500 min-h-[140px] font-medium"
           />

           <div className="flex justify-between items-center mt-5">
             <span className={`text-[11px] tracking-widest font-bold tabular-nums ${idea.length > 500 ? "text-[var(--red)]" : "text-[var(--muted)]"}`}>
               {idea.length} / 500
             </span>
             <button
               onClick={() => submitIdea(idea)}
               disabled={isLoading || idea.length < 10 || idea.length > 500}
               className="relative overflow-hidden group/btn px-10 py-3.5 bg-transparent border-[0.5px] border-[var(--gold)] transition-all duration-500 hover:bg-[rgba(201,168,76,0.08)] disabled:opacity-30 disabled:cursor-not-allowed"
             >
               <div className="relative z-10 font-[family-name:var(--font-bebas)] text-[15px] tracking-[0.25em] text-[var(--gold)] flex items-center gap-3">
                 {isLoading ? "AGENT INITIATION..." : "INITIATE VALIDATION"}
                 <span className="group-hover/btn:translate-x-1 transition-transform duration-300">→</span>
               </div>
             </button>
           </div>
        </div>

        {/* Examples */}
        <div className="mt-16 flex flex-col items-center">
           <span className="text-[9px] tracking-[0.4em] text-[var(--muted)] uppercase font-bold mb-6">Select Sample Narrative</span>
           <div className="flex flex-col gap-[1px] bg-[var(--border)] border-[0.5px] border-[var(--border)] w-full max-w-[480px]">
             {["AI legal assistant for small businesses", "Subscription box for sustainable pet products", "Peer-to-peer car sharing in emerging markets"].map((ex) => (
               <button 
                 key={ex} 
                 onClick={() => setIdea(ex)} 
                 className="bg-[var(--surface)] p-4 text-[12px] text-[var(--muted)] hover:text-[var(--gold)] hover:bg-[var(--surface2)] transition-all duration-300 text-left tracking-[0.02em] border-none"
               >
                 {ex}
               </button>
             ))}
           </div>
        </div>

        {/* Footer */}
        <div className="mt-20 text-center font-bold tracking-[0.3em] text-[9px] text-[var(--muted)] uppercase opacity-60">
          Orchestrated by LangGraph · Groq · Tavily · Next.js 15
        </div>
      </div>
    </main>
  );
}
