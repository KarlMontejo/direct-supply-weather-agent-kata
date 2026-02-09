# Decisions

## Architecture

- **Single backend** — AI layer (agent, tools, prompts) lives inside backend. No separate ai_services process.
- **Session on backend** — Frontend sends session_id + message. Backend owns full history. Simpler client, single source of truth.
- **In-memory SQLite** — Demo only. No persistence. Resets on restart.

## API

- **POST /chat** — Request: `{ session_id?, message }`. Response: `{ session_id, messages }` with `tools_used` per assistant message.
- **No full history in request** — Frontend never sends the full conversation. Backend already has it.

## Agent

- **Three tools** — product_search (SQL over products/contracts/inventory), compliance_checker (sub-agent), calculator.
- **ReAct-style loop** — LangGraph create_agent. LLM decides when to call tools or respond.
- **Compliance as sub-agent** — Separate LLM + policy prompt. Main agent calls it as a tool for structured output.
