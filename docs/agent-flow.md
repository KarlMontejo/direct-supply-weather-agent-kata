# Agent Flow

## Loop

1. User sends message → backend appends to session history
2. LangGraph agent receives full history
3. LLM decides: call tool(s) or respond
4. If tool: call product_search / compliance_checker / calculator
5. Tool result returns to LLM
6. Repeat until LLM produces final answer
7. Backend extracts tool names from turn, returns history + tools_used to frontend

## Tools

| Tool | Input | Output |
|------|-------|--------|
| product_search | SQL string | List of products (or contracts/inventory rows) |
| compliance_checker | ProductOrder + context | ComplianceAssessment (violations, is_compliant) |
| calculator | Arithmetic expression | Numeric result |

## Sub-agent

The compliance_checker wraps a second LLM with the compliance system prompt. Main agent delegates compliance reasoning to it. Returns structured ComplianceAssessment.
