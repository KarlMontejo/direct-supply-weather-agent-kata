"""
Compliance checker tool — evaluates product orders against procurement policy.

Internally delegates to a compliance sub-agent (LLM with structured output)
that reasons over the policy text and returns a ComplianceAssessment.
"""

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from backend.app.schemas.compliance_assessment import ComplianceAssessment
from backend.app.schemas.product_order import ProductOrder
from ai_services.agent.prompts import COMPLIANCE_SYSTEM_PROMPT
from backend.app.config import MODEL_NAME, MODEL_TEMPERATURE

# Compliance sub-agent — a structured-output LLM, not a tool-calling agent.
# It evaluates orders against the procurement policy loaded in prompts.py.
_compliance_model = init_chat_model(model=MODEL_NAME, temperature=MODEL_TEMPERATURE)

_compliance_agent = create_agent(
    system_prompt=COMPLIANCE_SYSTEM_PROMPT,
    response_format=ComplianceAssessment,
    model=_compliance_model,
)


@tool
def compliance_checker(
    product_order: ProductOrder, original_user_query: str
) -> ComplianceAssessment:
    """
    Evaluate a product order for compliance with company procurement policies.

    Args:
        product_order: The proposed order containing line items (product_id + quantity).
        original_user_query: The user's original procurement request for context.

    Returns:
        A ComplianceAssessment with an is_compliant flag and a list of violations.
    """
    inputs = {
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Original User Query: {original_user_query}\n"
                    f"Product Order: {product_order.model_dump_json()}\n\n"
                    "Determine if the order complies with the company policies. "
                    "If there are any violations, identify the specific products "
                    "and the reasons for non-compliance. Return a structured report "
                    "indicating whether the order is compliant and detailing any violations."
                ),
            }
        ]
    }
    return _compliance_agent.invoke(inputs)
