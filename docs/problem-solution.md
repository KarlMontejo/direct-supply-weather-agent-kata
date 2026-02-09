# Problem and Solution

## Context

Food procurement in healthcare and senior living is high-frequency, constraint-heavy, and fragile. Stock-outs cascade quickly. Contracts define brands, pack sizes, suppliers, and effective dates — small deviations break compliance. Finding compliant, available substitutes is slow and error-prone.

## Problems

1. **Stock-outs** — Products go unavailable or partially unavailable. Manual substitution is slow.
2. **Compliance** — Contracts specify brands, sizes, suppliers, dietary rules. Easy to break, hard to fix.
3. **Discovery** — Checking multiple systems for compliant alternatives is fragmented. Staff rely on tribal knowledge.

## Solution

An agentic LLM chatbot that acts as decision-support. It does not place orders. It recommends and explains.

- Resolves stock-outs by finding compliant substitutes
- Validates proposed orders against contracts and policy
- Searches catalog by name, price, supplier, availability, dietary flags
- Drafts order recommendations with reasoning

## Data

In-memory SQLite seeded from mock JSONL: products, contracts, inventory. Designed with edge cases (expired contracts, stock-outs, prohibited ingredients). See `backend/app/data/EDGE_CASES.md`.
