"use client";

import React from "react";
import type { Competitor } from "../lib/types";

export default function CompetitorTable({ competitors }: { competitors: Competitor[] | null }) {
  const list = (competitors && competitors.length > 0) ? competitors.slice(0, 4) : [
    { name: "Notion", category: "All-in-one workspace", threat_level: "high" },
    { name: "Slack", category: "Team communication", threat_level: "medium" },
    { name: "Linear", category: "Project management", threat_level: "medium" },
    { name: "Asana", category: "Work management", threat_level: "low" },
  ];

  return (
    <div className="flex flex-col h-full justify-center">
      <div className="text-[9px] tracking-[0.3em] text-[#e09c3a] font-[family-name:var(--font-bebas)] mb-6 uppercase font-bold text-left">
        Top Competitors
      </div>
      
      <div className="space-y-4 pr-3">
        {list.map((c, i) => {
          let badge = "#4caf7d";
          if (c.threat_level === "high") badge = "#e05252";
          if (c.threat_level === "medium") badge = "#e09c3a";

          return (
            <div key={i} className="flex items-center gap-4 group">
              <div className="h-8 w-8 border border-[#c9a84c44] bg-[rgba(201,168,76,0.04)] flex items-center justify-center text-[12px] text-[#7a6230] font-bold transition-all group-hover:bg-[#c9a84c1a] shrink-0">
                {c.name.charAt(0).toUpperCase()}
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-[12px] text-white font-medium tracking-wide truncate uppercase leading-none mb-1">
                   {c.name}
                </div>
                <div className="text-[9px] text-[#5a5a6a] truncate italic font-medium opacity-80">
                   {c.category}
                </div>
              </div>
              <div className={`text-[7px] px-2 py-0.5 border uppercase shrink-0 font-bold tracking-[0.2em] bg-black/30 w-[60px] text-center`} style={{ borderColor: badge + '44', color: badge }}>
                {c.threat_level}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
