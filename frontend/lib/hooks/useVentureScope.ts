"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { createJob, streamJobEvents, pollJobReport } from "../api";
import type {
  AgentStatus,
  FullReport,
  JobStatus,
  SSEEvent,
  StreamPhase,
} from "../types";

interface VentureScopeState {
  idea: string;
  jobId: string | null;
  jobStatus: JobStatus | null;
  agentStatuses: Record<string, AgentStatus>;
  report: FullReport | null;
  isLoading: boolean;
  error: string | null;
  streamPhase: StreamPhase;
  useFallbackPolling: boolean;
  elapsedSeconds: number;
  currentNode: string | null;
}

interface VentureScopeHook extends VentureScopeState {
  setIdea: (idea: string) => void;
  submitIdea: (idea: string) => Promise<void>;
  reset: () => void;
}

const INITIAL_STATE: VentureScopeState = {
  idea: "",
  jobId: null,
  jobStatus: null,
  agentStatuses: {},
  report: null,
  isLoading: false,
  error: null,
  streamPhase: "idle",
  useFallbackPolling: false,
  elapsedSeconds: 0,
  currentNode: null,
};

export function useVentureScope(): VentureScopeHook {
  const [state, setState] = useState<VentureScopeState>(INITIAL_STATE);
  const streamCleanupRef = useRef<(() => void) | null>(null);
  const pollCleanupRef = useRef<(() => void) | null>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const clearTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  };

  const startTimer = () => {
    clearTimer();
    timerRef.current = setInterval(() => {
      setState((s) => ({ ...s, elapsedSeconds: s.elapsedSeconds + 1 }));
    }, 1000);
  };

  useEffect(() => {
    if (!state.jobId || state.useFallbackPolling) return;

    setState((s) => ({ ...s, streamPhase: "streaming" }));
    startTimer();

    streamCleanupRef.current = streamJobEvents(
      state.jobId,
      (event: SSEEvent) => {
        if (event.type === "heartbeat") {
          // ignore heartbeat data in UI
        } else if (event.type === "agent_update") {
          setState((s) => ({
            ...s,
            agentStatuses: event.agent_statuses ?? s.agentStatuses,
            currentNode: event.node ?? s.currentNode,
          }));
        } else if (event.type === "complete") {
          clearTimer();
          setState((s) => ({
            ...s,
            report: event.final_report,
            streamPhase: "complete",
            isLoading: false,
          }));
        } else if (event.type === "error") {
          clearTimer();
          setState((s) => ({
            ...s,
            streamPhase: "error",
            error: event.message,
            isLoading: false,
          }));
        }
      },
      (err: Error) => {
        // SSE connection totally failed
        setState((s) => ({
          ...s,
          useFallbackPolling: true,
        }));
      },
      () => {
        clearTimer();
        setState((s) => ({
          ...s,
          isLoading: false,
          streamPhase: s.report ? "complete" : s.streamPhase,
        }));
      },
      3
    );

    return () => {
      if (streamCleanupRef.current) {
        streamCleanupRef.current();
        streamCleanupRef.current = null;
      }
      clearTimer();
    };
  }, [state.jobId, state.useFallbackPolling]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (state.useFallbackPolling && state.jobId) {
      pollCleanupRef.current = pollJobReport(
        state.jobId,
        5000,
        36, // 3 minutes total tracking
        (report) => {
          clearTimer();
          setState((s) => ({
            ...s,
            report: report,
            streamPhase: "complete",
            isLoading: false,
          }));
        },
        () => {
          clearTimer();
          setState((s) => ({
            ...s,
            streamPhase: "error",
            error: "Polling failed. Timed out waiting for job completion.",
            isLoading: false,
          }));
        }
      );

      return () => {
        if (pollCleanupRef.current) {
          pollCleanupRef.current();
          pollCleanupRef.current = null;
        }
      };
    }
  }, [state.useFallbackPolling, state.jobId]);

  const setIdea = useCallback((idea: string) => {
    setState((s) => ({ ...s, idea }));
  }, []);

  const submitIdea = useCallback(async (idea: string) => {
    const trimmed = idea.trim();
    if (trimmed.length < 10) {
      setState((s) => ({
        ...s,
        error: "Please describe your idea in at least 10 characters.",
      }));
      return;
    }
    if (trimmed.length > 500) {
      setState((s) => ({
        ...s,
        error: "Your idea description must be 500 characters or fewer.",
      }));
      return;
    }

    setState((s) => ({
      ...s,
      idea: trimmed,
      isLoading: true,
      error: null,
      streamPhase: "connecting",
      report: null,
      agentStatuses: {},
      jobId: null,
      jobStatus: null,
      useFallbackPolling: false,
      elapsedSeconds: 0,
      currentNode: null,
    }));

    try {
      const { job_id } = await createJob(trimmed);
      setState((s) => ({ ...s, jobId: job_id }));
    } catch (err) {
      setState((s) => ({
        ...s,
        isLoading: false,
        streamPhase: "error",
        error: err instanceof Error ? err.message : "Failed to start pipeline.",
      }));
    }
  }, []);

  const reset = useCallback(() => {
    if (streamCleanupRef.current) streamCleanupRef.current();
    if (pollCleanupRef.current) pollCleanupRef.current();
    streamCleanupRef.current = null;
    pollCleanupRef.current = null;
    clearTimer();
    setState(INITIAL_STATE);
  }, []);

  return { ...state, setIdea, submitIdea, reset };
}
