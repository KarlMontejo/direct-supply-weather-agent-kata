# builds the main procurement agent — wires up the llm, tools, and system prompt.
# called once at startup, then the agent instance is reused for every request.

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from backend.app.agent.prompts import PROCUREMENT_SYSTEM_PROMPT
from backend.app.tools.product_search import product_search
from backend.app.tools.compliance_checker import compliance_checker
from backend.app.tools.calculator import calculator
from backend.app.config import MODEL_NAME, MODEL_TEMPERATURE


def create_procurement_agent():
    # set up the chat model with whatever is in our config
    model = init_chat_model(model=MODEL_NAME, temperature=MODEL_TEMPERATURE)

    tools = [product_search, compliance_checker, calculator]

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=PROCUREMENT_SYSTEM_PROMPT,
    )

    return agent
