# Agentic Food Procurement Assistant

**Name:** Karl Montejo
**Date:** 2/8/2026
**Company:** Direct Supply

---

## What This Is

An AI-powered chatbot that helps food procurement teams at senior living facilities make better purchasing decisions. It searches product catalogs, checks orders against contracts and compliance rules, and recommends compliant alternatives when things go wrong (stock-outs, expired contracts, dietary violations).

Built for **Karl's Senior Living of Dallas** as a demonstration of how agentic AI can reduce friction in healthcare food procurement.

---

## Problem

Food procurement in healthcare and senior living is operationally complex:

- **Stock-outs are frequent** — a single unavailable product can disrupt meals across an entire facility
- **Contracts are strict** — approved brands, pack sizes, suppliers, dietary restrictions, and effective dates must all align
- **Finding substitutes is slow** — staff manually cross-reference inventory, contracts, and catalogs under time pressure

These tasks are repetitive, error-prone, and hard to scale.

---

## Solution

An **agentic LLM-powered chatbot** that acts as a decision-support tool. It does not place orders — it recommends and explains.

The system helps procurement agents:

- Detect and resolve stock-outs by finding compliant substitutes
- Validate proposed orders against contract and compliance rules
- Search the product catalog by name, price, supplier, availability, or dietary requirements
- Draft order recommendations with clear reasoning

The AI agent has three tools it can call on its own:

| Tool | What It Does |
|---|---|
| `product_search` | Queries the product catalog, contracts, and inventory via SQL |
| `compliance_checker` | Evaluates a proposed order against procurement policies using a second LLM |
| `calculator` | Does arithmetic for cost totals and quantity planning |

---

## Architecture

```
frontend/  (Next.js + React + Tailwind)
  └── Chat UI → sends messages to backend

backend/   (Python + FastAPI + LangChain)
  ├── app/api/         → POST /chat endpoint
  ├── app/agent/       → LangGraph procurement agent + system prompts
  ├── app/tools/       → product_search, compliance_checker, calculator
  ├── app/data_access/ → in-memory SQLite loader
  ├── app/data/        → mock products, contracts, inventory (JSONL)
  ├── app/schemas/     → Pydantic models for API + domain objects
  ├── app/services/    → session management + agent bridge
  └── db/              → SQL schema
```

The backend manages conversation sessions — the frontend just sends the new message and a session ID, and gets back the full chat history with tool usage annotations.

---

## Data

Three mock datasets loaded into an in-memory SQLite database at startup:

| Table | Records | What It Represents |
|---|---|---|
| `products` | 44 | Food catalog with brand, category, ingredients, nutrition, dietary flags, pricing |
| `contracts` | 14 | Procurement rules for Karl's Senior Living — approved brands, suppliers, prohibited ingredients, sodium limits |
| `inventory` | 72 | Stock levels across 3 distribution centers (midwest, southeast, northeast) |

The data is intentionally designed with edge cases: expired contracts, off-contract alternatives that look cheaper, stock-outs that force substitution, prohibited ingredients (pork, shellfish, peanuts), and facility-specific sodium limits. See `backend/app/data/EDGE_CASES.md` for the full test scenario matrix.

---

## Running It

**Prerequisites:** Python 3.11+, Node.js 18+, an OpenAI API key

**Backend:**

```bash
cp .env.example .env
# add your OPENAI_API_KEY to .env

set -a && source .env && set +a && uv run uvicorn backend.app.main:app --reload
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `localhost:3000`, the backend on `localhost:8000`.

---

## Tech Stack

- **Frontend:** React, Next.js, Tailwind CSS, TypeScript
- **Backend:** Python, FastAPI, Pydantic
- **AI:** LangChain, LangGraph, OpenAI (gpt-4.1-mini)
- **Database:** SQLite (in-memory)
- **Data:** JSONL seed files for products, contracts, and inventory

---

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── agent/           # procurement agent + system prompts
│   │   ├── api/             # POST /chat endpoint
│   │   ├── data/            # mock JSONL datasets + edge case docs
│   │   ├── data_access/     # sqlite loader
│   │   ├── schemas/         # pydantic models
│   │   ├── services/        # session management + agent bridge
│   │   ├── tools/           # product_search, compliance_checker, calculator
│   │   ├── config.py        # env var configuration
│   │   └── main.py          # fastapi entrypoint
│   └── db/
│       └── schema.sql       # sqlite table definitions
├── frontend/
│   ├── app/                 # next.js pages and layout
│   ├── components/          # ChatWindow, MessageBubble
│   └── services/            # api client
├── notebooks/
│   └── poc.ipynb            # original proof of concept
├── docs/                    # architecture, user stories, decisions
├── .env.example
├── pyproject.toml
└── README.md
```

---

## Notes

- The mock data is designed for demonstration, not production. In a real system, the JSONL files would be replaced by enterprise inventory, contract, and supplier APIs.
- The in-memory SQLite database resets on every server restart — there is no persistence.
- The chatbot does not execute orders. It produces recommendations that humans review and approve.
