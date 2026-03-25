import type {
  AgentStatus,
  FullReport,
  JobRecord,
  JobStatus,
  SSEEvent,
} from "./types";

export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let message = `HTTP ${res.status}`;
    try {
      const body = await res.json();
      message = body?.detail?.error ?? body?.detail ?? body?.error ?? message;
    } catch {
      // ignore json parse errors on error responses
    }
    throw new Error(message);
  }
  return res.json() as Promise<T>;
}

export async function createJob(
  idea: string
): Promise<{ job_id: string; status: string }> {
  const res = await fetch(`${API_BASE}/api/jobs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ idea }),
  });
  return handleResponse(res);
}

export async function getJobStatus(jobId: string): Promise<{
  job_id: string;
  status: JobStatus;
  agent_statuses: Record<string, AgentStatus>;
  updated_at: string;
}> {
  const res = await fetch(`${API_BASE}/api/jobs/${jobId}/status`);
  return handleResponse(res);
}

export async function getReport(jobId: string): Promise<FullReport | null> {
  const res = await fetch(`${API_BASE}/api/jobs/${jobId}/report`);
  if (res.status === 202) return null;
  return handleResponse<FullReport>(res);
}

export async function getJob(jobId: string): Promise<JobRecord> {
  const res = await fetch(`${API_BASE}/api/jobs/${jobId}`);
  return handleResponse<JobRecord>(res);
}

export function streamJobEvents(
  jobId: string,
  onEvent: (event: SSEEvent) => void,
  onError: (err: Error) => void,
  onDone: () => void,
  reconnectAttempts: number = 3
): () => void {
  let attempt = 0;
  let es: EventSource | null = null;
  let receivedDone = false;
  let retryTimeout: NodeJS.Timeout | null = null;
  let active = true;

  const connect = () => {
    if (!active) return;
    es = new EventSource(`${API_BASE}/api/jobs/${jobId}/stream`);

    const handleMessage = (raw: MessageEvent) => {
      try {
        const parsed = JSON.parse(raw.data as string);
        if (parsed.type === "heartbeat") {
          attempt = 0; // reset attempts on successful connection heartbeat
          return;
        }
        if (parsed.type === "done") {
          receivedDone = true;
          onDone();
          cleanup(false);
          return;
        }
        onEvent(parsed as SSEEvent);
      } catch {
        // Ignore malformed frames
      }
    };

    es.addEventListener("agent_update", handleMessage);
    es.addEventListener("complete", handleMessage);
    es.addEventListener("error", handleMessage as EventListener);
    es.addEventListener("done", handleMessage);
    es.onmessage = handleMessage;

    es.onerror = () => {
      if (!receivedDone && active) {
        es?.close();
        if (attempt < reconnectAttempts) {
          const delay = (2 ** attempt) * 1000;
          attempt++;
          console.warn(`SSE error. Reconnecting attempt ${attempt} in ${delay}ms...`);
          retryTimeout = setTimeout(connect, delay);
        } else {
          onError(new Error(`SSE connection failed after ${reconnectAttempts} reconnect attempts`));
          cleanup(false);
        }
      }
    };
  };

  const cleanup = (isUnmount: boolean) => {
    active = false;
    if (retryTimeout) clearTimeout(retryTimeout);
    if (es) {
      es.close();
      es = null;
    }
  };

  connect();

  return () => {
    cleanup(true);
  };
}

export function pollJobReport(
  jobId: string,
  intervalMs: number,
  maxAttempts: number,
  onReport: (r: FullReport) => void,
  onGiveUp: () => void
): () => void {
  let attempts = 0;
  let active = true;
  let timer: NodeJS.Timeout | null = null;

  const poll = async () => {
    if (!active) return;
    try {
      attempts++;
      const report = await getReport(jobId);
      if (report) {
        active = false;
        onReport(report);
        return;
      }
      if (attempts >= maxAttempts) {
        active = false;
        onGiveUp();
        return;
      }
      timer = setTimeout(poll, intervalMs);
    } catch {
      if (attempts >= maxAttempts) {
        active = false;
        onGiveUp();
      } else {
        timer = setTimeout(poll, intervalMs);
      }
    }
  };

  poll();

  return () => {
    active = false;
    if (timer) clearTimeout(timer);
  };
}
