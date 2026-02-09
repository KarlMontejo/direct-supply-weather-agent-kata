# Architecture

**Domain:** Food procurement (senior living)  
**Stack:** Next.js frontend, FastAPI backend, LangChain/LangGraph agent, in-memory SQLite

## Flow

```
User
  ↓
Frontend (Next.js chat UI)
  ↓
Backend (FastAPI) — POST /chat
  ↓
Agent (LangGraph ReAct loop)
  ↓
Tools: product_search, compliance_checker, calculator
  ↓
In-memory SQLite (products, contracts, inventory)
  ↓
Response back to frontend
```

## Layout

| Layer | Location | Purpose |
|-------|----------|---------|
| Frontend | `frontend/` | Chat UI, sends message + session_id, shows reply + tools_used |
| Backend | `backend/app/` | API, session store, agent bridge |
| Agent | `backend/app/agent/` | Prompts, procurement agent factory |
| Tools | `backend/app/tools/` | product_search (SQL), compliance_checker (sub-agent), calculator |
| Data | `backend/app/data_access/`, `backend/app/data/` | Loader, JSONL seed files |
| Schema | `backend/db/schema.sql` | products, contracts, inventory tables |

## Data

| Table | Source | Contents |
|-------|--------|----------|
| products | products.jsonl | Catalog with brand, category, ingredients, nutrition, pricing |
| contracts | contracts.jsonl | Approved brands, suppliers, dietary rules, effective dates |
| inventory | inventory.jsonl | Stock levels per distribution center |

All loaded into SQLite at startup. No persistence — resets on restart.
