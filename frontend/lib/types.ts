export type AgentStatusValue = "queued" | "running" | "done" | "failed";
export type ThreatLevel = "low" | "medium" | "high";
export type JobStatus = "pending" | "running" | "complete" | "failed";
export type StreamPhase = "idle" | "connecting" | "streaming" | "complete" | "error";

export interface AgentStatus {
  name: string;
  status: AgentStatusValue;
  message: string;
}

export interface Competitor {
  name: string;
  category: string;
  threat_level: ThreatLevel;
  reason: string;
}

export interface CompetitorAnalysisOutput {
  competitors: Competitor[];
  total_found: number;
  direct_threats: number;
  analysis_summary: string;
}

export interface MarketResearchOutput {
  tam: string;
  sam: string;
  som: string;
  growth_rate: string;
  market_summary: string;
  key_trends: string[];
}

export interface RevenueScenario {
  year_1: string;
  year_2: string;
  year_3: string;
}

export interface FinancialModellingOutput {
  conservative: RevenueScenario;
  base: RevenueScenario;
  optimistic: RevenueScenario;
  key_assumptions: string[];
  financial_summary: string;
}

export interface SynthesisOutput {
  viability_score: number;
  market_demand_score: number;
  competitive_gap_score: number;
  execution_feasibility_score: number;
  financial_outlook_score: number;
  verdict: string;
  recommended_strategy: string;
  key_risks: string[];
  tags: string[];
}

export interface FullReport {
  idea: string;
  market: MarketResearchOutput;
  competitors: CompetitorAnalysisOutput;
  financials: FinancialModellingOutput;
  synthesis: SynthesisOutput;
}

export interface JobRecord {
  job_id: string;
  idea: string;
  status: JobStatus;
  created_at: string;
  updated_at: string;
  agent_statuses: Record<string, AgentStatus>;
  partial_results: Record<string, unknown>;
  final_report: FullReport | null;
}

// SSE discriminated union
export interface AgentUpdateEvent {
  type: "agent_update";
  node: string;
  agent_statuses: Record<string, AgentStatus>;
  partial_data: Record<string, boolean>;
}

export interface CompleteEvent {
  type: "complete";
  final_report: FullReport;
}

export interface ErrorEvent {
  type: "error";
  message: string;
}

export interface DoneEvent {
  type: "done";
}

export type SSEEvent = AgentUpdateEvent | CompleteEvent | ErrorEvent | DoneEvent | { type: "heartbeat" };
