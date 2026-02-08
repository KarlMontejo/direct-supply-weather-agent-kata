"""
Procurement agent — the core agentic reasoning layer.

Creates a LangChain/LangGraph agent wired with procurement tools
and a domain-specific system prompt. The agent interprets user intent,
selects appropriate tools, reasons across constraints, and generates
explainable procurement recommendations.
"""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from ai_services.agent.prompts import PROCUREMENT_SYSTEM_PROMPT
from ai_services.tools.product_search import product_search
from ai_services.tools.compliance_checker import compliance_checker
from ai_services.tools.calculator import calculator
from backend.app.config import MODEL_NAME, MODEL_TEMPERATURE


def create_procurement_agent():
    """
    Build and return the procurement agent.

    The agent is backed by a chat model and equipped with tools for:
    - Product search (SQL queries against the product catalog)
    - Compliance checking (policy validation via sub-agent)
    - Arithmetic calculation (cost totals, quantity planning)

    Returns a LangGraph agent ready to be invoked with a messages dict.
    """
    model = init_chat_model(model=MODEL_NAME, temperature=MODEL_TEMPERATURE)

    tools = [product_search, compliance_checker, calculator]

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=PROCUREMENT_SYSTEM_PROMPT,
    )

    return agent
