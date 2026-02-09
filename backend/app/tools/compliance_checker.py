# wraps a separate llm (the "compliance sub-agent") that checks whether
# a proposed order follows Karl's procurement contracts and policies.
# when the main agent calls this tool, it hands off the order to the
# sub-agent which returns a structured pass/fail assessment.

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from backend.app.schemas.compliance_assessment import ComplianceAssessment
from backend.app.schemas.product_order import ProductOrder
from backend.app.agent.prompts import COMPLIANCE_SYSTEM_PROMPT
from backend.app.config import MODEL_NAME, MODEL_TEMPERATURE

# initialize the compliance sub-agent once at import time
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
    Evaluate a product order for compliance with Karl's Senior Living
    of Dallas procurement policies and contracts.

    Args:
        product_order: the proposed order with line items (product_id + quantity).
        original_user_query: the user's original request, for context.

    Returns:
        a ComplianceAssessment with is_compliant flag and list of violations.
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
