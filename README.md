<h1 align="center">StratosAI — Multi-Agent Startup Validator</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/LangGraph-1C1C1C?style=flat-square" alt="LangGraph" />
  <img src="https://img.shields.io/badge/Groq-F55036?style=flat-square" alt="Groq" />
  <img src="https://img.shields.io/badge/Tavily-4B32C3?style=flat-square" alt="Tavily" />
  <img src="https://img.shields.io/badge/Python_3.11-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
</p>

## What is StratosAI?

StratosAI is an advanced multi-agent system designed to instantly validate startup ideas. It orchestrates 4 specialized AI agents through LangGraph to conduct in-depth market research, analyze competitors, generate financial models, and synthesis a final verdict. Results are streamed real-time via Server-Sent Events (SSE) to a gorgeous, highly-responsive Next.js dashboard. 

## Architecture

```text
User Input 
   │
   ▼
FastAPI Backend ──(SSE Stream)──▶ Next.js Dashboard
   │
   ▼
LangGraph Supervisor
   │
   ├──▶ Market Research Agent
   ├──▶ Competitor Analysis Agent
   ├──▶ Financial Modelling Agent
   └──▶ Synthesis Agent
```

## Agent Pipeline

| Agent | Role | Data Source | Output |
| --- | --- | --- | --- |
| **Market Research** | Computes TAM/SAM/SOM and identifies trends | Tavily + Groq | JSON (tam, sam, som, trends...) |
| **Competitor** | Finds competition and gauges threat levels | Tavily + Groq | JSON (competitors, threats...) |
| **Financial** | Generates conservative/base/optimistic models | Groq | JSON (revenue scenarios...) |
| **Synthesis** | Computes viability scores and aggregates data | Groq | JSON (scores, verdict...) |

## Tech Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| **Frontend** | Next.js, React, Tailwind CSS | Dashboard UI, hooks, and responsive components |
| **Backend** | FastAPI, Python 3.11+ | REST API, SSE streaming, job store |
| **Orchestration** | LangGraph | Graph state automation and agent routing |
| **LLM** | Groq (LLaMA 3) | Sub-second token generation for JSON responses |
| **Search** | Tavily Search | Web-native LLM research agent |
| **Streaming** | Server-Sent Events (SSE) | Real-time push updates for UI rendering |

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Groq API Key (Free at [console.groq.com](https://console.groq.com))
- Tavily API Key (Free tier at [app.tavily.com](https://app.tavily.com))

### Backend Setup

```powershell
git clone <repo-url>
cd StratosAI/backend
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
cp .env.example .env
# Fill in your GROQ_API_KEY and TAVILY_API_KEY in .env
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```powershell
cd ../frontend
npm install
cp .env.local.example .env.local
npm run dev
```

## API Reference

| Method | Endpoint | Description | Response |
| --- | --- | --- | --- |
| POST | `/api/jobs` | Submit an idea | `{ "job_id": "...", "status": "pending" }` |
| GET | `/api/jobs/{id}/stream` | SSE stream for a job | Server-Sent Events |
| GET | `/api/jobs/{id}` | Get full job state | `JobRecord` JSON |
| GET | `/api/jobs/{id}/status` | Check agent status | Job Status JSON |
| GET | `/api/jobs/{id}/report` | Get completed report | FullReport or 202 if pending |

## Project Structure

```text
StratosAI/
├── backend/                  # FastAPI & Agent logic
│   ├── agents/               # Individual specialized LLM agents
│   ├── api/                  # FastAPI routers
│   ├── graph/                # LangGraph builders and runners
│   ├── models/               # Pydantic schemas
│   ├── store/                # In-memory jobs & EventBus 
│   ├── utils/                # Helpers, timeouts, filters
│   └── main.py               # Uvicorn entrypoint
│
└── frontend/                 # Next.js Application
    ├── app/                  # Pages & Layouts
    ├── components/           # UI Elements (Dashboard, Verdicts)
    └── lib/                  # types, fetch calls, hooks (useVentureScope)
```

## Edge Cases Handled

- **LLM Timeouts & Retry**: Agents retry gracefully using exponential backoffs safely avoiding eternal freezing.
- **SSE Auto-Reconnect**: Automatic exponential reconnection for the SSE event stream ensuring the UX never stalls.
- **Partial Pipeline**: If one agent fails, the supervisor node synthesizes a partial fallback preventing total pipeline failures.
- **Relevance Filtering**: Agent context windows are managed strictly via a mini relevance filter node reducing hallucination probabilities on Tavily output.
- **Graceful UI Degradation**: If a stream completes but data pieces are unavailable, the Next.js frontend visually decays rather than crashing.

## License

MIT License.
