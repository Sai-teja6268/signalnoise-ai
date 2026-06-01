# SignalNoise AI — Claude Context File

## Project Overview

**SignalNoise AI** is an enterprise AI platform that surfaces weak signals hidden in organizational communications and operational documents. It uses RAG, Multi-Agent AI, Trend Analysis, and Risk Scoring to detect emerging risks before they escalate.

- **Version:** 1.0
- **Architecture Style:** Multi-Agent RAG
- **Primary Goal:** Ingest enterprise documents → extract signals → analyze trends → score risks → generate executive summaries

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + Uvicorn |
| Agent Orchestration | LangGraph |
| RAG Framework | LangChain |
| LLM | OpenAI |
| Vector Database | ChromaDB |
| Relational Database | PostgreSQL |
| Observability | LangSmith |
| Containerization | Docker |
| Frontend | React / Next.js |

---

## Key Libraries

**AI**
- `langchain`, `langgraph`, `langsmith`, `openai`, `chromadb`

**API**
- `fastapi`, `uvicorn`, `pydantic`

**Database**
- `sqlalchemy`, `psycopg2`, `alembic`

**Utilities**
- `python-dotenv`, `pandas`, `numpy`

---

## Architecture

### End-to-End Processing Flow

```
Upload Document
  → Validate
  → Extract Text
  → Chunk Text
  → Generate Embeddings
  → Store Vectors (ChromaDB)
  → Retrieve Evidence
  → Extract Signals       [Signal Agent]
  → Analyze Trends        [Trend Agent]
  → Score Risks           [Risk Agent]
  → Generate Summary      [Summary Agent]
  → Persist Results (PostgreSQL)
```

### Agent Responsibilities

| Agent | Role |
|---|---|
| Signal Extraction Agent | Detect blockers, delays, escalations, customer concerns |
| Trend Analysis Agent | Identify recurring patterns and directional trends |
| Risk Scoring Agent | Assign risk category and confidence score |
| Executive Summary Agent | Produce leadership-focused reports |
| Evaluation Agent | Measure quality, groundedness, and faithfulness |

---

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/documents/upload` | Upload and process a document |
| POST | `/signals/analyze` | Trigger multi-agent analysis |
| GET | `/signals` | Retrieve extracted signals |
| GET | `/risks` | Retrieve risk assessments |
| GET | `/summary` | Retrieve executive summary |
| GET | `/health` | Health check |

---

## Database Design

### PostgreSQL Tables

- `documents` — raw ingested documents
- `signals` — extracted signals per document
- `trends` — aggregated trend patterns
- `risk_assessments` — scored risk records
- `agent_executions` — agent run logs
- `evaluations` — quality metric records

**Relationship chain:** `Document → Signal → Trend → Risk Assessment`

### ChromaDB Collection

**Collection name:** `signalnoise_documents`

**Metadata fields:** `document_id`, `source`, `team`, `date`, `project`, `department`

---

## Security

- JWT Authentication
- Role-Based Access Control (RBAC)
- Encryption at rest and in transit
- Audit logging
- Secret management

---

## Evaluation Metrics

**Retrieval:** Context Precision, Context Recall

**Generation:** Groundedness, Faithfulness

**Business:** Signal Accuracy, Risk Detection Accuracy, False Positive Rate

---

## Deployment

**Current:** Docker Compose with FastAPI, PostgreSQL, ChromaDB containers

**Future:**
- Kubernetes
- CI/CD pipelines
- Full monitoring stack

---

## Roadmap

| Phase | Features |
|---|---|
| Phase 2 | Slack integration, Teams integration, real-time ingestion |
| Phase 3 | GraphRAG, Knowledge Graph, predictive risk detection |
| Phase 4 | Enterprise dashboards, autonomous monitoring agents |

---

## Development Notes for Claude

- All agent orchestration flows through **LangGraph** — changes to agent logic should preserve the graph structure.
- **ChromaDB** is the sole vector store; embedding generation happens before storage, not at query time.
- **LangSmith** is used for tracing — wrap new agent steps in tracing spans where possible.
- Database migrations are managed via **Alembic**; never alter tables directly.
- The `agent_executions` table is append-only for auditability — do not update or delete rows.
- Prefer adding new agents as nodes in the LangGraph graph rather than expanding existing agent responsibilities.